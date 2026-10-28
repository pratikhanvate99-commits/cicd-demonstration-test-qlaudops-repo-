output "cluster_name" {
  value       = module.platform.cluster_name
  description = "EKS cluster name (plan only until explicitly applied)."
}

output "ecr_repository_url" {
  value       = module.platform.ecr_repository_url
  description = "Private image registry URL."
}
