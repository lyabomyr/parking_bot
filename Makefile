
build:
	docker build -f Dockerfile -t parking-tele-bot:latest .

build_push: build
	docker tag parking-tele-bot:latest lyabomyr/parking-tele-bot:latest; docker push lyabomyr/parking-tele-bot:latest
run:
	docker run --rm -it --entrypoint bash lyabomyr/parking-tele-bot:latest
createcluster:
	kind create cluster
	kubectl create namespace parkingbot
kubeapply:
	kubectl apply -f cron.yaml
	kubectl apply -f parking_bot.yaml 
kubestop:
	kubectl delete -f cron.yaml

local_run:
	python3 -m venv en
	source en/bin/activate
	export BOT_TOKEN=5983708480:AAGili-17GfvFR5MRO_PgnvqtOFWsGMqUIM
	export  PYTHONPATH=$PWD
	pip install -r requirements.txt
	pip uninstall telebot
	pip uninstall pyTelegramBotApi
	pip install pyTelegramBotApi
	python3 parking_bot/parking_tele_bot.py 

