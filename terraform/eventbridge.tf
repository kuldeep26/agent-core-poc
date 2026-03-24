resource "aws_cloudwatch_event_rule" "daily_scan" {
  name                = "agent-daily-scan"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule = aws_cloudwatch_event_rule.daily_scan.name
  arn  = aws_lambda_function.agent_core.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.agent_core.function_name
  principal     = "events.amazonaws.com"
}