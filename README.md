[![Train model, build containers and create a new version tag](https://github.com/Fastjur/nidhogg/actions/workflows/build.yaml/badge.svg)](https://github.com/Fastjur/nidhogg/actions/workflows/build.yaml)
[![Code Scanning - Security Analysis Action](https://github.com/Fastjur/nidhogg/actions/workflows/codeQL.yaml/badge.svg)](https://github.com/Fastjur/nidhogg/actions/workflows/codeQL.yaml)
[![Run tests](https://github.com/Fastjur/nidhogg/actions/workflows/test.yaml/badge.svg)](https://github.com/Fastjur/nidhogg/actions/workflows/test.yaml)
[![Run mllint](https://github.com/Fastjur/nidhogg/actions/workflows/linter.yaml/badge.svg)](https://github.com/Fastjur/nidhogg/actions/workflows/linter.yaml)

## How to run locally
Make sure you have installed [minikube](https://minikube.sigs.k8s.io/docs/start/), [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/), [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) and [docker](https://www.docker.com/).

```
minikube start
```

### Building local image
Note that if you want to run your local images, you need to have installed [dvc](https://dvc.org/) and execute the following commands.
```
eval $(minikube docker-env)
python3 -m venv venv # Only if you have not already created a venv directory!
source venv/bin/activate
pip install -r requirements.txt
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

## Testing out github actions locally using act
You can test out the github actions locally using the `act` tool.
1. Install the `act` tool: https://github.com/nektos/act
2. Create a Personal Access Token: https://github.com/settings/tokens/new and make sure it has the `repo`, `read:user`, `read:email` and `write:discussions` scopes.
3. Save this token in a `act.secrets` file as: `GITHUB_TOKEN=<your token>`.
4. Then you can test out actions using act, see their page for more instructions.
   You have to include the secrets file using `act --secret-file act.secrets <any other options or commands>`

## Additions

- Template code from: https://github.com/mengdong/python-ml-structure

Get started:
- `python3 ./src/run.py --preprocess`
- `python3 ./src/run.py --train`
- `python3 ./src/run.py --serve`

Build and run the HTTP server container:
- `docker build -t nidhogg-http-server http_server`
- `docker run -it -p 8080:8080 nidhogg-http-server`
