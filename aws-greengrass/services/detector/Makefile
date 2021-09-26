build:
	docker buildx build --platform linux/arm64/v8 -t registry.inovex.de:4567/lkirner/edge-platforms-evaluation/aws/detector:latest --push .

ecr:
	aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 661407315395.dkr.ecr.eu-central-1.amazonaws.com
	docker buildx build --platform linux/arm64/v8 -t 661407315395.dkr.ecr.eu-central-1.amazonaws.com/thesis-detector:latest --push .
