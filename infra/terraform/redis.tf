resource "kubernetes_config_map" "redis_runtime" {
  metadata {
    name      = "innovation-redis-runtime"
    namespace = kubernetes_namespace.innovation.metadata[0].name
  }

  data = {
    REDIS_URL = "redis://redis:6379/0"
  }
}
