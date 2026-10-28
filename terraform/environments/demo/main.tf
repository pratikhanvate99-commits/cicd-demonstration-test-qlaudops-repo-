provider "aws" {
  region = var.region
  default_tags { tags = { Project = "QlaudOps", ManagedBy = "Terraform" } }
}

module "platform" {
  source             = "../../modules/eks"
  name               = var.name
  region             = var.region
  vpc_id             = var.vpc_id
  private_subnet_ids = var.private_subnet_ids
  cluster_version    = var.cluster_version
}
