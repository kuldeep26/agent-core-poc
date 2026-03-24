data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "../lambda_agent"
  output_path = "../lambda.zip"
}

resource "aws_lambda_function" "agent_core" {
  function_name = "agent-core-platform"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  timeout       = 900

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
  variables = {
    TEAMS_WEBHOOK = var.teams_webhook
    AGENT_ID      = aws_bedrockagent_agent.platform_agent.id
    AGENT_ALIAS_ID = "TSTALIASID"
    }
  }
}