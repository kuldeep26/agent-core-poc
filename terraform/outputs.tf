output "lambda_name" {
  value = aws_lambda_function.agent_core.function_name
}

output "bedrock_agent_id" {
  value = aws_bedrockagent_agent.platform_agent.id
}

output "bedrock_agent_alias_id" {
  value = aws_bedrockagent_agent_alias.platform_agent_alias.agent_alias_id
}
