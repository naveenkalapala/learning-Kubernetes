
# Kubernetes Scheduling: NodeSelector, NodeAffinity, Taints & Tolerations

This document explains how Kubernetes decides **where to schedule Pods** using:
- NodeSelector
- NodeAffinity
- Taints
- Tolerations

These concepts are critical for **production-grade clusters**, workload isolation, and controlled scheduling.

---

## 1. NodeSelector

### What is NodeSelector?
`nodeSelector` is the **simplest way** to constrain Pods to run only on nodes with specific labels.

- It matches **node labels**, not node names
- It is a **hard requirement**
- If no node matches → Pod stays in `Pending` state

### How it works
1. Add a label to the node
2. Define `nodeSelector` in the Pod spec
3. Scheduler matches labels exactly

### Example

```yaml
spec:
  nodeSelector:
    node-type: arm
````

The Pod will only schedule on nodes with:

```bash
node-type=arm
```

### Common Use Cases

* ARM vs AMD architecture
* GPU workloads
* High-memory / high-IO nodes
* Dedicated application nodes

### Key Limitation

* Supports **only exact match**
* No logical operators (`In`, `NotIn`, etc.)

---

## 2. Node Affinity

### What is Node Affinity?

NodeAffinity is a **more expressive and flexible** alternative to NodeSelector.

It allows:

* Logical operators
* Soft and hard scheduling rules

---

### Types of Node Affinity

#### 2.1 RequiredDuringSchedulingIgnoredDuringExecution (Hard Rule)

* Pod **must** be scheduled on matching nodes
* If no match exists → Pod remains `Pending`

```yaml
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node-type
                    operator: In
                    values:
                      - arm
```

---

#### 2.2 PreferredDuringSchedulingIgnoredDuringExecution (Soft Rule)

* Scheduler **tries** to match preferred nodes
* If no match → schedules on other nodes

```yaml
    spec:
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 1
              preference:
                matchExpressions:
                  - key: node-type
                    operator: In
                    values:
                      - arm
```

---

### Supported Operators

* `In`
* `NotIn`
* `Exists`
* `DoesNotExist`
* `Gt`, `Lt`

---

### NodeSelector vs NodeAffinity

| Feature     | NodeSelector | NodeAffinity |
| ----------- | ------------ | ------------ |
| Match Type  | Exact        | Logical      |
| Soft Rules  | ❌            | ✅            |
| Operators   | ❌            | ✅            |
| Flexibility | Low          | High         |

---

## 3. Taints

### What are Taints?

Taints are applied to **nodes** to **repel Pods** unless Pods explicitly tolerate them.

> "Do not schedule Pods here unless they tolerate me."

### Taint Format

```bash
kubectl taint nodes <node-name> key=value:effect

kubectl taint nodes <node-name> key1=value1:NoSchedule
kubectl taint nodes <node-name> key1=value1:NoExecute

```

### Taint Effects

| Effect             | Description                    |
| ------------------ | ------------------------------ |
| `NoSchedule`       | New Pods will not be scheduled |
| `PreferNoSchedule` | Scheduler tries to avoid       |
| `NoExecute`        | Existing Pods are evicted      |

---

### Common Use Cases

* Dedicated nodes (DB, GPU, monitoring)
* Control-plane isolation
* Node maintenance / upgrades
* Preventing noisy neighbor issues

---

## 4. Tolerations

### What are Tolerations?

Tolerations are defined on **Pods** and allow them to be scheduled on **tainted nodes**.

> Tolerations do NOT force scheduling — they only **allow** it.

---

### Matching Rules

A Pod can tolerate a taint only if:

* `key` matches
* `effect` matches
* Operator logic matches

---

### Operators

| Operator | Meaning                        |
| -------- | ------------------------------ |
| `Exists` | Key must exist (value ignored) |
| `Equal`  | Key and value must match       |

---

### Example

#### Node Taint

```bash
kubectl taint node node1 key1=value1:NoSchedule
```

#### Pod Toleration

```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoSchedule"
```

---> Pod **can** be scheduled on `node1`

---

## 5. Drain vs Taints (Important Difference)

### `kubectl drain`

* Used during node upgrades
* Evicts Pods safely
* Respects PodDisruptionBudgets (PDB)
* Temporarily marks node as unschedulable

### Taints

* Manual and persistent
* Used for long-term scheduling control
* Require tolerations to bypass

---

## 6. Mental Model 

* **NodeSelector / NodeAffinity** →
  *Where should my Pod go?*

* **Taints / Tolerations** →
  *Where should my Pod NOT go unless explicitly allowed?*

---

## 7. Production Best Practices

* Prefer **NodeAffinity** over NodeSelector
* Use **Taints** for dedicated workloads
* Always document taints and tolerations
* Avoid overusing hard constraints
* Combine with **Resource Requests & Limits**

---

## Summary

* NodeSelector → Simple, hard match
* NodeAffinity → Flexible, expressive scheduling
* Taints → Repel Pods from nodes
* Tolerations → Allow Pods onto tainted nodes
* Scheduler uses all of these together to make decisions

---

📌 This knowledge is critical for **scalable, secure, and predictable Kubernetes clusters**.
