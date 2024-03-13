terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
}

provider "aws" {
  profile = "LabRole"
  region = "us-west-2"
}

resource "aws_ecr_repository" "spam-classifier-image" {
  name = "spam-classifier-image"
}
