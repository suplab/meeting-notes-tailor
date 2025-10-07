output "alb_dns_name" {
  value       = aws_lb.app.dns_name
  description = "Application Load Balancer DNS name"
}

output "ecr_repo_url" {
  value = aws_ecr_repository.repo.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.meeting_cluster.name
}
