Argo Rollouts Canary Deployment - Complete Steps

Phase 1 - Install Argo Rollouts Controller (One-time setup)
Install CRDs and Controller

    kubectl create namespace argo-rollouts

    kubectl apply -n argo-rollouts \
    -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

Verify:

    kubectl get pods -n argo-rollouts

Expected:

argo-rollouts-xxxxxxxxx-xxxxx   Running
_______________________________________________________________________________________________________________________________________

Install kubectl plugin

Linux:


    curl -LO https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-linux-amd64


    chmod +x kubectl-argo-rollouts-linux-amd64


    sudo mv kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts


Verify:

    kubectl argo rollouts version

____________________________________________________________________________________________________________________________________________

Phase 2 - Install NGINX Ingress Controller (One-time setup)


    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

    helm repo update

    helm install ingress-nginx ingress-nginx/ingress-nginx \
    -n ingress-nginx \
    --create-namespace

Verify:

    kubectl get pods -n ingress-nginx

    kubectl get svc -n ingress-nginx

Note the EXTERNAL-IP or LoadBalancer DNS.
________________________________________________________________________________________________________________________________________________

Phase 3 - Build Version 1

    cd app

    docker build -t canary-demo:v1 .

Tag:

    docker tag canary-demo:v1 \
    273263084701.dkr.ecr.us-east-1.amazonaws.com/canary-demo:v1

Push:

    docker push \
    273263084701.dkr.ecr.us-east-1.amazonaws.com/canary-demo:v1
__________________________________________________________________________________________________________________________________________________

Phase 4 - Deploy Version 1
    kubectl apply -f manifests/

________________________________________________________________________________________________________________________________________________

Phase 5 - Verify Deployment

Rollout

    kubectl get rollout -n canary-deployment

Pods

    kubectl get pods -n canary-deployment

ReplicaSets

    kubectl get rs -n canary-deployment

Services

    kubectl get svc -n canary-deployment

Ingress

    kubectl get ingress -n canary-deployment

Open the application:

    http://<LOAD_BALANCER_DNS>

You should see:

    Version 1

_____________________________________________________________________________________________________________________________________

Phase 6 - Build Version 2

    Modify the application. index.html file for "APP VERSION : V2"

Build:

    docker build -t canary-demo:v2 .

Tag:

    docker tag canary-demo:v2 \
    273263084701.dkr.ecr.us-east-1.amazonaws.com/canary-demo:v2

Push:

    docker push \
    273263084701.dkr.ecr.us-east-1.amazonaws.com/canary-demo:v2

+______________________________________________________________________________________________________________________________________

Phase 7 - Update Rollout

Update only the image:

    image: 273263084701.dkr.ecr.us-east-1.amazonaws.com/canary-demo:v2

Apply:

    kubectl apply -f manifests/rollout.yaml
_________________________________________________________________________________________________________________________________________

Phase 8 - Watch the Rollout

Terminal 1

    kubectl argo rollouts get rollout canary-demo \
    -n canary-deployment --watch

Terminal 2

    watch -n1 kubectl get pods -n canary-deployment -o wide

Terminal 3

    watch -n1 kubectl get rs -n canary-deployment

Terminal 4

    watch -n1 kubectl get svc -n canary-deployment

Browser

    Refresh the application repeatedly.

Expected:

    Mostly Version 1

    Sometimes Version 2

because:

Weight = 20%
Phase 9 - Verify the Rollout

Detailed rollout:

    kubectl argo rollouts get rollout canary-demo -n canary-deployment

Describe rollout:

    kubectl describe rollout canary-demo -n canary-deployment

ReplicaSets:

    kubectl get rs -n canary-deployment

Pods:

    kubectl get pods -n canary-deployment -o wide

Services:

    kubectl get svc -n canary-deployment

Ingress:

    kubectl get ingress -n canary-deployment

Stable Service selector:

    kubectl get svc stable-service -n canary-deployment -o yaml

Canary Service selector:

    kubectl get svc canary-service -n canary-deployment -o yaml

___________________________________________________________________________________________________________________________________

Phase 10 - Promote

    kubectl argo rollouts promote canary-demo \
    -n canary-deployment

Watch again:

    kubectl argo rollouts get rollout canary-demo \
    -n canary-deployment --watch

Expected:

    Weight

    20%

    ↓

    50%

    ↓

    100%

__________________________________________________________________________________________________________________________________

Phase 11 - Final Verification

Pods

    kubectl get pods -n canary-deployment

ReplicaSets

    kubectl get rs -n canary-deployment

Rollout

    kubectl get rollout -n canary-deployment

Detailed rollout

    kubectl argo rollouts get rollout canary-demo \
    -n canary-deployment

Refresh browser.

Expected:

    Version 2

Every request

___________________________________________________________________________________________________________________________________


Useful Troubleshooting Commands

Logs

kubectl logs <pod-name> -n canary-deployment

Describe Pod

kubectl describe pod <pod-name> -n canary-deployment

Events

kubectl get events -n canary-deployment --sort-by=.metadata.creationTimestamp

ReplicaSets

kubectl describe rs <replicaset-name> -n canary-deployment

Rollout

kubectl describe rollout canary-demo -n canary-deployment
Rollback (Production)

View history:

kubectl argo rollouts history rollout canary-demo -n canary-deployment

Undo to a previous revision:

kubectl argo rollouts undo rollout canary-demo \
-n canary-deployment \
--to-revision=<revision-number>



____________________________________________________________________________________________________________________________________

Complete Flow


Developer
    │
    ▼
Build Docker Image
    │
    ▼
Push Image to ECR
    │
    ▼
Update rollout.yaml
    │
    ▼
kubectl apply
    │
    ▼
API Server
    │
    ▼
etcd
    │
    ▼
Argo Rollouts Controller
    │
    ▼
Create New ReplicaSet
    │
    ▼
ReplicaSet Controller
    │
    ▼
Create Canary Pod
    │
    ▼
Scheduler
    │
    ▼
Worker Node
    │
    ▼
Kubelet
    │
    ▼
Pod Ready
    │
    ▼
EndpointSlice Updated
    │
    ▼
NGINX Ingress
    │
    ▼
20% Traffic → Canary
80% Traffic → Stable
    │
    ▼
Verify
    │
    ▼
Promote
    │
    ▼
100% Traffic → New Version
    │
    ▼
Old ReplicaSet Scaled Down
