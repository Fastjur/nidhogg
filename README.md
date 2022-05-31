
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

## Linting the python code
To lint the python code, you should run the `linter.sh` script.
This requires you to have installed the `requirements.txt` file.

## Additions

- Template code from: https://github.com/mengdong/python-ml-structure

Get started:
- `python3 ./src/run.py --preprocess`
- `python3 ./src/run.py --train`
- `python3 ./src/run.py --serve`

Build and run the HTTP server container:
- `docker build -t nidhogg-http-server http_server`
- `docker run -it -p 8080:8080 nidhogg-http-server`
