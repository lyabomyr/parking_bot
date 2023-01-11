
build:
	docker build -f Dockerfile -t parking-tele-bot:latest .

build_push: build
	docker tag parking-tele-bot:latest lyabomyr/parking-tele-bot:latest; docker push lyabomyr/parking-tele-bot:latest
run:
	docker run --rm -it --entrypoint bash lyabomyr/parking-tele-bot:latest
createcluster:
	kind create cluster;\
	kubectl create namespace parkingbot
kubeapply:
	kubectl apply -f cron.yaml
	kubectl apply -f parking_bot.yaml 
kubestop:
	kubectl delete -f cron.yaml
	kubectl delete -f  parking_bot.yaml 


