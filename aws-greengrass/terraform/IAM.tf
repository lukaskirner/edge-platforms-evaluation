resource "aws_iam_role" "ggc_device_role" {
  name = "GreengrassV2DeviceRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "credentials.iot.amazonaws.com"
        }
      },
    ]
  })

  inline_policy {
    name = "ggc_device_inline_policy"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Resource = "*"
          Action = [
            "iot:DescribeCertificate",
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents",
            "logs:DescribeLogStreams",
            "iot:Connect",
            "iot:Publish",
            "iot:Subscribe",
            "iot:Receive",
            "s3:GetBucketLocation"
          ]
        },
        {
          Effect = "Allow"
          Resource = "*"
          Action = [
            "ecr:GetAuthorizationToken",
            "ecr:BatchGetImage",
            "ecr:GetDownloadUrlForLayer"
          ]
        },
        {
          Effect = "Allow"
          Resource = "${aws_s3_bucket.ggc_services.arn}/*"
          Action = [
            "s3:GetObject"
          ]
        },
      ]
    })
  }
}
