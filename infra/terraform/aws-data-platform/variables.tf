variable "aws_region" {
  description = "AWS deployment region."
  type        = string
  default     = "ap-south-1"
}

variable "name_prefix" {
  description = "Prefix for project AWS resources."
  type        = string
  default     = "bms-databricks-platform"
}

variable "log_retention_days" {
  description = "CloudWatch log retention period."
  type        = number
  default     = 14
}

variable "tags" {
  description = "Additional resource tags."
  type        = map(string)
  default     = {}
}
