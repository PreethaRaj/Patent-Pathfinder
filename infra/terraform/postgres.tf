resource "kubernetes_namespace" "innovation" {
  metadata {
    name = "innovation"
  }
}

resource "kubernetes_secret" "app_env" {
  metadata {
    name      = "innovation-app-secrets"
    namespace = kubernetes_namespace.innovation.metadata[0].name
  }

  data = {
    JWT_SECRET = "change-me"
  }

  type = "Opaque"
}
