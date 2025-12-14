
# CrashLoopBackOff in Kubernetes

## What is CrashLoopBackOff?

`CrashLoopBackOff` occurs when a container **starts successfully but repeatedly crashes**, and Kubernetes **restarts it with increasing delay (exponential backoff)** between attempts.

---

## Pod Lifecycle Leading to CrashLoopBackOff

1. A Deployment manifest is applied.
2. The **API Server** stores the desired state in etcd.
3. The **Scheduler** assigns the Pod to a node.
4. The **kubelet** on the node:

   * Pulls the container image
   * Creates the container
   * Starts the container

### Outcomes:

* ✅ If the container runs successfully → Pod phase is `Running`
* ❌ If the container starts but crashes → restart cycle begins

---

## Common Causes of Container Crashes

* **Application errors** (exceptions, misconfigured arguments)
* **OOMKilled** (container exceeds memory limits)
* **Liveness probe failures**
* **Invalid command / entrypoint**
* Missing environment variables or config files

> ⚠️ **Note:**
> `readinessProbe` failures do **not** restart containers.
> They only mark the Pod as *NotReady* and stop traffic.

---

## Why “CrashLoop”?

The container:

1. Starts
2. Crashes
3. Gets restarted by kubelet
4. Crashes again

This continuous crash–restart cycle forms the **CrashLoop**.

---

## Why “BackOff”?

Kubernetes applies an **exponential backoff delay** between restart attempts to avoid resource exhaustion.

Example:

```
Restart → fail → wait
Restart → fail → wait longer
Restart → fail → wait even longer
```

During this time, the container state shows:

```
State: Waiting
Reason: CrashLoopBackOff
```

> 📌 The Pod phase usually remains `Running`.

---

## Restart Policy Behaviour

* Deployments / ReplicaSets use:

  ```yaml
  restartPolicy: Always
  ```
* kubelet **must restart** the container after every crash
* This leads to CrashLoopBackOff when failures persist

---

## How to Troubleshoot CrashLoopBackOff

### 1. Describe the Pod

```bash
kubectl describe pod <pod-name>
```

Check:

* Exit codes
* `Last State`
* OOMKilled messages
* Probe failures

---

### 2. Check Previous Container Logs (Most Important)

```bash
kubectl logs <pod-name> --previous
```

---

### 3. View Events (Chronological)

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

## Key Takeaway

> **CrashLoopBackOff means the image pulled successfully, the container started, but the application inside keeps crashing. Kubernetes retries with increasing delay.**

