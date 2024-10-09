# CSV to JSON Processor

このプロジェクトは、CSVファイルを処理してJSONファイルに変換し、さらにそのデータを用いて棒グラフを生成するPythonプログラムです。

## 構成

- `main.py`: メインの処理を行うスクリプト。
- `csv_downloader.py`: CSVファイルをダウンロードするスクリプト。
- `plot.py`: 棒グラフを生成するためのスクリプト。
- `config.json`: 設定ファイル。
- `requirements.txt`: 必要なPythonパッケージを記載したファイル。
- `.gitignore`: Gitで無視するファイルやディレクトリを記載したファイル。
- `CSVs/`: 処理されたCSVファイルを格納するディレクトリ。
- `ZIPs/`: ダウンロードされたZIPファイルを格納するディレクトリ。

## インストール

1. リポジトリをクローンします。

    ```sh
    git clone <リポジトリのURL>
    cd <リポジトリのディレクトリ>
    ```

2. 必要なパッケージをインストールします。

    ```sh
    pip install -r requirements.txt
    ```

## 使い方

1. `config.json`を編集して設定を行います。

    ```json
    {
        "select_data": true,
        "show_chart": true
    }
    ```

    - [`select_data`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A305%2C%22character%22%3A15%7D%7D%5D%2C%22cbe812e2-4b5f-4245-accd-e5a01d5a1b89%22%5D "Go to definition"): `true`に設定すると、個別のCSVファイルを選択します。`false`に設定すると、フォルダ内の全てのCSVファイルを処理します。
    - [`show_chart`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2Fplot.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A9%2C%22character%22%3A44%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A323%2C%22character%22%3A59%7D%7D%5D%2C%22cbe812e2-4b5f-4245-accd-e5a01d5a1b89%22%5D "Go to definition"): `true`に設定すると、棒グラフを表示します。

2. プログラムを実行します。

    ```sh
    python main.py
    ```

3. プログラムの実行中に、CSVファイルまたはフォルダのパスを入力します。

## 主な機能

- **CSVProcessor**: CSVファイルを読み込み、データを処理してJSONファイルに変換します。
    - [`load_csv()`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22load_csv\(\)%22%2C%22cbe812e2-4b5f-4245-accd-e5a01d5a1b89%22%5D "/Users/fukamiayumionore/Documents/GitHub/EDINETCSVToChart/main.py"): CSVファイルを読み込みます。
    - [`process_data()`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22process_data\(\)%22%2C%22cbe812e2-4b5f-4245-accd-e5a01d5a1b89%22%5D "/Users/fukamiayumionore/Documents/GitHub/EDINETCSVToChart/main.py"): データを処理します。
    - [`save_to_json()`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22save_to_json\(\)%22%2C%22cbe812e2-4b5f-4245-accd-e5a01d5a1b89%22%5D "/Users/fukamiayumionore/Documents/GitHub/EDINETCSVToChart/main.py"): データをJSONファイルに保存します。
    - [`rename_csv_file()`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2Fmain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22rename_csv_file\(\)%22%2C%22cbe812e2-4b5f-4245-accd-e5a01d5a1b89%22%5D "/Users/fukamiayumionore/Documents/GitHub/EDINETCSVToChart/main.py"): CSVファイルの名前を変更します。

- **Barchart**: JSONファイルを読み込み、棒グラフを生成します。
    - [`reading_json()`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2Fplot.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22reading_json\(\)%22%2C%22cbe812e2-4b5f-4245-accd-e5a01d5a1b89%22%5D "/Users/fukamiayumionore/Documents/GitHub/EDINETCSVToChart/plot.py"): JSONファイルを読み込みます。
    - [`plot()`](command:_github.copilot.openSymbolInFile?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2Fplot.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22plot\(\)%22%2C%22cbe812e2-4b5f-4245-accd-e5a01d5a1b89%22%5D "/Users/fukamiayumionore/Documents/GitHub/EDINETCSVToChart/plot.py"): 棒グラフを生成します。

- **extract_target_csv()**: ZIPファイルから目的のCSVファイルを抽出します。
- **find_csv_files_in_folder()**: 指定されたフォルダ内の全てのCSVファイルを検索します。
- **check_missing_data()**: データが欠落しているかどうかを確認します。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2FLICENSE%22%2C%22path%22%3A%22%2FUsers%2Ffukamiayumionore%2FDocuments%2FGitHub%2FEDINETCSVToChart%2FLICENSE%22%2C%22scheme%22%3A%22file%22%7D%7D)ファイルを参照してください。