variable "region" {
  default = "us-east-1"
}

variable "teams_webhook" {
  description = "Microsoft Teams Webhook URL for notifications"
  type        = string
  default     = "https://outlook.office.com/webhook/your-webhook-url"
}


variable "foundation_model" {
  description = "Foundation model ID or inference profile ARN used by the Bedrock agent"
  type        = string
  default     = "anthropic.claude-3-5-sonnet-20241022-v2:0"
}
