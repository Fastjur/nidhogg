resource "kubernetes_service" "example" {
  metadata {
    name      = "backend-service"
    namespace = "prod"
  }
  spec {
    selector = {
      app = kubernetes_pod.example.metadata.0.labels.app
    }
    session_affinity = "ClientIP"
    port {
      port        = 8080
      target_port = 8080
    }
    type = "LoadBalancer"
  }
}

resource "kubernetes_pod" "frontend" {
  metadata {
    name      = "inference-frontend"
    namespace = "prod"
    labels = {
      App = "inference-frontend"
    }
  }

  spec {
    container {
      image = "ghcr.io/fastjur/frontend:latest"
      name  = "inference-frontend"

      env {
        name  = "environment"
        value = "prod"
      }

      port {
        container_port = 8080
      }

    }

    # dns_config {
    #   nameservers = ["1.1.1.1", "8.8.8.8", "9.9.9.9"]
    #   searches    = ["example.com"]

    #   option {
    #     name  = "ndots"
    #     value = 1
    #   }

    #   option {
    #     name = "use-vc"
    #   }
    # }

    # dns_policy = "None"
  }
}


resource "kubernetes_pod" "example" {
  metadata {
    name      = "inference-backend"
    namespace = "prod"
    labels = {
      app = "inference-backend"
    }
  }

  spec {
    container {
      image = "ghcr.io/fastjur/inference:latest"
      name  = "inference-backend"

      env {
        name  = "environment"
        value = "prod"
      }

      port {
        container_port = 8080
      }
    }

    # dns_config {
    #   nameservers = ["1.1.1.1", "8.8.8.8", "9.9.9.9"]
    #   searches    = ["example.com"]

    #   option {
    #     name  = "ndots"
    #     value = 1
    #   }

    #   option {
    #     name = "use-vc"
    #   }
    # }

    # dns_policy = "None"
  }
}