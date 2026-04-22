resource "kubernetes_config_map" "search_runtime" {
  metadata {
    name      = "innovation-search-runtime"
    namespace = kubernetes_namespace.innovation.metadata[0].name
  }

  data = {
    OPENSEARCH_URL = "http://opensearch:9200"
    NEO4J_URL      = "bolt://neo4j:7687"
  }
}
