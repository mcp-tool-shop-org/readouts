# Native audio and MIDI host — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](host-audio-and-midi.md) · [catalog index](README.md)

## Anchor midir microseconds to cpal StreamInstant and re-anchor for drift
**Because midir timestamps and cpal StreamInstant come from independent clocks, the host must establish an anchor and re-anchor periodically to keep the law’s sample clock aligned.**

*Check 1: midir timestamp and cpal StreamInstant types can be combined* · `compiles` · edition 2024 · host · bin · deps: cpal, midir · jam dependency set · **✔ oracle pass**
```rust
use cpal::StreamInstant;
fn midi_to_sample_offset(midi_us: u64, _anchor_cpal: StreamInstant, anchor_midi_us: u64, sample_rate: u32) -> i64 {
    let delta_us = midi_us as i64 - anchor_midi_us as i64;
    (delta_us * sample_rate as i64) / 1_000_000
}
fn main() {
    let _ = midi_to_sample_offset(1000, StreamInstant::ZERO, 0, 48000);
}
```

## Build cpal output stream in f32 for highest real-time priority
**cpal ranks F32 highest in its default-format heuristic because it is the universal real-time audio format, and build_output_stream::<f32> selects compile-time sample processing.**

*Check 1: cpal F32 output stream compiles* · `compiles` · edition 2024 · host · bin · deps: cpal · jam dependency set · **✔ oracle pass**
```rust
use cpal::traits::{DeviceTrait, HostTrait};
fn main() {
    let host = cpal::default_host();
    if let Some(device) = host.default_output_device() {
        let supported = device.default_output_config().unwrap();
        let config = supported.config();
        let _stream = device.build_output_stream::<f32, _, _>(
            config,
            move |_data: &mut [f32], _info: &cpal::OutputCallbackInfo| {},
            move |_err| {},
            None,
        );
    }
}
```

## Count allocations across a simulated audio callback popping rtrb into an f32 buffer
**A counting #[global_allocator] records zero new allocations during a simulated callback that pops from an rtrb Consumer into a stack f32 buffer.**

*Check 1: Counting allocator shows zero allocs in simulated callback body* · `runs` · edition 2024 · host · bin · deps: rtrb · jam dependency set · **✔ oracle pass**
```rust
use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering};
use rtrb::RingBuffer;

struct CountingAllocator;

static ALLOC_COUNT: AtomicUsize = AtomicUsize::new(0);

unsafe impl GlobalAlloc for CountingAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        ALLOC_COUNT.fetch_add(1, Ordering::SeqCst);
        System.alloc(layout)
    }
    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        System.dealloc(ptr, layout)
    }
}

#[global_allocator]
static GLOBAL: CountingAllocator = CountingAllocator;

fn main() {
    let (mut producer, mut consumer) = RingBuffer::<f32>::new(64);
    for i in 0..10 {
        producer.push(i as f32).unwrap();
    }

    ALLOC_COUNT.store(0, Ordering::SeqCst);

    let mut buf = [0.0f32; 64];
    let mut idx = 0;
    while let Ok(v) = consumer.pop() {
        if idx < buf.len() {
            buf[idx] = v;
            idx += 1;
        } else {
            break;
        }
    }

    let count = ALLOC_COUNT.load(Ordering::SeqCst);
    println!("alloc_count={}", count);
}
```
Expected output: `alloc_count=0`

## Create rtrb RingBuffer before the stream because only RingBuffer::new allocates
**rtrb 0.4.0 allocates its backing buffer in RingBuffer::new, not during push or pop, so the ring must be created before the stream starts.**

*Check 1: RingBuffer::new allocates but push and pop do not* · `runs` · edition 2024 · host · bin · deps: rtrb · jam dependency set · **✔ oracle pass**
```rust
use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering};
use rtrb::RingBuffer;

struct CountingAllocator;
static ALLOC_COUNT: AtomicUsize = AtomicUsize::new(0);

unsafe impl GlobalAlloc for CountingAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        ALLOC_COUNT.fetch_add(1, Ordering::SeqCst);
        System.alloc(layout)
    }
    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        System.dealloc(ptr, layout)
    }
}

#[global_allocator]
static GLOBAL: CountingAllocator = CountingAllocator;

fn main() {
    ALLOC_COUNT.store(0, Ordering::SeqCst);
    let (mut p, mut c) = RingBuffer::<f32>::new(4);
    let after_new = ALLOC_COUNT.load(Ordering::SeqCst);

    ALLOC_COUNT.store(0, Ordering::SeqCst);
    p.push(1.0).unwrap();
    p.push(2.0).unwrap();
    c.pop().unwrap();
    let after_ops = ALLOC_COUNT.load(Ordering::SeqCst);

    if after_new > 0 && after_ops == 0 {
        println!("new_allocates ops_do_not");
    } else {
        println!("unexpected new={} ops={}", after_new, after_ops);
    }
}
```
Expected output: `new_allocates ops_do_not`

## Interpret midir WinMM input timestamps as microseconds since start
**midir’s WinMM backend delivers input callback timestamps in microseconds, converted from the Windows MIDI driver’s millisecond timestamp that starts at zero when midiInStart is called.**

*Check 1: midir input callback signature and timestamp type compile* · `compiles` · edition 2024 · host · bin · deps: midir · jam dependency set · **✔ oracle pass**
```rust
use midir::{MidiInput, Ignore};
fn main() {
    let mut midi_in = MidiInput::new("test").unwrap();
    midi_in.ignore(Ignore::None);
    let _ports = midi_in.ports();
    let _conn = midi_in.connect(
        &_ports[0],
        "test-port",
        move |_timestamp: u64, _message: &[u8], _data: &mut ()| {},
        (),
    );
}
```

## Negative control: Vec push inside callback body increments allocator counter
**A Vec::push inside the same simulated callback body increments the counting allocator, confirming the measurement is sensitive.**

*Check 1: Vec push inside callback body increments allocation counter* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering};

struct CountingAllocator;
static ALLOC_COUNT: AtomicUsize = AtomicUsize::new(0);

unsafe impl GlobalAlloc for CountingAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        ALLOC_COUNT.fetch_add(1, Ordering::SeqCst);
        System.alloc(layout)
    }
    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        System.dealloc(ptr, layout)
    }
}

#[global_allocator]
static GLOBAL: CountingAllocator = CountingAllocator;

fn main() {
    let mut v = Vec::new();
    ALLOC_COUNT.store(0, Ordering::SeqCst);
    v.push(1.0f32);
    let count = ALLOC_COUNT.load(Ordering::SeqCst);
    if count > 0 {
        println!("alloc_count>0");
    } else {
        println!("alloc_count=0");
    }
}
```
Expected output: `alloc_count>0`

## Register assert_no_alloc AllocDisabler around the callback body to catch debug allocations
**With AllocDisabler registered as #[global_allocator], assert_no_alloc aborts in debug if the callback body allocates and returns normally when it does not.**

*Check 1: assert_no_alloc returns normally when callback body does not allocate* · `runs` · edition 2024 · host · bin · deps: rtrb, assert_no_alloc · jam dependency set · **✔ oracle pass**
```rust
use assert_no_alloc::{AllocDisabler, assert_no_alloc};
use rtrb::RingBuffer;

#[global_allocator]
static A: AllocDisabler = AllocDisabler;

fn main() {
    let (mut producer, mut consumer) = RingBuffer::<f32>::new(64);
    for i in 0..5 {
        producer.push(i as f32).unwrap();
    }

    let sum = assert_no_alloc(move || {
        let mut s = 0.0f32;
        while let Ok(v) = consumer.pop() {
            s += v;
        }
        s
    });

    println!("sum={}", sum);
}
```
Expected output: `sum=10`

## Render oscillator voices from SPSC queue into cpal silence buffer
**The cpal output callback buffer is pre-filled with silence, and the callback can pop committed events from an rtrb Consumer without blocking or allocating.**

*Check 1: SPSC event queue feeds non-allocating audio callback simulation* · `runs` · edition 2024 · host · bin · deps: rtrb · jam dependency set · **✔ oracle pass**
```rust
use rtrb::{RingBuffer, PopError};
fn main() {
    let (mut prod, mut cons) = RingBuffer::<f32>::new(16);
    prod.push(0.5).unwrap();
    prod.push(-0.5).unwrap();
    let mut buf = [0.0f32; 4];
    for s in buf.iter_mut() {
        *s = cons.pop().unwrap_or(0.0);
    }
    assert_eq!(buf, [0.5, -0.5, 0.0, 0.0]);
    println!("ok");
}
```
Expected output: `ok`

## Request cpal BufferSize::Fixed on WASAPI shared-mode output
**cpal’s WASAPI backend always creates shared-mode streams, and BufferSize::Fixed only requests a callback size that the host may round.**

*Check 1: cpal BufferSize::Fixed and shared mode compile* · `compiles` · edition 2024 · host · bin · deps: cpal · jam dependency set · **✔ oracle pass**
```rust
use cpal::{BufferSize, StreamConfig};
use cpal::traits::{DeviceTrait, HostTrait};
fn main() {
    let host = cpal::default_host();
    if let Some(device) = host.default_output_device() {
        let config = StreamConfig {
            channels: 2,
            sample_rate: 48000,
            buffer_size: BufferSize::Fixed(256),
        };
        let _ = device.build_output_stream::<f32, _, _>(
            config,
            move |_data: &mut [f32], _info: &cpal::OutputCallbackInfo| {},
            move |_err| {},
            None,
        );
    }
}
```

## Use OutputCallbackInfo playback timestamp for latency alignment
**cpal output callbacks receive an OutputCallbackInfo whose timestamp contains a callback instant and a predicted playback instant derived from the device clock and buffered frames.**

*Check 1: OutputCallbackInfo timestamp fields accessible* · `compiles` · edition 2024 · host · bin · deps: cpal · jam dependency set · **✔ oracle pass**
```rust
use cpal::traits::{DeviceTrait, HostTrait};
fn main() {
    let host = cpal::default_host();
    if let Some(device) = host.default_output_device() {
        let config = device.default_output_config().unwrap().config();
        let _stream = device.build_output_stream::<f32, _, _>(
            config,
            move |_data: &mut [f32], info: &cpal::OutputCallbackInfo| {
                let ts = info.timestamp();
                let _callback = ts.callback;
                let _playback = ts.playback;
            },
            move |_err| {},
            None,
        );
    }
}
```

## Enumerate midir WinMM input ports by interface ID
**MidiInput::ports returns a vector of MidiInputPort values on Windows via the WinMM midiInGetNumDevs and midiInGetDevCapsW APIs.**

*Check 1: midir port enumeration compiles on Windows host* · `compiles` · edition 2024 · host · bin · deps: midir · jam dependency set · **✔ oracle pass**
```rust
use midir::MidiInput;
fn main() {
    let midi_in = MidiInput::new("test").unwrap();
    let ports = midi_in.ports();
    for port in &ports {
        let _name = midi_in.port_name(port).unwrap();
        let _id = port.id();
    }
}
```

## Handle cpal WASAPI xruns and device changes in error callback
**The cpal WASAPI backend forwards discontinuities as ErrorKind::Xrun and device removals as DeviceNotAvailable or StreamInvalidated on the error callback.**

*Check 1: cpal error callback handles ErrorKind* · `compiles` · edition 2024 · host · bin · deps: cpal · jam dependency set · **✔ oracle pass**
```rust
use cpal::{Error, ErrorKind};
use cpal::traits::{DeviceTrait, HostTrait};
fn main() {
    let host = cpal::default_host();
    if let Some(device) = host.default_output_device() {
        let config = device.default_output_config().unwrap().config();
        let _stream = device.build_output_stream::<f32, _, _>(
            config,
            move |_data: &mut [f32], _info: &cpal::OutputCallbackInfo| {},
            move |err: Error| {
                match err.kind() {
                    ErrorKind::Xrun => {}
                    ErrorKind::DeviceNotAvailable => {}
                    ErrorKind::StreamInvalidated => {}
                    _ => {}
                }
            },
            None,
        );
    }
}
```

## Send events to audio callback via lock-free rtrb or ringbuf queue
**Both rtrb and ringbuf provide single-producer single-consumer queues that are lock-free and allocate only on construction, making them safe for real-time audio callbacks.**

*Check 1: rtrb SPSC queue works across threads without blocking* · `runs` · edition 2024 · host · bin · deps: rtrb · jam dependency set · **✔ oracle pass**
```rust
use rtrb::{RingBuffer, PopError};
fn main() {
    let (mut p, mut c) = RingBuffer::<i32>::new(4);
    std::thread::spawn(move || {
        p.push(1).unwrap();
        p.push(2).unwrap();
    }).join().unwrap();
    assert_eq!(c.pop(), Ok(1));
    assert_eq!(c.pop(), Ok(2));
    assert_eq!(c.pop(), Err(PopError::Empty));
    println!("ok");
}
```
Expected output: `ok`

## Wrap oscillator callback in assert_no_alloc with cpal equilibrium buffer
**assert_no_alloc aborts or warns if the audio callback allocates, and cpal pre-fills the output buffer with silence before invoking the callback.**

*Check 1: assert_no_alloc wraps cpal callback pattern compiles* · `compiles` · edition 2024 · host · bin · deps: cpal, assert_no_alloc · jam dependency set · **✔ oracle pass**
```rust
use assert_no_alloc::assert_no_alloc;
use cpal::traits::{DeviceTrait, HostTrait};
fn main() {
    let host = cpal::default_host();
    if let Some(device) = host.default_output_device() {
        let config = device.default_output_config().unwrap().config();
        let _stream = device.build_output_stream::<f32, _, _>(
            config,
            move |_data: &mut [f32], _info: &cpal::OutputCallbackInfo| {
                assert_no_alloc(|| {
                    for s in _data.iter_mut() { *s = 0.0; }
                });
            },
            move |_err| {},
            None,
        );
    }
}
```

*Check 2: with AllocDisabler as #[global_allocator], an allocation inside assert_no_alloc aborts (debug build); one outside it is allowed* · `runs` · edition 2024 · host · bin · deps: assert_no_alloc · jam dependency set · exit code 3221226505 · **✔ oracle pass**
```rust
use assert_no_alloc::{assert_no_alloc, AllocDisabler};

#[global_allocator]
static ALLOC: AllocDisabler = AllocDisabler;

fn main() {
    println!("before");
    // Allowed: outside assert_no_alloc.
    let ok: Vec<u8> = Vec::with_capacity(8);
    std::hint::black_box(&ok);
    // Forbidden: an allocation inside the closure reaches AllocDisabler, which calls handle_alloc_error.
    assert_no_alloc(|| {
        let v: Vec<u8> = Vec::with_capacity(16);
        std::hint::black_box(&v);
    });
    println!("unreachable");
}
```
Expected output: `before`

