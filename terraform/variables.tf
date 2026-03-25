variable "region" {
  default = "us-east-1"
}

variable "teams_webhook" {
  description = "Microsoft Teams Webhook URL for notifications"
  type        = string
}


variable "foundation_model" {
  description = "Inference profile ID/ARN for the Bedrock model (required in regions where on-demand model IDs are unsupported)"
  type        = string
}
