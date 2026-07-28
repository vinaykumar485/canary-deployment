# canary-deployment


install of rollout and rollout controler ( similer to deployment and deployment controler )

    Step 1: Create the namespace
        kubectl create namespace argo-rollouts

Verify:

    kubectl get ns

You should now see:

    argo-rollouts


Step 2: Install Argo Rollouts

Run:

    kubectl apply -n argo-rollouts \
    -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml


This downloads the official installation manifest from the Argo Rollouts project and creates all the required Kubernetes resources.



Step 3: Wait for the controller

    kubectl get pods -n argo-rollouts -w

Wait until you see something like:

NAME                              READY   STATUS
argo-rollouts-xxxxxxxxxx-xxxxx     1/1     Running


Then verify everything

Run these commands one by one:

    kubectl get all -n argo-rollouts
    kubectl get sa -n argo-rollouts
    kubectl get clusterrole | grep argo
    kubectl get clusterrolebinding | grep argo
    kubectl get crd | grep argoproj
    kubectl api-resources | grep rollout


Verfication:

    kubectl get all -n argo-rollouts

    kubectl get crd | grep argoproj


--------------------------------------------------------------------------------------------------------------------------------------------------

application deployment:
______________________


part 1:

1. create app.py, dockerfile,rollout,yaml stable-service.yaml. canary-service.yaml
2. cret docker image and push to ecr with tag.
3. apply rollout.yaml file with the newimage name
4. Argo Rollouts Controller sees

 Image

    ↓

It creates

ReplicaSet

     & 
it cretes a pod A and pod B

5. NOW APPLY THE STABLE-SERVICE.YAML AND CANARY-SERVICE.YAML 
6. This crete STABLE-service will select the pod A and pod B  and the canaru-service do not have the end point or pod now.
4. create ingress which is poing to stable-service
5. access the app using load labcer - it is point to stable servce endpoint "Everything is Version 1." 

part 2: 

6. edit docker file for v2, also app.py file and index.html
7. build the new v2 image tag and ush to ecr
8. update the rollout.yaml file with new image
9. apply rollout.yaml ifle, and then it will cret the pod -c
10. At this moment, Pod C is running, but no user traffic is reaching it yet, Because the Ingress still routes everything to stable-service.



At this point:


                    Browser

                       │

                       ▼

             AWS Load Balancer

                       │

                       ▼

          NGINX Ingress Controller

                       │

                       ▼

                stable-service

                 /           \

             Pod A         Pod B



canary-service

      │

      ▼

    Pod C



Pod C is running and healthy, but it is not receiving user traffic yet, because the Ingress still forwards requests only to stable-service.

part 3: 

so, after apply -f rollout.yaml file the new pod -c is creted , and this is monitored by the rollout controler , thos chnages is updated in live ingress inside the api server
but not the ingress.yaml file in local machine. 

once it notice the chnage and udate the live ingrees in API server , now ingress will come to know that , it (ingress ) need to send 20% trafic to new pod -c 

part 4 : then , when you run promt , it makes 50% trafic to flow to pod -c 

part 5: then , when you run promt , it makes 80% trafic to flow to pod -c 

part 6: then , when you run promt , it makes 100% trafic to flow to pod -c 

part 7 : all trafic will be going to pod - c and no trafic to pod A and pod B , SO pod a and pod b will run for some time and then get terminated and now pod -c will become the stable service endpoint and  there is no canary anymore.

The rollout is finished.

The canary pod has become the stable pod


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

final workflow

        		   BROWSER
                      │

               AWS Load Balancer

                      │

                      ▼

              NGINX Ingress

                      │

         ┌────────────┴────────────┐

         │                         │

        80%                      20%

         │                         │

         ▼                         ▼

 stable-service             canary-service

         │                         │

    Pod A   Pod B               Pod C




------------------------------------------------------------------------------------------------------------------------------------



BASIC ARCHITECTURE FOR CANARY DEPLOYMENT

    Internet
         │
         ▼
    AWS ELB
         │
         ▼
NGINX Ingress Controller
         │
         ▼
    Ingress
         │
 ┌───┴───────────┐
 ▼               ▼
Stable Service   Canary Service
 │               │
 ▼_______________▼
         |
    Argo rollout     
         |
ArogoRollout controler
  |              |
  |              |
Stable RS      Canary RS
 │               │
 ▼               ▼
V1             V2




--------------------------------------------------------------------------------------------------------------------------------------

