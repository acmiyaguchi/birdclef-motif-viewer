terraform {
  backend "gcs" {
    bucket = "birdclef-2022-tfstate"
    prefix = "birdclef-motif-viewer"
  }
}

locals {
  project_id = "birdclef-2022"
  region     = "us-central1"
  repo_name  = "birdclef-motif-viewer"
}

provider "google" {
  project = local.project_id
  region  = local.region
}

data "google_project" "project" {}

// A useful blog post: https://ruanmartinelli.com/posts/terraform-cloud-run
resource "google_project_service" "run" {
  service = "run.googleapis.com"
}

resource "google_project_service" "cloudbuild" {
  service = "cloudbuild.googleapis.com"
}

// necessary for manual triggering of builds
resource "google_project_service" "iam" {
  service = "iam.googleapis.com"
}

resource "google_container_registry" "registry" {
  location = "US"
}

// https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudbuild_trigger
// https://cloud.google.com/build/docs/configuring-builds/substitute-variable-values
// https://cloud.google.com/build/docs/cloud-build-service-account
// https://cloud.google.com/build/docs/securing-builds/store-manage-build-logs
resource "google_cloudbuild_trigger" "deploy-cloud-run" {
  github {
    name  = local.repo_name
    owner = "acmiyaguchi"
    push {
      branch       = "^main$"
      invert_regex = false
    }
  }
  substitutions = {
    _REGION = local.region
  }
  filename        = "cloudbuild.yaml"
  service_account = google_service_account.cloudbuild.id
  depends_on = [
    google_project_service.cloudbuild,
    google_project_iam_member.act-as,
    google_project_iam_member.logs-writer
  ]
}


resource "google_cloud_run_service" "default" {
  depends_on = [google_project_service.run]

  name                       = local.repo_name
  location                   = local.region
  autogenerate_revision_name = true

  template {
    spec {
      container_concurrency = 4
      containers {
        image = "gcr.io/${local.project_id}/${local.repo_name}:latest"
        env {
          # NOTE: circular dependencies, so this is a chicken and egg problem
          name  = "STATIC_EXTERNAL_HOST"
          value = "https://birdclef-motif-viewer-bx4w66axbq-uc.a.run.app"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "all-users" {
  service  = google_cloud_run_service.default.name
  location = google_cloud_run_service.default.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "service_url" {
  value = google_cloud_run_service.default.status[0].url
}
