
build:
	docker build -f Dockerfile -t parking-tele-bot:latest .

build_push: build
	docker tag parking-tele-bot:latest lyabomyr/parking-tele-bot:latest; docker push lyabomyr/parking-tele-bot:latest
run:
	docker run --rm -it --entrypoint bash lyabomyr/parking-tele-bot:latest
