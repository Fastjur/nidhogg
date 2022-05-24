# Multilabel classification on Stack Overflow tags
Predict tags for posts from StackOverflow with multilabel classification approach.

## Dataset
- Dataset of post titles from StackOverflow

## Transforming text to a vector
- Transformed text data to numeric vectors using bag-of-words and TF-IDF.

## MultiLabel classifier
[MultiLabelBinarizer](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html) to transform labels in a binary form and the prediction will be a mask of 0s and 1s.

[Logistic Regression](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) for Multilabel classification
- Coefficient = 10
- L2-regularization technique

## Evaluation
Results evaluated using several classification metrics:
- [Accuracy](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)
- [F1-score](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)
- [Area under ROC-curve](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html)
- [Area under precision-recall curve](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html#sklearn.metrics.average_precision_score)

## Libraries
- [Numpy](http://www.numpy.org/) — a package for scientific computing.
- [Pandas](https://pandas.pydata.org/) — a library providing high-performance, easy-to-use data structures and data analysis tools for the Python
- [scikit-learn](http://scikit-learn.org/stable/index.html) — a tool for data mining and data analysis.
- [NLTK](http://www.nltk.org/) — a platform to work with natural language.

Note: this sample project was originally created by @partoftheorigin

## Terraform
All the terraform files should be stored in the `terraform` folder.
If you want to use the terraform cli tool, you should first `cd terraform` to navigate to the terraform folder.

## Additions

- Template code from: https://github.com/mengdong/python-ml-structure

Get started:
- `python3 ./src/run.py --preprocess`
- `python3 ./src/run.py --train`
- `python3 ./src/run.py --serve`

Build and run the HTTP server container:
- `docker build -t nidhogg-http-server http_server`
- `docker run -it -p 8080:8080 nidhogg-http-server`

## How to run locally
Make sure you have installed [minikube](https://minikube.sigs.k8s.io/docs/start/) and [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and [docker](https://www.docker.com/).

```
minikube start
```

```
minikube dashboard
```

```
cd terraform
terraform init
terraform apply
```

```
minikube tunnel
```