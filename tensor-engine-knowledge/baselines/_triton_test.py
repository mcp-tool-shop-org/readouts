import torch, triton
import triton.language as tl

@triton.jit
def add_kernel(x_ptr, y_ptr, o_ptr, n, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offs < n
    tl.store(o_ptr + offs, tl.load(x_ptr + offs, mask=mask) + tl.load(y_ptr + offs, mask=mask), mask=mask)

x = torch.randn(4096, device="cuda")
y = torch.randn(4096, device="cuda")
o = torch.empty_like(x)
add_kernel[(4,)](x, y, o, 4096, BLOCK=1024)
torch.cuda.synchronize()
print("TRITON JIT OK — max abs err:", (o - (x + y)).abs().max().item())
