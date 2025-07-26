
Kubernetes RBAC (Role-Based Access Control)

📌 What is RBAC?

**RBAC (Role-Based Access Control)** is a mechanism for controlling access to **Kubernetes resources** based on the **roles of individual users or service accounts**.

It allows you to define **who** can perform **what actions** on **which resources** in your Kubernetes cluster.

---

🎯 Why Do We Use RBAC?

| Purpose              |           Description                                                                         |
|----------------------|-----------------------------------------------------------------------------------------------|
| ✅ **Security**                   | Restricts access to prevent unauthorized actions like deleting pods or services.  |
| ✅ **Granular Control**           | Fine-tuned permissions (e.g., read-only access to pods in a specific namespace).  |
| ✅ **Separation of Duties**       | Different teams/users get permissions specific to their responsibilities.         |
| ✅ **Least Privilege Principle**  | Users are only granted the minimum permissions they need.                         |

---

⚙️ How RBAC Works in Kubernetes

RBAC is implemented via **four main resource types**:

1. `Role`
- Defines a **set of permissions** (verbs on resources) within a **specific namespace**.
- Example: Read-only access to pods in `dev` namespace.

2. `ClusterRole`
- Similar to `Role`, but **cluster-wide** or for **non-namespaced resources** (like nodes, persistent volumes, etc.).

3. `RoleBinding`
- Binds a `Role` to a user, group, or service account **within a namespace**.

4. `ClusterRoleBinding`
- Binds a `ClusterRole` to a user, group, or service account **across the entire cluster**.

---

📦 Example: Read-Only Access to Pods in `dev` Namespace

Step 1: Create a Role

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: dev
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
````

Step 2: Bind the Role to a User

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods-binding
  namespace: dev
subjects:
  - kind: User
    name: jane@example.com
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

> 🔐 This grants user `jane@example.com` read-only access to pods in the `dev` namespace.

---

 Additional Notes

* **Verbs** include: `get`, `list`, `watch`, `create`, `update`, `patch`, `delete`.
* **Resources** can be: `pods`, `services`, `deployments`, `secrets`, etc.
* You can also control access to **non-resource URLs** (like `/healthz` or `/metrics`) using RBAC.
* RBAC can apply to:

  * Human users
  * Service accounts (used by apps inside the cluster)
* **ClusterRole** can be used with **RoleBinding** to give cluster-wide roles only within a namespace (advanced use case).
* Kubernetes API server **enforces** RBAC checks before granting access to any resource.

---

Summary

> **RBAC in Kubernetes** is a powerful and flexible way to **secure your cluster** by managing **who can do what**. By using `Roles`, `ClusterRoles`, and their respective bindings, you can **enforce least privilege** and protect your workloads from unauthorized actions.
