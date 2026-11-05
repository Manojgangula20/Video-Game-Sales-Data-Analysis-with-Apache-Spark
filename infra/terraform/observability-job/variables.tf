
variable "git_repo_url" {
  description = "GitHub repository containing the Databricks notebooks."
  type        = string
  default     = "https://github.com/Manojgangula20/Video-Game-Sales-Data-Analysis-with-Apache-Spark-"
}

variable "git_branch" {
  description = "Git branch used by the Databricks job."
  type        = string
  default     = "main"
}
