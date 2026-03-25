variable "region" {
  default = "us-east-1"
}

variable "teams_webhook" {
  description = "Microsoft Teams Webhook URL for notifications"
  type        = string
  default = "https://outlook.office.com/webhook/your-webhook-url"
}
