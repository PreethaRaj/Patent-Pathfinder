resource "kubernetes_config_map" "gpu_runtime" {
  metadata {
    name      = "innovation-gpu-runtime"
    namespace = kubernetes_namespace.innovation.metadata[0].name
  }

  data = {
    note = "Attach a GPU node pool and set nodeSelector/tolerations for the vLLM workload when enabling GPU mode."
  }
}
