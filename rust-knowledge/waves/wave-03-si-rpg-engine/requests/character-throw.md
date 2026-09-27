# Character throw: kinematic contact becomes dynamic speed

Issues #128 and #121. Two sources, kept apart. The measurements are from 2026-09-26. This note was written on 2026-09-27 and does not re-run either one.

**#121** is [`crate-eject.md`](crate-eject.md), measured on si-rpg-engine `main` at `19cf8c8`. rapier3d-f64 0.35.3 with `enhanced-determinism`, parry3d-f64 0.30.2, rustc 1.98.1.

**#128** is the overseer's JavaScript replay on `main` at `1da5f6a`, product law `fd4b46bb45f299894d31e8745a3649f986c08b95ad3acba7ec20d70bfef2fde2`. The same reading is summarised in pull request #136 (`docs/dispatch-128-driven-contacts.md`). The scripts are not in this repository. Numbers from that reading are marked [RELAYED].

On `origin/main` at `09e3bf7` these still match the code: `solverModes` is at `packages/tick/world.js:127`, `pinCarried` sets a carried body's linear and angular velocity to 0, and `solver/src/rapier_law.rs` sets `vy = b[4] + G * DT` at line 810 and `vy = 0.0` when the controller reports grounded at line 831. `to_dynamic` starts at line 524 on that commit. The relay names line 519, which is where the function stood at `1da5f6a`.

## What the two share

A driven character in deep contact with a dynamic body. The contact solver turns a kinematic fact into dynamic velocity.

- **#128, the squeeze.** [RELAYED] While driven, the walker cannot produce 11 m/s. Its vertical velocity is the record plus gravity, and it is set to 0 when grounded. From t322 the refusals walker walks west across the dynamic crate. The crate tips from 0° to 42.5° by t355. The walker's feet sit 0.08 to 0.09 below the crate's AABB top. Warm-starts at t350 to t355 are walker–crate about 3.1 to 3.4 N·s over 4 points, and ledge–crate about the same, against a crate weight impulse of 0.027 N·s per quantum. At t356 the in-place switch to dynamic keeps the pairs and their warm-starts. The first dynamic step applies that impulse to a walker of 0.125 kg. It leaves at about (−1.29, 11.12, −0.70) m/s and reaches y 8.9. A fresh world loaded from the same t355 poses, the walker's velocity zeroed and no stored impulses, steps once to 0.81 m/s for the walker and 0.33 m/s for the crate. The geometry does not throw. The stored impulse does.

- **#121, the step.** [MEASURED in `crate-eject.md`] A 0.25 autostep is a pose change. Rapier turns it into about 16 m/s with `interpolate_velocity`, and the contact solver writes that onto a dynamic box the walker overlaps, or onto a box that only meets the walker's head. The engine's push copy does not write it. F5's guard does not see it: the guard reads horizontal speed from the record at the start of the quantum, and the plan's vertical velocity is 0 once the controller reports grounded.

## Where dispatch 128 leaves the measurement

Pull request #136 first said the contact solver writes that speed onto a dynamic box the walker overlaps or carries. Commit `c0d3f55`, merged as `895b2bf`, corrects the red.

`crate-eject.md` measures the carried case on its own. A carried body is not in the solver (`Mode::Carried` inserts no body). After the step, `pinCarried` (`packages/tick/world.js`) copies the body to the walker's head and sets its velocity to 0. On that same 0.25 step the carried box ends at speed 0. An overlapping box leaves at about 16.58 m/s. A box that only meets the head leaves at about 16.51 m/s. The push's own contribution on those boxes is about 0.007 m/s, and the step writes the rest.

A red room that requires a carried box to leave at 16 m/s does not go red on `main`. The red that does is an overlapping box, or a box that meets the head.

The rest of route B in that dispatch matches this reading. Solver groups, not collision groups, so the narrow phase still finds the pairs. Groups follow the mode, and no collider handle changes. The change sits behind a switch, and with the switch off the law matches `main` bit for bit. The product run relayed with #128 has no warm-started contact between a driven body and a dynamic body across 10,000 quanta, so the golden `69a671f962665563` has no reason to move. The slice still confirms that by hash. The slice merges after #144. If the measured cost is wider than the removed driven–dynamic contacts, the dispatch already says the builder stops, and route A is a new dispatch.

## What this note did not do

The #128 replay was not run again. The product-scene contact count was not run again. `crate-eject.md` is in this private repository and is not on the public readouts snapshot. `docs/dispatch-114-drop-clearance.md` on the engine's `main` links the public path.
