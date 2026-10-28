output "cluster_name" {
  description = "EKS control plane name."
  value       = aws_eks_cluster.this.name
}

output "cluster_arn" {
  description = "EKS cluster ARN."
  value       = aws_eks_cluster.this.arn
}

output "ecr_repository_url" {
  description = "Private ECR repository URL."
  value       = aws_ecr_repository.this.repository_url
}
