normalbuild:
	@docker build --tag freezmeinster/serveronsock .
buildx:
	@docker buildx build --platform linux/arm/v7,linux/arm64/v8,linux/amd64 --tag freezmeinster/serveronsock .
buildnpush:
	@docker buildx build --push --platform linux/arm/v7,linux/arm64/v8,linux/amd64 --tag freezmeinster/serveronsock .
run:
	@docker run --rm -it --name server -v /tmp/anu:/root/share/ freezmeinster/serveronsock /root/share/socks.sock
