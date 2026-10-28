terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  # For production, configure an encrypted, versioned S3 backend and locking.
  # Keep state out of this repository and apply from an approved deployment role.
}
