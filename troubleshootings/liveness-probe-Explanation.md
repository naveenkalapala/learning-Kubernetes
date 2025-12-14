# Kubernetes LivenessProbe – Explanation & Troubleshooting  

## Overview

A **LivenessProbe** is a Kubernetes health-check that lets the kubelet know **whether a container is still alive**.  
If the probe fails, kubelet **kills the container** and restarts it according to the Pod’s `restartPolicy`.  
It is the “**circuit-breaker**” that recovers from dead-locked or corrupted processes.

---

## How LivenessProbe Works

1. Kubelet executes the probe **at configured intervals**.
2. On success → **nothing happens**, container keeps running.
3. On failure → container is **SIGKILL-ed** (`restartPolicy` decides what comes next).
4. Counter is **per-container**; restarting resets the probe state.

---

## Probe Types & Minimal Definitions

| Type   | Example Spec |
| ------ | ------------ |
| **exec** | `exec: { command: ["cat", "/tmp/healthy"] }` |
| **httpGet** | `httpGet: { path: /healthz, port: 8000 }` |
| **tcpSocket** | `tcpSocket: { port: 8080 }` |
| **gRPC** *(1.24+)* | `grpc: { service: mypackage.MyService, port: 9000 }` |

Common tunables (apply to all):
```yaml
initialDelaySeconds: 5   # wait before first probe
periodSeconds: 10        # how often to probe
timeoutSeconds: 1        # individual probe timeout
failureThreshold: 3      # consecutive fails before restart
successThreshold: 1      # min consecutive successes to be considered healthy
```

---

## Live Example Walk-Through

Below manifest creates a Pod that **simulates a crash after 30 s** and lets the **exec LivenessProbe** recover it.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: livenessprobe-deployment
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: livenessprobe
  template:
    metadata:
      labels:
        app: livenessprobe
    spec:
      containers:
      - name: livenessprobe-container
        image: nkalapala24/liveness-probe:v1
        args:
        - /bin/bash
        - -c
        - |
          touch /tmp/health
          sleep 30
          rm -f /tmp/health        # &lt;-- simulate deadlock / crash
          sleep 300
        livenessProbe:
          exec:
            command:
            - cat
            - /tmp/health          # file disappears ➜ probe fails
          initialDelaySeconds: 5
          periodSeconds: 10
          timeoutSeconds: 2
          failureThreshold: 2
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: livenessprobe-service
spec:
  selector:
    app: livenessprobe
  type: NodePort
  ports:
  - port: 8000
    targetPort: 8000
```

Deploy & watch:

```bash
kubectl apply -f deployment.yaml
kubectl get pods -w
# after ~40s you will see RESTARTS counter increment
kubectl describe pod &lt;name&gt; | grep -A 5 Liveness
```

Expected event:
```
Liveness probe failed: cat: /tmp/health: No such file or directory
Killing container with id docker://livenessprobe-container
```

---

## When to Use (and Not to Use) LivenessProbe

| Use-Cases ✅ | Anti-Patterns ❌ |
| ------------ | ---------------- |
| Deadlock detection (app stuck but JVM/RT still running) | Simple HTTP 500 during load (use **readiness**) |
| Background worker that must never stop | Expensive checks (DB scans, heavy CPU) |
| Self-healing without human intervention | Probe depends on external services (couples fate) |

&gt; **Rule of thumb:**  
&gt; Liveness = **“is this process alive?”**  
&gt; Readiness = **“can this pod serve traffic?”**

---

## Troubleshooting LivenessProbe Failures

1. **Describe Pod**
   ```bash
   kubectl describe pod &lt;pod-name&gt;
   ```
   Check `Events` section for probe failure reason.

2. **Check Logs**
   ```bash
   kubectl logs &lt;pod-name&gt; --previous   # logs of crashed container
   ```

3. **Simulate Probe Manually**
   ```bash
   kubectl exec &lt;pod-name&gt; -- cat /tmp/health   # exec probe
   kubectl exec &lt;pod-name&gt; -- wget -q -O- http://localhost:8000/healthz   # http probe
   ```

4. **Adjust Thresholds / Delays**  
   If container needs &gt;5 s to start, raise `initialDelaySeconds` or `failureThreshold`.

5. **Avoid Fork-Bombs**  
   Exec probes that run shell pipelines can leak processes; keep them single-binary.

---

## Common Pitfalls & Fixes

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| Pod restarts continuously | `initialDelaySeconds` too small | Increase delay |
| Probe never passes | Wrong port / path | Validate with `kubectl exec` |
| High CPU during startup | Probe runs too frequently | Increase `periodSeconds` |
| Network split brain | HTTP probe hits external LB | Probe localhost only |

---

## Key Takeaways

* LivenessProbe = **self-healing**; use only for **true dead-process** detection.
* Pick the **cheapest** probe type that proves liveness (exec &lt; http &lt; tcp).
* Always **tune delays** to your app start-up time.
* **Never** use liveness to check dependencies—use **readiness** instead.

---

## One-Line Summary

&gt; A LivenessProbe lets Kubernetes automatically **restart a container that is no longer alive**, recovering from deadlocks or corruption without manual intervention.