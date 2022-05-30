resource "kubernetes_service" "inference-service" {
  metadata {
    name      = "inference-service"
  }
  spec {
    selector = {
      app = kubernetes_pod.inference.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
    type = "LoadBalancer"
  }
}

resource "kubernetes_service" "frontend-service" {
  metadata {
    name      = "frontend-service"
  }
  spec {
    selector = {
      App = kubernetes_pod.frontend.metadata.0.labels.App
    }
    port {
      port        = 8081
      target_port = 5000
    }
    type = "LoadBalancer"
  }
}

resource "kubernetes_service" "grafana" {
  metadata {
    name      = "grafana-service"
  }
  spec {
    selector = {
      "app.kubernetes.io/name" = "grafana"
    }
    port {
      port        = 3000
      target_port = 3000
    }
    type = "LoadBalancer"
  }
}

resource "kubernetes_service" "prom" {
  metadata {
    name      = "prom-service"
  }
  spec {
    selector = {
      "component" = "server"
    }
    port {
      port        = 9090
      target_port = 9090
    }
    type = "LoadBalancer"
  }
}

resource "kubernetes_pod" "frontend" {
  metadata {
    name      = "inference-frontend"
    labels = {
      App = "inference-frontend"
    }
  }

  spec {
    container {
      image = var.use_local_containers ? "nidhogg-frontend:latest" : "ghcr.io/fastjur/nidhogg-frontend:latest"
      name  = "inference-frontend"
      image_pull_policy = var.use_local_containers ? "Never" : "IfNotPresent"

      port {
        container_port = 5000
      }

    }
  }
}


resource "kubernetes_pod" "inference" {
  metadata {
    name      = "inference-backend"
    labels = {
      app = "inference-backend"
    }
    
    annotations = {
      "prometheus.io/scrape" = "true"
      "prometheus.io/port"   = "8080"
      "prometheus.io/path"   = "/metrics"
    }
  }

  spec {
    container {
      image = var.use_local_containers ? "nidhogg-inference:latest" : "ghcr.io/fastjur/nidhogg-inference:latest"
      name  = "inference-backend"
      image_pull_policy = var.use_local_containers ? "Never" : "IfNotPresent"

      port {
        container_port = 8080
      }
    }
  }
}