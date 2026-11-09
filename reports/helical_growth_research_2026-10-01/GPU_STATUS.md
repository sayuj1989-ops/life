# GPU visibility snapshot

Read-only checks during this session on 2026-10-01 IST.
Commands were repeated outside the execution sandbox because its launcher failed
with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.

- `nvidia-smi`: **No devices were found**.
- `/proc/driver/nvidia/version`: NVIDIA UNIX Open Kernel Module for aarch64,
  version **580.178.04**, build dated 2026-07-07.
- `/proc/driver/nvidia/gpus/000f:01:00.0/information`: Model **Unknown**,
  GPU UUID **GPU-????????-????-????-????-????????????**, GPU Firmware **N/A**,
  PCIe Bus Location **000f:01:00.0**, Device Minor **0**, GPU Excluded **No**.
- NVIDIA device nodes `/dev/nvidia0`, `/dev/nvidiactl`, `/dev/nvidia-uvm` exist.
- `/proc/meminfo`: MemAvailable **106192268 kB**, approximately **101.27 GiB**;
  SwapFree **12586136 kB**. Available RAM does not establish a healthy GPU context.

**GPU health is not established.** A loaded kernel module and device nodes do not
prove enumeration or usable CUDA. These observations warrant separate driver/GPU
diagnosis before GPU work. They do not identify the cause: PCIe availability,
firmware initialization, driver state and kernel errors have not been resolved.
No CUDA test, GPU workload, driver reload, reboot or model-service restart was run.
This snapshot is point-in-time evidence and must be refreshed before future GPU work.
