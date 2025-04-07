1. What is minikube ?

    - Minikube is a tool that allows developers to run a single-node Kubernetes cluster on their local machine, making it easy to learn, develop, and test Kubernetes applications without needing a full-fledged cloud environment. 

2. What is kubectl ?

    - kubectl is a command-line tool used to interact with and manage Kubernetes clusters.
    - It's the primary way to communicate with the Kubernetes API server to perform various operations on your Kubernetes resources, such as deployments, services, pods, namespaces, and more.

    Key Functions of kubectl:
    Cluster Management: 
        - You can use kubectl to manage and interact with Kubernetes clusters, view cluster information, and configure cluster settings.

    Resource Management: 
        - It allows you to create, update, delete, and manage resources like pods, deployments, services, replicasets, and more.

    Access Logs & Monitor: 
        - You can fetch logs, get real-time resource statuses, and monitor the performance of your Kubernetes workloads.

    Namespace Management: 
        - kubectl helps you manage resources within specific namespaces to isolate and organize different environments (like development, testing, production).

    Configuration and Deployment: 
        - It can be used to apply configuration files (YAML or JSON) to your cluster, enabling you to deploy and scale applications.


3. Here’s a list of `kubectl` commands organized from basic to advanced level.

---

Basic Level:

1. Get Kubernetes Cluster Info:
   
   kubectl cluster-info
   
   Shows the cluster's API server and other services’ endpoints.

2. Check Cluster Version:
   
   kubectl version
   
   Displays the Kubernetes client and server version.

3. Get Resources:
   - List all pods in the default namespace:
     
     kubectl get pods
     
   - List nodes in the cluster:
     
     kubectl get nodes
     
   - List services in the default namespace:
     
     kubectl get services
     
   - List all resources in the cluster:
     
     kubectl get all
     

4. Get Detailed Information About a Resource:
   - Describe a pod:
     
     kubectl describe pod <pod-name>
     

5. Check Logs for a Pod:
   - View logs of a specific pod:
     
     kubectl logs <pod-name>
     

6. Access a Pod’s Shell (For Debugging):
   - Open a bash shell inside a pod (if available):
     
     kubectl exec -it <pod-name> -- /bin/bash
     
   - Or open sh if the pod does not have bash:
     
     kubectl exec -it <pod-name> -- /bin/sh
     

---

Intermediate Level:

7. Create Resources (From YAML File):
   - Create resources defined in a YAML file:
     
     kubectl create -f <file>.yaml
     

8. Apply Configuration Changes (Create/Update):
   - Apply changes from a YAML configuration file:
     
     kubectl apply -f <file>.yaml
     

9. Delete Resources:
   - Delete a pod:
     
     kubectl delete pod <pod-name>
     
   - Delete resources using a YAML file:
     
     kubectl delete -f <file>.yaml
     

10. Scale a Deployment:
    - Scale a deployment to a specific number of replicas:
      
      kubectl scale deployment <deployment-name> --replicas=<number>
      

11. Get Events in the Cluster:
    - Show the latest events in the cluster:
      
      kubectl get events
      

12. Check Resource Usage:
    - Get the resource usage (CPU and memory) of pods:
      
      kubectl top pods
      
    - Get the resource usage of nodes:
      
      kubectl top nodes
      

13. Port Forward a Pod’s Port:
    - Forward a local port to a pod’s port (useful for accessing services locally):
      
      kubectl port-forward pod/<pod-name> <local-port>:<pod-port>
      

---

Advanced Level:

14. Describe Nodes:
    - Get detailed information about a node:
      
      kubectl describe node <node-name>
      

15. Get Detailed Logs from a Specific Container in a Pod:
    - Get logs from a specific container inside a pod:
      
      kubectl logs <pod-name> -c <container-name>
      

16. Use a Specific Namespace:
    - Set the namespace for your current session:
      
      kubectl config set-context --current --namespace=<namespace>
      
    - Get resources from a specific namespace:
      
      kubectl get pods -n <namespace>
      

17. Get Resources in YAML or JSON Format:
    - Display resources in YAML format:
      
      kubectl get pods -o yaml
      
    - Display resources in JSON format:
      
      kubectl get pods -o json
      

18. Export Resources to Files:
    - Export a resource’s configuration (e.g., pod) to a YAML file:
      
      kubectl get pod <pod-name> -o yaml > pod-config.yaml
      

19. Apply Resource Patches:
    - Apply a partial update or patch to a resource:
      
      kubectl patch deployment <deployment-name> -p '{"spec":{"replicas":3}}'
      

20. Roll Back to a Previous Deployment:
    - Roll back to a previous version of a deployment:
      
      kubectl rollout undo deployment/<deployment-name>
      

21. Get and Manage Contexts:
    - List all contexts available in your `kubectl` configuration:
      
      kubectl config get-contexts
      
    - Switch to a different context:
      
      kubectl config use-context <context-name>
      

22. Watch Resources in Real-Time:
    - Watch the status of resources in real-time:
      
      kubectl get pods --watch
      

23. Run Commands in a Pod:
    - Run an interactive command in a pod (e.g., start a shell):
      
      kubectl run -i --tty --rm busybox --image=busybox -- /bin/sh
      

24. Run a Pod in a Specific Namespace:
    - Run a pod in a specific namespace:
      
      kubectl run <pod-name> --image=<image-name> -n <namespace>
      

---

Expert Level:

25. Deploy Multiple Resources at Once:
    - Apply a set of YAML files to deploy multiple resources:
      
      kubectl apply -f <dir-containing-yamls>
      

26. Create Resources from a Template:
    - Create a resource using a template from the command line:
      
      kubectl run <name> --image=<image-name> --dry-run=client -o yaml > <file>.yaml
      

27. View Resource Usage Across All Namespaces:
    - View resource usage for all namespaces:
      
      kubectl top pods --all-namespaces
      

28. Set Resource Limits and Requests:
    - Apply CPU and memory limits/requests in a deployment YAML:
      yaml
      resources:
        requests:
          memory: "64Mi"
          cpu: "250m"
        limits:
          memory: "128Mi"
          cpu: "500m"
      
      You can apply this by running:
      
      kubectl apply -f <file>.yaml
      

29. Manage ConfigMaps and Secrets:
    - Get ConfigMap in a specific namespace:
      
      kubectl get configmap <configmap-name> -n <namespace>
      
    - Create a ConfigMap from a file:
      
      kubectl create configmap <configmap-name> --from-file=<file-path>
      
    - Get Secrets (Base64 encoded):
      
      kubectl get secret <secret-name> -o yaml
      

30. Run CronJobs:
    - Create a CronJob from a YAML file (for scheduled jobs):
      
      kubectl apply -f cronjob.yaml






