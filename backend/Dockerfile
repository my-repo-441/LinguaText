FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y ffmpeg  # ffmpeg に含まれる ffprobe をインストール
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
