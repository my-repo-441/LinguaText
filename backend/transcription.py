import os
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech

# Google Cloud認証情報ファイルのパスを環境変数に設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/keisuke/Documents/Python/LinguaText/backend/speechtotext-440503-44ea1f8a5734.json"

def split_audio(file_path, chunk_length_ms):
    audio = AudioSegment.from_mp3(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def mp3_to_text(file_path):
    # 音声ファイルを55秒（55000ms）ごとに分割
    chunks = split_audio(file_path, 55000)

    # Google Speech-to-Text クライアントの初期化
    client = speech.SpeechClient()

    full_transcript = ""
    for i, chunk in enumerate(chunks):
        # チャンクをモノラルに変換し、WAV形式で保存
        chunk = chunk.set_channels(1)  # モノラルに変換
        wav_path = f"/Users/keisuke/Documents/Python/Speech-to-text/output/chunked_audio_file/chunk_{i}.wav"
        chunk.export(wav_path, format="wav", parameters=["-ar", "16000"]) 

        # 音声データの読み込み
        with open(wav_path, "rb") as audio_file:
            content = audio_file.read()
        
        # リクエスト用のオーディオ設定
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,  # サンプルレートを設定（必要に応じて変更）
            language_code="en-US"  # 言語コードを適宜設定
        )
        
        # 音声データの認識（非同期認識に変更）
        try:
            operation = client.long_running_recognize(config=config, audio=audio)
            print(f"Chunk {i}: Waiting for operation to complete...")
            response = operation.result(timeout=1000)

            # 認識結果を収集
            for result in response.results:
                full_transcript += result.alternatives[0].transcript + " "
        except Exception as e:
            print(f"チャンク {i} の認識中にエラーが発生しました: {e}")
    
    # 最終的なテキストをテキストファイルに保存
    with open("/Users/keisuke/Documents/Python/Speech-to-text/output/transcription_output.txt", "w") as output_file:
        output_file.write(full_transcript)
    
    # 最終的なテキストの出力
    print("Full Transcript:", full_transcript)

# 実行例
mp3_to_text("/Users/keisuke/Documents/Python/Speech-to-text/audio_files/sample-reinvent-short.mp3")