# V2GIF2IMG

動画からGIFへの変換とフレーム抽出を行うWebアプリケーション

## 機能

- 動画からGIFへの変換
  - 開始/終了時間の指定
  - FPSの調整
  - サイズ調整
- フレーム抽出
  - 最後のフレーム抽出
  - 任意の時間のフレーム抽出

## 必要要件

- Python 3.8以上
- moviepy
- gradio
- imageio

## インストール

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/v2gif2img.git
cd v2gif2img

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Linuxの場合
venv\Scripts\activate     # Windowsの場合

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 使用方法

```bash
# アプリケーションの起動
python app.py
```

起動後、ブラウザで http://localhost:7860 にアクセスしてください。

### GIF変換

1. 「GIF変換」タブを選択
2. 動画をアップロード
3. 必要に応じてパラメータを調整：
   - 開始時間（秒）
   - 終了時間（秒）
   - FPS（1-30）
   - リサイズ倍率（0.1-2.0）
4. 「GIFを生成」ボタンをクリック

### フレーム抽出

1. 「フレーム抽出」タブを選択
2. 動画をアップロード
3. 以下のいずれかの方法でフレームを抽出：
   - 「最後のフレーム抽出」ボタンをクリック
   - スライダーで時間を指定して任意の位置のフレームを抽出

## 開発者向け情報

### テストの実行

```bash
# すべてのテストを実行
pytest

# カバレッジレポート付きでテストを実行
pytest --cov=src tests/
```

### Lintチェック

```bash
pylint src/ tests/
```

## ライセンス

MIT

## 作者

やすさん
