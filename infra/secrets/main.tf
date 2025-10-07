resource "aws_secretsmanager_secret" "openai" {
  name = "${var.project_name}-openai-key"
  description = "OpenAI API key for meeting-notes-tailor (optional)"
}

resource "aws_secretsmanager_secret_version" "openai_version" {
  secret_id     = aws_secretsmanager_secret.openai.id
  secret_string = var.openai_api_key
  depends_on     = [aws_secretsmanager_secret.openai]
}
