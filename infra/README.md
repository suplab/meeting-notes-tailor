# Terraform infra for meeting-notes-tailor


This folder contains Terraform configurations to provision a minimal
AWS environment to run the meeting-notes-tailor FastAPI container on ECS Fargate
behind an Application Load Balancer (ALB). It also creates an ECR repository
and an optional Secrets Manager secret for the OpenAI API key.

IMPORTANT:
- Review and set variables before running `terraform apply`.
- Build and push your container image to ECR (or set `ecr_image_uri` variable).


