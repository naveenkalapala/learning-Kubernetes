
# Kubernetes OOMKilled – Explanation & Troubleshooting

## Overview
`OOMKilled` (Out Of Memory Killed) is a container termination reason that occurs when a Pod **exceeds its memory limit** and the Linux **Out-Of-Memory (OOM) killer** terminates the process to protect the node. Kubernetes marks the container as `OOMKilled` and restarts it according to the Pod’s `restartPolicy`.

---

## How Memory Limits Work in Kubernetes

1. A **Deployment / Pod manifest** is applied with **memory requests** and **limits**.
2. The **Kubernetes scheduler** assigns the Pod to a node that has **sufficient allocatable memory**.
3. The **kubelet** configures the container runtime (**containerd / Docker / CRI-O**) to:
   - Set the **cgroup memory limit** to the value specified in the Pod spec.
4. If the container’s **resident memory (RSS)** exceeds the limit:
   - The **Linux OOM killer** sends **SIGKILL** to the process.
   - The container exits with **code 137** (128 + 9).
   - Kubernetes records the **reason: OOMKilled**.

---

## Pod State Transitions During OOM

```text
Running
  ↓
Memory usage rises
  ↓
OOMKilled (137)
  ↓
Restart (if restartPolicy: Always / OnFailure)
````

* **Running** – Container is healthy.
* **Memory spike** – Application allocates more than the limit.
* **OOMKilled** – Process is force-killed by the kernel.
* **Restart** – kubelet restarts the container (unless policy is `Never`).

---

## Why OOMKilled Happens

The container can be killed for several memory-related reasons:

### 1. Memory Limit Too Low

* Application’s **normal workload** needs more memory than the limit.
* Sudden **traffic spike** increases allocations.

### 2. Memory Leak

* Application **retains objects** without releasing them (e.g., caches, global variables).
* Memory usage **grows indefinitely** until it hits the limit.

### 3. Incorrect Unit / Typo

* Using `Mi` instead of `Gi` (or vice versa).
* Decimal typo (`100Mi` vs `1000Mi`).

### 4. Sidecar Container Memory

* Sidecars (istio-proxy, logging agents, etc.) **share the Pod’s memory limit** if no separate limits are set.

### 5. JVM / .NET / Node Apps

* Runtime **heap size** is **larger than the cgroup limit**.
* JVM: `-Xmx` > container memory limit.
  - **Fix**: use `-XX:MaxRAMPercentage=75.0` instead of fixed `-Xmx`.

### 6. Burstable vs Guaranteed QoS

* **Burstable** Pods can be **throttled or killed** earlier under node pressure.
* **Guaranteed** Pods (requests == limits) are **last to be evicted**.

---

## Why the Exit Code is 137

| Code | Meaning                        |
| ---- | ------------------------------ |
| 128  | Exited due to signal           |
| +9   | SIGKILL (force kill)           |
| =137 | OOMKilled by kernel            |

> **Note:**  
> `OOMKilled` is **not** a Kubernetes decision—it is the **Linux kernel’s OOM killer**.

---

## Requests vs Limits vs OOM

| Memory Setting | Purpose                                | Triggers OOMKilled |
| -------------- | -------------------------------------- | ------------------ |
| `requests`     | Scheduling & initial cgroup soft limit | ❌ No               |
| `limits`       | Hard cgroup limit                      | ✅ Yes              |

---

## How to Troubleshoot OOMKilled

### 1. Describe the Pod (Check Reason)

```bash
kubectl describe pod <pod-name>
```

Look for:

```
Last State:     Terminated
Reason:         OOMKilled
Exit Code:      137
```

---

### 2. Check Container Metrics

#### a. **kubectl top**
```bash
kubectl top pod <pod-name> --containers
```

#### b. **Metrics Server / Prometheus**
- Memory usage trend
- Spike pattern

#### c. **Container Memory Working Set**
- Prometheus query:
  ```
  container_memory_working_set_bytes{pod="<pod-name>"}
  ```

---

### 3. Check Application Logs (Memory Leak Clues)

```bash
kubectl logs <pod-name> --previous
```

Look for:

* OutOfMemoryError (Java)
* Allocation failures
* Heap dumps

---

### 4. Inspect Memory Inside Container (Live)

```bash
kubectl exec -it <pod-name> -- /bin/bash
# inside container
cat /sys/fs/cgroup/memory/memory.limit_in_bytes
cat /sys/fs/cgroup/memory/memory.usage_in_bytes
free -m
top
```

---

### 5. Increase Memory Limit (Quick Fix)

```yaml
resources:
  limits:
    memory: "1Gi"        # bump from 512Mi
  requests:
    memory: "512Mi"
```

Apply and monitor.

---

## Key Takeaways

* `OOMKilled` means **container exceeded its memory limit** and was **force-killed by the kernel**.
* Exit code **137** is the signature.
* Always check:
  * `kubectl describe pod` → reason
  * Memory **usage vs limit** → metrics
  * Application **heap settings** → runtime flags
* **Fix**: raise limit, fix leak, or tune runtime.

---

## Summary (One-Line Explanation)

> `OOMKilled` occurs when a container’s memory usage exceeds its cgroup limit and the Linux Out-Of-Memory killer terminates the process with SIGKILL (exit code 137).
````