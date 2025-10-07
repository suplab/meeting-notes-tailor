variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "meeting-notes-tailor"
}

variable "ecr_image_uri" {
  description = "ECR image URI for the container (provide: <account>.dkr.ecr.<region>.amazonaws.com/repo:tag)"
  type        = string
  default     = ""
}

variable "openai_api_key" {
  description = "(Optional) OpenAI API key to store in Secrets Manager via terraform input"
  type        = string
  default     = ""
  sensitive   = true
}
