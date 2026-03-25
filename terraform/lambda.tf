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
    }
  }
}

resource "aws_lambda_permission" "allow_bedrock" {
  statement_id  = "AllowBedrockInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.agent_core.function_name
  principal     = "bedrock.amazonaws.com"
  source_arn    = aws_bedrockagent_agent.platform_agent.arn
}
