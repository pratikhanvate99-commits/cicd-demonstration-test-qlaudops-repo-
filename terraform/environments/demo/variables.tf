variable "name" {
  description = "Prefix for billable AWS resource names."
  type        = string
  default     = "qlaudops-demo"
}

variable "region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "Existing VPC ID. No VPC is created by this example."
  type        = string
  default     = "vpc-00000000000000000"
}

variable "private_subnet_ids" {
  description = "Existing private subnets in separate availability zones."
  type        = list(string)
  default     = ["subnet-00000000000000000", "subnet-11111111111111111"]
}

variable "cluster_version" {
  description = "EKS Kubernetes version."
  type        = string
  default     = "1.31"
}
