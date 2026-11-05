
output "observability_job_id" {
  description = "Databricks observability job ID."
  value       = databricks_job.observability.id
}

output "observability_job_url" {
  description = "Databricks observability job URL."
  value       = databricks_job.observability.url
}
