resource "kubernetes_persistent_volume" "airflow_dags" {
  metadata {
    name = "openmetadata-dependencies-dags-pv"
    labels = {
      app = "airflow-dags"
    }
  }
  spec {
    capacity = {
      storage = "10Gi"
    }
    access_modes                     = ["ReadWriteMany"]
    persistent_volume_reclaim_policy = "Retain"
    storage_class_name               = "efs-sc"
    persistent_volume_source {
      csi {
        driver        = "efs.csi.aws.com"
        volume_handle = "${module.efs.id}::${module.efs.access_points["airflow_dags"].id}"
      }
    }
  }
}

resource "kubernetes_persistent_volume" "airflow_logs" {
  metadata {
    name = "openmetadata-dependencies-logs-pv"
    labels = {
      app = "airflow-logs"
    }
  }
  spec {
    capacity = {
      storage = "10Gi"
    }
    access_modes                     = ["ReadWriteMany"]
    persistent_volume_reclaim_policy = "Retain"
    storage_class_name               = "efs-sc"
    persistent_volume_source {
      csi {
        driver        = "efs.csi.aws.com"
        volume_handle = "${module.efs.id}::${module.efs.access_points["airflow_logs"].id}"
      }
    }
  }
}
