import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

# Google Cloud認証情報ファイルのパスを環境変数に設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/your-json-file"

app = Flask(__name__)
CORS(app, supports_credentials=True)

def split_audio(file_path, chunk_length_ms):
    audio = AudioSegment.from_mp3(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def mp3_to_text(file_path):
    output_dir = "/app/output/chunked_audio_file"
    os.makedirs(output_dir, exist_ok=True)

    # 音声ファイルを55秒（55000ms）ごとに分割
    chunks = split_audio(file_path, 55000)

    # Google Speech-to-Text v2 クライアントの初期化
    client = SpeechClient()

    full_transcript = ""
    for i, chunk in enumerate(chunks):
        # チャンクをモノラルに変換し、WAV形式で保存
        chunk = chunk.set_channels(1)
        wav_path = f"{output_dir}/chunk_{i}.wav"
        chunk.export(wav_path, format="wav", parameters=["-ar", "16000"]) 

        # 音声データの読み込み
        with open(wav_path, "rb") as audio_file:
            audio_content = audio_file.read()

        # 設定を作成
        config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=["en-US"],
            model="long",
        )

        # 認識リクエストを作成
        request = cloud_speech.RecognizeRequest(
            recognizer=f"projects/{PROJECT_ID}/locations/global/recognizers/_",
            config=config,
            content=audio_content,
        )

        # 音声データの認識
        try:
            response = client.recognize(request=request)
            print(f"Chunk {i}: Recognition complete.")

            # 認識結果を収集
            for result in response.results:
                full_transcript += result.alternatives[0].transcript + " "
        except Exception as e:
            print(f"チャンク {i} の認識中にエラーが発生しました: {e}")
    
    # transcript をテキストファイルに保存
    output_file_path = "/app/output/transcript_output.txt"
    with open(output_file_path, "w") as output_file:
        output_file.write(full_transcript)

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

# 翻訳と要約の関数はそのままです
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
