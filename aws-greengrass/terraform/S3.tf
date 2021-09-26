
resource "aws_s3_bucket" "ggc_services" {
  bucket = "de.inovex.lkirner.ggc.services"
  acl    = "private"
  force_destroy = true
}
