FROM python:3.10.9
RUN mkdir /weather_bot
WORKDIR /weather_bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]
