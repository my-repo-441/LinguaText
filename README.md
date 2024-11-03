# LinguaText

## Webサイトの起動
- コンテナのビルドと起動
`docker compose up --build`

- http://localhost:3000にアクセス

1.mp3ファイルを選択
2.文字起こしボタンを押下


## pythonのライブラリを追加するとき
`source ~/venv/speech-to-text/bin/activate`

`pip install <ライブラリ名>`

`pip freeze > ./backend/requirements.txt`
