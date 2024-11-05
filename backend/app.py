import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 

client = OpenAI()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Google Cloud認証情報ファイルのパスを環境変数に設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/speechtotext-440503-44ea1f8a5734.json"

app = Flask(__name__)
# CORSを有効化してすべてのオリジンを許可
CORS(app, supports_credentials=True)  # すべてのオリジンを許可

def split_audio(file_path, chunk_length_ms):
    audio = AudioSegment.from_mp3(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def mp3_to_text(file_path):
    # 出力ディレクトリを指定し、存在しない場合は作成
    output_dir = "/app/output/chunked_audio_file"
    os.makedirs(output_dir, exist_ok=True)

    # 音声ファイルを55秒（55000ms）ごとに分割
    chunks = split_audio(file_path, 55000)

    # Google Speech-to-Text クライアントの初期化
    client = speech.SpeechClient()

    full_transcript = ""
    for i, chunk in enumerate(chunks):
        # チャンクをモノラルに変換し、WAV形式で保存
        chunk = chunk.set_channels(1)  # モノラルに変換
        wav_path = f"{output_dir}/chunk_{i}.wav"
        chunk.export(wav_path, format="wav", parameters=["-ar", "16000"]) 

        # 音声データの読み込み
        with open(wav_path, "rb") as audio_file:
            content = audio_file.read()

        # リクエスト用のオーディオ設定
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US"
        )
        
        # 音声データの認識
        try:
            operation = client.long_running_recognize(config=config, audio=audio)
            print(f"Chunk {i}: Waiting for operation to complete...")
            response = operation.result(timeout=1000)

            # 認識結果を収集
            for result in response.results:
                full_transcript += result.alternatives[0].transcript + " "
        except Exception as e:
            print(f"チャンク {i} の認識中にエラーが発生しました: {e}")
    
    return full_transcript

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "File is required"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # アップロードされたファイルを保存する
    file_path = f"/app/audio_files/{file.filename}"
    file.save(file_path)

    try:
        transcript = mp3_to_text(file_path)
        return jsonify({"transcription": transcript})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "Text is required"}), 400

    try:
        translated_text = translate_text_to_japanese(data['text'])
        return jsonify({"translation": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def translate_text_to_japanese(text):
    messages = [
        {"role": "system", "content": "あなたは優秀な翻訳家です。次の文章を日本語に翻訳して。"},
        {"role": "user", "content": f"文章：{text}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=5000
    )
    translated_text = response.choices[0].message.content.strip()

    return translated_text

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "Text is required"}), 400

    try:
        summary = summarize_translated_text(data['text'])
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def summarize_translated_text(text):
    messages = [
        {"role": "system", "content": "あなたは優秀な要約者です。次の文章を要約してください。"},
        {"role": "user", "content": f"文章：{text}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=1000
    )
    summary = response.choices[0].message.content.strip()

    return summary

@app.errorhandler(500)
def internal_error(error):
    print(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
