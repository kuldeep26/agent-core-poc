terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "abc-us-east-1-terraform-state-bucket"
    key            = "agent-core/terraform.tfstate"
  }
}

provider "aws" {
  region = var.region
}