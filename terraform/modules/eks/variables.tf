variable "name" {
  description = "EKS cluster and ECR repository prefix."
  type        = string
  default     = "qlaudops"
}

variable "region" {
  description = "AWS region for the example resources."
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "Existing VPC ID; this module does not create networking."
  type        = string
}

variable "private_subnet_ids" {
  description = "Existing private subnet IDs in at least two availability zones."
  type        = list(string)
  validation {
    condition     = length(var.private_subnet_ids) >= 2
    error_message = "Provide at least two private subnet IDs for EKS availability."
  }
}

variable "cluster_version" {
  description = "Kubernetes version supported by the selected EKS region."
  type        = string
  default     = "1.31"
}
