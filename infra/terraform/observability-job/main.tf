
resource "databricks_job" "observability" {
  name        = "Video Game Sales - Platform Observability"
  description = "Runs platform health monitoring, Delta history inspection, data quality monitoring and alert evaluation."

  git_source {
    url      = var.git_repo_url
    branch   = var.git_branch
    provider = "gitHub"
  }

  task {
    task_key = "platform_observability"

    notebook_task {
      notebook_path = "notebooks/06_platform_observability"
      source        = "GIT"
    }

    max_retries                 = 1
    min_retry_interval_millis   = 60000
    timeout_seconds             = 3600
  }

  max_concurrent_runs = 1

  tags = {
    project     = "video-game-sales-platform"
    environment = "portfolio"
    managed_by  = "terraform"
    component   = "observability"
  }
}
