FROM python:3.9
LABEL maintainer="lyabomyr@gmail.com"
RUN pip install --upgrade pip
WORKDIR /telegram_bot
COPY requirements.txt /telegram_bot/requirements.txt
ENV PYTHONPATH="$PWD/telegram_bot"
ENV PARKING_BOT_TOKEN="5983708480:AAGili-17GfvFR5MRO_PgnvqtOFWsGMqUIM"
ENV STATUS_BOT_TOKEN="5634197832:AAE56-whWU7J9fykrCUXl6uoteBUHt9pmfw"
RUN pip install --no-cache-dir --upgrade -r  /telegram_bot/requirements.txt
COPY booking-parking-place-918d6fcf7e75.json /telegram_bot/booking-parking-place-918d6fcf7e75.json
COPY parking_bot /telegram_bot/parking_bot
COPY config.py /telegram_bot/config.py
COPY cron.py /telegram_bot/cron.py
ENTRYPOINT ["python"]
CMD ["--version"]
