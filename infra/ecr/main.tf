resource "aws_ecr_repository" "repo" {
  name                 = "${var.project_name}"
  image_scanning_configuration { scan_on_push = true }
  tags = { Name = var.project_name }
}

output "ecr_repo_url" {
  value = aws_ecr_repository.repo.repository_url
}
