variable "region" {
  default = "us-east-1"
}

variable "teams_webhook" {
    description = "Microsoft Teams Webhook URL for notifications"
    type        = string
    default     = "update_teams_webhook_url_manually in lambda environment variables"
}
