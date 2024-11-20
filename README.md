# LinguaText

LinguaTextは、音声ファイルの文字起こし、翻訳、要約を行うWebアプリケーションです。このプロジェクトは、フロントエンド（React）とバックエンド（Flask）で構成されています。

---

## 📂 ディレクトリ構成

```plaintext
.
├── README.md               # 本ドキュメント
├── docker-compose.yml      # Docker Compose設定ファイル
├── backend/                # バックエンド用ディレクトリ
│   ├── Dockerfile          # バックエンド用Dockerfile
│   ├── app.py              # バックエンドのFlaskアプリケーション
│   ├── audio_files/        # 音声ファイルの保存ディレクトリ
│   ├── output/             # 文字起こし結果の保存ディレクトリ
│   ├── requirements.txt    # Python依存ライブラリ
│   └── speechtotext-*.json # Google Cloud認証情報ファイル
├── frontend/               # フロントエンド用ディレクトリ
│   ├── Dockerfile          # フロントエンド用Dockerfile
│   ├── public/index.html   # HTMLテンプレート
│   ├── src/                # Reactコンポーネント
│   │   ├── App.js          # メインアプリケーション
│   │   └── index.js        # Reactのエントリーポイント
│   ├── package.json        # Node.js依存ライブラリ
│   └── package-lock.json   # Node.js依存情報
```

---

## 💻 必要な環境

- **Docker**: バージョン20.x以上推奨
- **Docker Compose**
- **Google Cloud Speech-to-Text API認証情報**
  - ファイル名: `speechtotext-440503-44ea1f8a5734.json`

---

## 🔧 環境変数

### バックエンド

- `OPENAI_API_KEY`: OpenAI APIキー。文字起こし、翻訳、要約に使用。
- `GOOGLE_CLOUD_PROJECT`: Google Cloud Speech-to-Text API用のプロジェクトID。

---

## 🚀 セットアップと起動

### **1. リポジトリのクローン**
```bash
git clone https://github.com/yourusername/linguatext.git
cd linguatext
```

### **2. Docker Composeによるビルドと起動**
```bash
docker-compose build
docker-compose up
```

### **3. サービスの確認**
- フロントエンド: [http://localhost:3000](http://localhost:3000)
- バックエンド: [http://localhost:5001](http://localhost:5001)

---

## 🛠 使用方法

1. **音声ファイルのアップロード**
   - フロントエンドのフォームから音声ファイルを選択します。

2. **文字起こし**
   - 「文字起こし」ボタンをクリックして、アップロードした音声ファイルの文字起こしを実行します。

3. **翻訳**
   - 文字起こしが完了すると「翻訳」ボタンが有効になります。クリックして日本語に翻訳します。

4. **要約**
   - 翻訳が完了すると「要約」ボタンが有効になります。クリックして翻訳結果を要約します。

---

## 🌐 API エンドポイント

### バックエンドのエンドポイント

| メソッド | エンドポイント       | 説明                   |
|----------|----------------------|------------------------|
| POST     | `/transcribe`        | 音声ファイルを文字起こし |
| POST     | `/translate`         | 文字起こし内容を翻訳   |
| POST     | `/summarize`         | 翻訳内容を要約         |

---

## ⚙️ 開発者向け情報

### フロントエンド

- **依存ライブラリのインストール**
  ```bash
  cd frontend
  npm install
  ```

- **ローカル環境で起動**
  ```bash
  npm start
  ```

### バックエンド

- **依存ライブラリのインストール**
  ```bash
  cd backend
  pip install -r requirements.txt
  ```

- **ローカル環境で起動**
  ```bash
  python app.py
  ```

- ## pythonのライブラリを追加するとき
  ```source ~/venv/speech-to-text/bin/activate
  ```
  ```pip install <ライブラリ名>
  ```
  ```pip freeze > ./backend/requirements.txt
  ```
---


