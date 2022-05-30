
## How to run locally
Make sure you have installed [minikube](https://minikube.sigs.k8s.io/docs/start/), [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/), [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) and [docker](https://www.docker.com/).

```
minikube start
```

### Building local image
Note that if you want to run your local images, you need to execute the following commands.
```
eval $(minikube docker-env)
dvc repro
```

```
minikube dashboard
```

```
cd terraform
terraform init
terraform apply -var="use_local_containers=true"
```

```
minikube tunnel
```