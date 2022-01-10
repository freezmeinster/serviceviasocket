normalbuild:
	@docker build --tag serveronsock .
buildx:
	@docker buildx build --platform linux/arm/v7,linux/arm64/v8,linux/amd64 --tag serveronsock .
run:
	@docker run --rm -it --name server -v /tmp/anu:/root/share/ serveronsock /root/share/socks.sock
