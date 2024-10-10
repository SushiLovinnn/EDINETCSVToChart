# EDINETCSVToChart

このプログラムは、EDINETで取得できる有価証券報告書のCSVファイルから必要なデータを抜き出してJSONファイルに変換し、さらにそのデータを用いて棒グラフを生成します。
## 構成

- `main.py`: メインの処理を行うスクリプト。
- `plot.py`: 棒グラフを生成するためのスクリプト。
- `config.json`: 設定ファイル。
- `requirements.txt`: 必要なパッケージを記載したファイル。
- `.gitignore`: Gitで無視するファイルやディレクトリを記載したファイル。
- `CSVs/`: 処理されたCSVファイルを格納するディレクトリ。
- `ZIPs/`: ダウンロードされたZIPファイルを格納するディレクトリ。
- `json_file/`: 生成されたJSONファイルを格納するディレクトリ。

## インストール

1. リポジトリをクローンします。

    ```sh
    git clone https://github.com/SushiLovinnn/EDINETCSVToChart/
    cd EDINETCSVToChart
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

    - `select_data`: `true`に設定すると、個別のCSVファイルを選択します。`false`に設定すると、CSVs内の全てのCSVファイルを処理します。
    - `show_chart`を`true`に設定すると、棒グラフを表示します。

2. プログラムを実行します。

    ```sh
    python main.py
    ```

3. プログラムの実行中に、CSVファイルまたはフォルダのパスを入力します。

## 主な機能

- **CSVProcessor**: CSVファイルを読み込み、データを処理してJSONファイルに変換します。
    - `load_csv()`: CSVファイルを読み込みます。
    - `process_data()`: データを処理します。
    - `save_to_json()`: データをJSONファイルに保存します。
    - `rename_csv_file()`: CSVファイルの名前を変更します。

- **Barchart**: JSONファイルを読み込み、棒グラフを生成します。
    - `reading_json()`: JSONファイルを読み込みます。
    - `plot()`: 棒グラフを生成します。

- `extract_target_csv()`: ZIPファイルから目的のCSVファイルを抽出します。
- `find_csv_files_in_folder()`: 指定されたフォルダ内の全てのCSVファイルを探します。
- `check_missing_data()`: 取得できなかったデータを確認します。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細はLICENSEファイルを参照してください。
