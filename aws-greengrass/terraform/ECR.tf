resource "aws_ecr_repository" "ecr_detector" {
  name                 = "thesis-detector"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

output "foo" {
  value = aws_ecr_repository.ecr_detector.repository_url
}
