1. What is kubernetes ?

- K8s, is an open-source platform designed to automate the deployment, scaling, and management of containerized applications.
- Kubernetes provides a framework for running distributed systems resiliently, allowing you to scale applications up or down based on      demand, manage resources efficiently, and ensure high availability.

2. Why Do We Need Kubernetes?

- Containers (e.g., Docker) revolutionized how we package and deploy applications by making them portable, lightweight, and consistent across environments. However, when you have dozens, hundreds, or thousands of containers running across multiple machines, managing them manually becomes a nightmare. 

- Here’s where the need for Kubernetes arises:
 
    - Scalability: 
    Applications often face fluctuating demand. Manually adding or removing containers to handle traffic spikes or lulls is inefficient and error-prone.

    - Reliability: 
    Containers can crash, servers can fail, and networks can glitch. You need a system to detect failures and recover automatically.

    - Resource Efficiency:
    Without orchestration, you might over-provision or under-utilize resources (CPU, memory), wasting money or degrading performance.

    - Deployment Complexity: 
    Rolling out updates, rollbacks, or managing dependencies across many containers and servers is chaotic without automation.

    - Portability: 
    Organizations want to run apps across on-premises servers, public clouds, or hybrid setups without rewriting everything.

    - Team Collaboration: 
    As development teams grow, coordinating deployments and ensuring consistency across dev, test, and production environments gets messy.

3. What Does Kubernetes Do?

Kubernetes acts as an orchestration layer that automates and manages the lifecycle of containerized applications. 
 - Here’s what it does, step-by-step:
    
    - Container Orchestration:
        - Groups containers into pods and deploys them across a cluster of machines (nodes).
        - Ensures the right number of pods are running based on your defined requirements (e.g., “I want 5 instances of this app”).

    - Auto-Scaling:
        - Horizontally scales pods up or down based on demand (e.g., CPU usage or custom metrics).
        - Vertically adjusts resources allocated to containers if needed.

    - Self-Healing:
        - Automatically restarts failed containers or pods.
        - Replaces crashed pods and reschedules them to healthy nodes.
        - Kills and recreates pods that don’t pass health checks.

    - Load Balancing:
        - Distributes network traffic across multiple pods to prevent overloading any single instance.
        - Provides a stable endpoint (via Services) for accessing your app, even as pods come and go.

    - Deployment Management:
        - Handles rolling updates (e.g., updating an app to a new version without downtime).
        - Supports rollbacks if something goes wrong.
        - Manages configuration and secrets (like API keys) securely.

    - Resource Optimization:
        - Allocates CPU, memory, and storage efficiently across your cluster.
        - Prevents resource contention by setting limits and requests for each container.

    - Service Discovery and Networking:
        - Assigns internal DNS names or IP addresses to pods so they can communicate.
        - Exposes applications to the outside world via ingress controllers or load balancers.
    
    - Storage Orchestration:
        - Attaches persistent storage to containers (e.g., cloud volumes or local disks) and manages it as pods move between nodes.

Real-World Example :

- Imagine you’re running an e-commerce site. Traffic spikes during a sale, some servers crash, and you need to roll out a new feature. -Without Kubernetes:
- You’d manually spin up more containers, pray they don’t crash, and hope your update doesn’t break everything. 
- With Kubernetes:
- It auto-scales your app during the sale, restarts failed containers, and deploys the update seamlessly while keeping the site live.

Kubernetes takes the grunt work out of managing containers, letting developers focus on coding and businesses focus on delivering value. It’s like having a tireless sysadmin who never sleeps.



4. Kubernetes Architecture :
    
    - Cluster
        - A Kubernetes cluster consists of a set of machines (either physical or virtual) that run containerized applications. 
        The cluster has two main components:
        
        - Control Plane: 
            The control plane is responsible for managing the state of the Kubernetes cluster, making decisions about the deployment and scheduling of applications, and maintaining the overall health of the cluster.

            Node(s): 
            Machines that run the containerized applications. Each node runs a container runtime (like Docker), along with the    necessary Kubernetes components.

    - The main components of the control plane are:

        API Server (kube-apiserver):
            - The central point of contact for all interactions with the cluster. It exposes the Kubernetes API and serves as the gateway  for all communication between other components (both internal and external)
            - It ensures the cluster’s desired state is met and handles requests like creating, deleting, or updating resources.

        Controller Manager (kube-controller-manager):
            - A collection of controllers that keep the cluster in the desired state. For example, the ReplicaSet controller ensures the right number of pod replicas are running.

        Scheduler (kube-scheduler): 
            - This component watches for newly created pods that have no node assigned and selects a suitable node for them to run on
            - It considers factors like resource requirements, affinity rules, and available resources on nodes.

        etcd:
            - A highly-available key-value store used for storing all cluster data, including the configuration data and the state of the system.
            - It holds all configuration data, state, and metadata (e.g., how many pods should run).

        Cloud Controller Manager:
            - Manages integration with cloud provider APIs, allowing Kubernetes to work with cloud services like networking, storage, and load balancing in cloud environments.
    - Nodes:
        - Nodes are the physical or virtual machines that run the workloads (containers). 
        There are two types of nodes in a Kubernetes cluster:

        - Master Node: 
            - The node that runs the control plane components (API server, scheduler, controller manager). It manages the cluster state and decision-making.

        - Worker Node: 
            - These nodes run the application workloads (containers). They host the container runtime (e.g., Docker or containerd) and the necessary components to manage the containerized apps.

            - Each node has a few critical components:
                - Kubelet:
                 An agent that runs on every node in the cluster. It ensures that containers are running in a Pod as expected and communicates with the API server to report the node’s status.
                - Kube Proxy:
                 Ensures network connectivity to Pods and manages the routing of network traffic between Pods. It runs on each node and is responsible for implementing the service abstraction, ensuring that traffic is properly forwarded to the correct Pod.
                - Container Runtime:
                 The software responsible for running containers (Docker, containerd, etc.). It interacts with the kubelet to ensure that containers are started, stopped, and run on the worker nodes as needed.
    - Pods:
       - A Pod is the smallest deployable unit in Kubernetes and can hold one or more containers
       - Pods share the same network namespace (IP address and port space), storage volumes, and other resources.
       - Pods are ephemeral, meaning they can be created and destroyed dynamically based on the desired state of the system.
       - Kubernetes automatically handles the scaling and placement of pods across nodes to ensure the application’s health.

    - Services:
        - A service is a logical abstraction that defines a set of pods and provides a stable endpoint (IP and port) for accessing those pods. Services can be of different types, such as ClusterIP (internal), NodePort (external), and LoadBalancer (external).

    - Namespaces:
        - Namespaces provide a way to divide cluster resources between multiple users or teams. It is useful for managing large clusters and organizing resources.

    - Ingress & Ingress Controller
        - An ingress is a set of rules that allows external HTTP and HTTPS traffic to reach services within the cluster.
        - The ingress controller is the component that processes ingress rules and routes traffic to the appropriate services.

    - Volumes:
        - Kubernetes volumes provide persistent storage for containers.
        - They allow data to persist across container restarts.

    - ConfigMap:
        - A ConfigMap is a Kubernetes resource used to store non-sensitive configuration data in key-value pairs. 
        - ConfigMaps allow you to separate configuration data from application code, making it easier to manage and modify configuration without needing to rebuild or redeploy containers.
        - Store application settings (e.g., database URLs, feature flags, environment variables).

    - Secret:
        - A Secret is a Kubernetes resource used to store sensitive data such as passwords, API keys, OAuth tokens, or TLS certificates. 
        - Secrets are similar to ConfigMaps but are intended for storing sensitive information. 
        - By storing sensitive data in Secrets, Kubernetes helps ensure that the information is not exposed in plaintext and is handled with more security.

    - Statefulset:
        - A StatefulSet is a Kubernetes controller designed to manage stateful applications. 
        - StatefulSets are used to manage applications that require stable, unique network identities and persistent storage across pod restarts.
        - Stateful applications are those that maintain their state between restarts, and they often require persistent storage (like databases or message queues) to function properly. Examples of stateful applications include databases like MySQL, MongoDB, or Redis.

    


Arechitecture of K8s:


                            +----------------------------+
                            |        Control Plane       |
                            |                            |
                            |   +--------------------+   |
                            |   | Kube-apiserver      |  |
                            |   +--------------------+   |
                            |   | Kube-controller     |  |
                            |   | manager             |  |
                            |   +--------------------+   |
                            |   | Kube-scheduler      |  |
                            |   +--------------------+   |
                            |   | etcd (Storage)      |  |
                            |   +--------------------+   |
                            +----------------------------+
                                |       |       |
                     +------------------+-----------------+
                     |                  |                 |
         +-------------------+   +-------------------+    +-------------------+
         |  Worker Node 1     |   |  Worker Node 2     |    |  Worker Node 3     |
         |                   |   |                   |    |                   |
         |  +-------------+  |   |  +-------------+  |    |  +-------------+  |
         |  | Kubelet     |  |   |  | Kubelet     |  |    |  | Kubelet     |  |
         |  +-------------+  |   |  +-------------+  |    |  +-------------+  |
         |  | Kube-proxy  |  |   |  | Kube-proxy  |  |    |  | Kube-proxy  |  |
         |  +-------------+  |   |  +-------------+  |    |  +-------------+  |
         |  | Container    |  |   |  | Container    |  |    |  | Container    |  |
         |  | Runtime      |  |   |  | Runtime      |  |    |  | Runtime      |  |
         |  +-------------+  |   |  +-------------+  |    |  +-------------+  |
         +-------------------+   +-------------------+    +-------------------+

