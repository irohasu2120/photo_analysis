# 撮影スタイルレポート
## 概要
これまでに撮影した写真ファイルに記録されているExif情報を分析し、その情報からPDFレポートを作成します。  

前提条件：分析対象の画像フォーマットはjpg(jpeg), tiffファイルのみ。ファイルパスはWindows準拠で記載しています。

- 初期設定
  1. Pythonのインストール
      1. \>= Python 3.11
  2. 仮想環境の作成
      1. `cd {スクリプトインストールフォルダ}`
      2. `python -m venv .venv`
  3. 仮想環境の有効化
      1. `.\.venv\Scripts\activate`
  4. ライブラリのインストール
      1. `pip install -r requirements.txt`

- PDF生成
  - 前提
    - ターミナル起動の度に仮想環境を有効化すること。
  - 生成コマンド
    - `python generate_pdf.py "{分析対象フォルダ}"`
  - 生成コマンドサンプル
    - `python generate_pdf.py "C:\\sample\\photograph_dir"`
  - 出力先
    - `.\out`

参考文献
- Exif情報定義
  - [CIPA DC-008-2024 デジタルスチルカメラ用画像ファイルフォーマット規格 Exif 3.0](https://cipa.jp/j/std/std-sec.html#stdtabsTop)
