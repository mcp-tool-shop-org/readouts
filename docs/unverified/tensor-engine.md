# Unverified — tensor-engine-knowledge
`verified=0` engines (**59** of 193; verified=1 **134**; waves **17**). Do not invent verified flips.
STUDY-068 refresh from DB. Do not set verified=1. Do not invent STUDY-071.

| id | wave | slug | name | url | claim | flag |
|----|------|------|------|-----|-------|------|
| 12 | 1 | `mlc-llm` | MLC-LLM | https://github.com/mlc-ai/mlc-llm | MLC-LLM is a universal LLM deployment engine with ML compilation, Apache-2.0, s… | verified=0; status=situational; note=verdict=unverified \\| currency=unknown \\| fixes: Version v0… |
| 143 | 4 | `bytefit` | bytefit | https://github.com/mcp-tool-shop-org/bytefit | Hardware-aware local-LLM loadout planner (probe/recommend/plan); MIT; v1.0.0; t… | verified=0; status=recommended |
| 145 | 15 | `consumer-blackwell-local-llm-guide` | Private LLM Inference on Consumer Blackwell (guide paper) | https://arxiv.org/abs/2601.09527 | consumer Blackwell local guide | verified=0; status=situational |
| 146 | 15 | `bench360-local-llm` | Bench360 — multi-axis local LLM inference bench | https://arxiv.org/abs/2511.16682 | Bench360 multi-axis honesty | verified=0; status=situational |
| 147 | 15 | `spectre-speculative-serving` | SPECTRE — hybrid speculative serving | https://arxiv.org/abs/2605.08151 | SPECTRE speculative serving | verified=0; status=situational |
| 148 | 15 | `turboquant` | TurboQuant — online vector quantization | https://arxiv.org/abs/2504.19874 | TurboQuant | verified=0; status=situational |
| 149 | 15 | `polarquant` | PolarQuant — polar KV cache quant | https://arxiv.org/abs/2502.02617 | PolarQuant | verified=0; status=situational |
| 150 | 15 | `fireq` | FireQ — INT4-FP8 kernel + RoPE-aware PTQ | https://arxiv.org/abs/2505.20839 | FireQ | verified=0; status=situational |
| 151 | 15 | `attn-qat` | Attn-QAT — 4-bit attention QAT | https://arxiv.org/abs/2603.00040 | Attn-QAT | verified=0; status=situational |
| 152 | 15 | `spec-cpu-runrules-analog` | SPEC CPU runrules — disclosure analog | https://www.spec.org/cpu2026/Docs/runrules.html | SPEC disclosure | verified=0; status=situational |
| 153 | 15 | `google-benchmark-warmup-analog` | Google Benchmark — warm-up method analog | https://google.github.io/benchmark/user_guide.html | MinWarmUpTime | verified=0; status=situational |
| 154 | 15 | `k8s-resourcequota-refuse-analog` | K8s ResourceQuota — capacity refuse analog | https://kubernetes.io/docs/concepts/policy/resource-quotas/ | ResourceQuota | verified=0; status=situational |
| 155 | 15 | `cgroup-v2-memory-max-analog` | cgroup v2 memory.max — hard ceiling analog | https://docs.kernel.org/admin-guide/cgroup-v2.html | memory.max | verified=0; status=situational |
| 156 | 15 | `fio-odirect-analog` | fio — O_DIRECT honest I/O measure analog | https://fio.readthedocs.io/ | fio O_DIRECT | verified=0; status=situational |
| 157 | 15 | `mlc-llm-install-docs` | MLC LLM install docs — CUDA 12.8/13 wheels | https://llm.mlc.ai/docs/install/mlc_llm.html | MLC install | verified=0; status=situational |
| 158 | 16 | `tvm-compiler-paper-1802` | TVM: An Automated End-to-End Optimizing Compiler for Deep Learning | https://arxiv.org/abs/1802.04799 | TVM end-to-end DL compiler | verified=0; status=situational |
| 159 | 16 | `autotvm-paper-1805` | Learning to Optimize Tensor Programs (AutoTVM) | https://arxiv.org/abs/1805.08166 | AutoTVM learned cost-model search | verified=0; status=situational |
| 160 | 16 | `ansor-paper-2006` | Ansor: Generating High-Performance Tensor Programs for Deep Learning | https://arxiv.org/abs/2006.06762 | Ansor hierarchical tensor-program search | verified=0; status=situational |
| 161 | 16 | `tensorir-paper-2207` | TensorIR: An Abstraction for Automatic Tensorized Program Optimization | https://arxiv.org/abs/2207.04296 | TensorIR block-based IR | verified=0; status=situational |
| 162 | 16 | `metaschedule-paper-2205` | Tensor Program Optimization with Probabilistic Programs (MetaSchedule) | https://arxiv.org/abs/2205.13603 | MetaSchedule probabilistic search | verified=0; status=situational |
| 163 | 16 | `relax-paper-2311` | Relax: Composable Abstractions for End-to-End Dynamic Machine Learning | https://arxiv.org/abs/2311.02103 | Relax IR symbolic shapes | verified=0; status=situational |
| 164 | 16 | `match-tvm-paper-2410` | MATCH: Model-Aware TVM-based Compilation for Heterogeneous Edge Devices | https://arxiv.org/abs/2410.08855 | MATCH hardware cost-model DSE | verified=0; status=situational |
| 165 | 16 | `vortex-paper-2409` | Vortex: Sample-Free Dynamic Tensor Program Optimization | https://arxiv.org/abs/2409.01075 | Vortex hardware-aware strategy spaces | verified=0; status=situational |
| 166 | 16 | `mlc-compile-models-analog-039` | MLC Compile Model Libraries (hold) | https://llm.mlc.ai/docs/compilation/compile_models.html | convert_weight→gen_config→compile→deploy | verified=0; status=situational |
| 167 | 16 | `mlc-install-tvm-analog-039` | MLC Install TVM Compiler (hold) | https://llm.mlc.ai/docs/install/tvm.html | TVM toolchain prerequisite before serve | verified=0; status=situational |
| 168 | 16 | `mlc-llm-readme-currency-039` | MLC LLM README (currency) | https://github.com/mlc-ai/mlc-llm | Apache-2.0 cross-backend compile+serve | verified=0; status=situational |
| 169 | 16 | `mlc-llm-pip-wheels-039` | MLC LLM pip install wheels (CUDA 12.8/13) | https://llm.mlc.ai/docs/install/mlc_llm.html | prebuilt nightly wheels CUDA 12.8/13.0 | verified=0; status=situational |
| 170 | 16 | `mlc-llm-quickstart-039` | MLC LLM Quick Start (no tok/s) | https://llm.mlc.ai/docs/get_started/quick_start.html | MLCEngine Llama-3-8B q4 ≥6GB VRAM note | verified=0; status=situational |
| 171 | 16 | `mlc-llm-intro-compile-039` | MLC LLM Introduction compile path | https://llm.mlc.ai/docs/get_started/introduction.html | gen_config→convert_weight→compile→serve | verified=0; status=situational |
| 172 | 16 | `mlc-llm-rest-api-039` | MLC LLM REST API | https://llm.mlc.ai/docs/deploy/rest.html | OpenAI-shaped /v1/chat/completions | verified=0; status=situational |
| 173 | 16 | `mlc-llm-tags-currency-039` | mlc-llm tags v0.19/v0.20 (Releases thin) | https://api.github.com/repos/mlc-ai/mlc-llm/tags | tags v0.19.0 v0.20.0; Releases only v0.1.dev0 | verified=0; status=situational |
| 174 | 16 | `bytefit-readme-currency-039` | bytefit README (probe/plan anti-paging) | https://github.com/mcp-tool-shop-org/bytefit | MIT probe/recommend/plan; refuses paging | verified=0; status=situational |
| 175 | 16 | `bytefit-spec-v100-039` | bytefit SPEC v1.0.0 CHANGELOG | https://raw.githubusercontent.com/mcp-tool-shop-org/bytefit/main/SPEC.md | advisor not estimator; anti-paging admission | verified=0; status=situational |
| 176 | 16 | `spec-cpu-runrules-analog-039` | SPEC CPU Run and Reporting Rules (hold) | https://www.spec.org/cpu2026/Docs/runrules.html | disclosed conditions or label estimates | verified=0; status=situational |
| 177 | 16 | `gbench-warmup-analog-039` | Google Benchmark MinWarmUpTime (hold) | https://google.github.io/benchmark/user_guide.html | discard cold iterations; report steady state | verified=0; status=situational |
| 178 | 16 | `k8s-resourcequota-analog-039` | Kubernetes ResourceQuota (hold) | https://kubernetes.io/docs/concepts/policy/resource-quotas/ | over-quota → 403 not silent overcommit | verified=0; status=situational |
| 179 | 16 | `cgroup-v2-memory-max-analog-039` | cgroup v2 memory.max (hold) | https://docs.kernel.org/admin-guide/cgroup-v2.html | hard ceiling refuses; soft high throttles | verified=0; status=situational |
| 180 | 17 | `local-llm-apple-silicon-comparative-060` | Production-Grade Local LLM Inference on Apple Silicon: A Comparative Study of M… | https://arxiv.org/abs/2511.05502 | comparative incl. MLC-LLM; no invent tok/s | verified=0; status=situational |
| 181 | 17 | `webllm-paper-060` | WebLLM: A High-Performance In-Browser LLM Inference Engine | https://arxiv.org/abs/2412.15803 | in-browser MLC-class compile-serve | verified=0; status=situational |
| 182 | 17 | `sglang-paper-060` | SGLang: Efficient Execution of Structured Language Model Programs | https://arxiv.org/abs/2312.07104 | structured LLM program runtime | verified=0; status=situational |
| 183 | 17 | `mlc-compile-models-060` | MLC Compile Model Libraries | https://llm.mlc.ai/docs/compilation/compile_models.html | convert→gen_config→compile; JIT; memory knobs | verified=0; status=situational |
| 184 | 17 | `mlc-convert-weights-060` | MLC Convert Model Weights | https://llm.mlc.ai/docs/compilation/convert_weights.html | HF→MLC quant; tensor-cache | verified=0; status=situational |
| 185 | 17 | `mlc-cli-chat-060` | MLC CLI (mlc_llm chat) | https://llm.mlc.ai/docs/deploy/cli.html | /stats meter surface; no invent rates | verified=0; status=situational |
| 186 | 17 | `mlc-python-engine-060` | MLC Python API / Engine Mode | https://llm.mlc.ai/docs/deploy/python_engine.html | concurrency↔KV↔GPU memory trade | verified=0; status=situational |
| 187 | 17 | `mlc-package-libs-060` | MLC Package Libraries and Weights | https://llm.mlc.ai/docs/compilation/package_libraries_and_weights.html | package/JIT cache | verified=0; status=situational |
| 188 | 17 | `bytefit-changelog-060` | bytefit CHANGELOG 1.0.0 | https://raw.githubusercontent.com/mcp-tool-shop-org/bytefit/main/CHANGELOG.md | anti-paging refuse; their 5090 notes ≠ invent studio tok/s | verified=0; status=situational |
| 189 | 17 | `bytefit-spec-admission-060` | bytefit SPEC §4–§6 admission | https://raw.githubusercontent.com/mcp-tool-shop-org/bytefit/main/SPEC.md | Refuse, don't page; do not flip 143 | verified=0; status=situational |
| 190 | 17 | `bytefit-readme-refuse-060` | bytefit README refuse claim | https://raw.githubusercontent.com/mcp-tool-shop-org/bytefit/main/README.md | probe/recommend/plan; sample UI rates ≠ invent | verified=0; status=situational |
| 191 | 17 | `tvm-quant-analysis-060` | Analyzing Quantization in TVM | https://arxiv.org/abs/2308.10905 | TVM quant survey | verified=0; status=situational |
| 192 | 17 | `halo-hw-quant-060` | HALO: Hardware-aware quantization with low critical-path-delay weights for LLM … | https://arxiv.org/abs/2502.19662 | HW-aware quant; adjacent bytefit | verified=0; status=situational |
| 193 | 17 | `flashinfer-paper-060` | FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Servi… | https://arxiv.org/abs/2501.01005 | attention kernels for LLM serve | verified=0; status=situational |
| 194 | 17 | `kernelband-paper-060` | KernelBand: Steering LLM-based Kernel Optimization via Hardware-Aware Multi-Arm… | https://arxiv.org/abs/2511.18868 | HW-aware bandit kernel search | verified=0; status=situational |
| 195 | 17 | `pruner-paper-060` | Pruner: A Draft-then-Verify Exploration Mechanism to Accelerate Tensor Program … | https://arxiv.org/abs/2402.02361 | draft-then-verify tensor-program tuning | verified=0; status=situational |
| 196 | 17 | `mlc-compile-then-run-analog-060` | Compile Model Libraries (hold) | https://llm.mlc.ai/docs/compilation/compile_models.html | hold compile-then-run | verified=0; status=situational |
| 197 | 17 | `nix-hermetic-build-analog-060` | How Nix Works (hold) | https://nixos.org/guides/how-nix-works/ | hold hermetic build-then-run | verified=0; status=situational |
| 198 | 17 | `bytefit-spec-antipaging-analog-060` | bytefit SPEC anti-paging (hold) | https://raw.githubusercontent.com/mcp-tool-shop-org/bytefit/main/SPEC.md | hold anti-paging refuse | verified=0; status=situational |
| 199 | 17 | `k8s-resourcequota-analog-060` | Kubernetes ResourceQuota (hold) | https://kubernetes.io/docs/concepts/policy/resource-quotas/ | hold capacity refuse | verified=0; status=situational |
| 200 | 17 | `cgroup-v2-memory-max-analog-060` | cgroup v2 memory.max (hold) | https://docs.kernel.org/admin-guide/cgroup-v2.html | hold hard ceiling admit | verified=0; status=situational |
| 201 | 17 | `fio-odirect-analog-060` | fio direct / O_DIRECT (hold) | https://fio.readthedocs.io/en/latest/fio_doc.html | hold honest measure | verified=0; status=situational |

