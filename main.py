import os
import zipfile
import json
import pandas as pd
from plot import Barchart



class CSVToJSONConverter:

    def __init__(self, file_path):
        self.file_path = file_path
        self.missing_GAAP = False
        self.data = {
            'CompanyName': ['会社名', -1, '単位'],
            'Sales': ['売上収益(IFRS)', -1, '単位'],
            'OperatingProfits': ['営業利益(IFRS)', -1, '単位'],
            'NetIncome': ['当期純利益(IFRS)', -1, '単位'],
            'Assets': ['資産(IFRS)', -1, '単位'],
            'Liabilities': ['負債(IFRS)', -1, '単位'],
            'CurrentAssets': ['流動資産(IFRS)', -1, '単位'],
            'NonCurrentAssets': ['固定資産(IFRS)', -1, '単位'],
            'EndDate': ['当会計期間終了日', -1, '単位'],
            'NetAssets': ['資本(IFRS)', -1, '単位'],
            'CurrentLiabilities': ['流動負債(IFRS)', -1, '単位'],
            'NonCurrentLiabilities': ['固定負債(IFRS)', -1, '単位'],
            'Interest-bearingCurrentLiabilities': ['有利子流動負債(IFRS)', -1, '単位'],
            'Interest-bearingNonCurrentLiabilities': ['有利子固定負債(IFRS)', -1, '単位']
        }
        self.CompanyName_IDs = (
            ('jpcrp_cor:CompanyNameCoverPage', 'FilingDateInstant'),
        )
        self.IFRSSales_IDs = (
            ('jpcrp030000-asr_E02144-000:OperatingRevenuesIFRSKeyFinancialData', 'CurrentYearDuration'),
            ('jpcrp_cor:RevenueIFRSSummaryOfBusinessResults', 'CurrentYearDuration'),
            ('jpcrp030000-asr_E01807-000:NetSalesIFRSSummaryOfBusinessResults', 'CurrentYearDuration')
        )
        self.IFRSOperatingProfits_IDs = (
            ('jpigp_cor:OperatingProfitLossIFRS', 'CurrentYearDuration'),
        )
        self.IFRSNetIncome_IDs = (
            ('jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults', 'CurrentYearDuration'),
            ('jpcrp_cor:ProfitLossIFRSSummaryOfBusinessResults', 'CurrentYearDuration')
        )
        self.IFRSAssets_IDs = (
            ('jpigp_cor:AssetsIFRS', 'CurrentYearInstant'),
        )
        self.IFRSLiabilities_IDs = (
            ('jpigp_cor:LiabilitiesIFRS', 'CurrentYearInstant'),
        )
        self.IFRSCurrentAssets_IDs = (
            ('jpigp_cor:CurrentAssetsIFRS', 'CurrentYearInstant'),
        )
        self.IFRSNonCurrentAssets_IDs = (
            ('jpigp_cor:NonCurrentAssetsIFRS', 'CurrentYearInstant'),
        )
        self.EndDate_IDs = (
            ('jpdei_cor:CurrentPeriodEndDateDEI', 'FilingDateInstant'),
        )
        self.IFRSNetAssets_IDs = (
            ('jpigp_cor:EquityIFRS', 'CurrentYearInstant'),
        )
        self.IFRSCurrentLiabilities_IDs = (
            ('jpigp_cor:TotalCurrentLiabilitiesIFRS', 'CurrentYearInstant'),
        )
        self.IFRSNonCurrentLiabilities_IDs = (
            ('jpigp_cor:NonCurrentLabilitiesIFRS', 'CurrentYearInstant'),
        )
        self.IFRSInterestBearingCurrentLiabilities_IDs = (
            ('jpigp_cor:InterestBearingLiabilitiesCLIFRS', 'CurrentYearInstant'),
        )
        self.IFRSInterestBearingNonCurrentLiabilities_IDs = (
            ('jpigp_cor:InterestBearingLiabilitiesNCLIFRS', 'CurrentYearInstant'),
        )
        self.tuple_of_IDs = (
            self.CompanyName_IDs,
            self.IFRSSales_IDs,
            self.IFRSOperatingProfits_IDs,
            self.IFRSOperatingProfits_IDs,
            self.IFRSNetIncome_IDs,
            self.IFRSAssets_IDs,
            self.IFRSLiabilities_IDs,
            self.IFRSCurrentAssets_IDs,
            self.IFRSNonCurrentAssets_IDs,
            self.EndDate_IDs,
            self.IFRSNetAssets_IDs,
            self.IFRSCurrentLiabilities_IDs,
            self.IFRSNonCurrentLiabilities_IDs,
            self.IFRSInterestBearingCurrentLiabilities_IDs,
            self.IFRSInterestBearingNonCurrentLiabilities_IDs
            )
        self.ID_expression_dict = {
            self.CompanyName_IDs: 'CompanyName',
            self.IFRSSales_IDs: 'Sales',
            self.IFRSOperatingProfits_IDs: 'OperatingProfits',
            self.IFRSNetIncome_IDs: 'NetIncome',
            self.IFRSAssets_IDs: 'Assets',
            self.IFRSLiabilities_IDs: 'Liabilities',
            self.IFRSCurrentAssets_IDs: 'CurrentAssets',
            self.IFRSNonCurrentAssets_IDs: 'NonCurrentAssets',
            self.EndDate_IDs: 'EndDate',
            self.IFRSNetAssets_IDs: 'NetAssets',
            self.IFRSCurrentLiabilities_IDs: 'CurrentLiabilities',
            self.IFRSNonCurrentLiabilities_IDs: 'NonCurrentLiabilities',
            self.IFRSInterestBearingCurrentLiabilities_IDs: 'Interest-bearingCurrentLiabilities',
            self.IFRSInterestBearingNonCurrentLiabilities_IDs: 'Interest-bearingNonCurrentLiabilities'
        }
        self.df = None
        self.json_file_path = ''

    def load_csv(self):
        try:
            self.df = pd.read_csv(self.file_path, encoding='utf-16le', delimiter='\t')
        except Exception as e:
            print(f"読み込みエラー: {e}")
            exit()

    def process_data(self):
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            key = (row['要素ID'], row['コンテキストID'])
            for IDs in self.tuple_of_IDs:
                if key in IDs:
                    try:
                        self.data[self.ID_expression_dict[IDs]][1] = int(row['値'])
                    except ValueError:
                        self.data[self.ID_expression_dict[IDs]][1] = row['値']
                    self.data[self.ID_expression_dict[IDs]][2] = row['単位'] if row['単位'] != '－' else ''

    def save_to_json(self) -> None:
        """
        dataをjsonファイルにして保存する関数
        """
        self.json_file_path = f'json_file/{self.data["CompanyName"][1]}{self.data["EndDate"][1]}.json'
        # ディレクトリが存在しなければ作成
        json_dir = os.path.dirname(self.json_file_path)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
            
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(self.data, json_file, ensure_ascii=False, indent=4)
            print(f"JSONファイルを保存しました: {self.json_file_path}")
        except Exception as e:
            print(f"JSONファイル保存エラー: {e}")
            exit()


def find_csv_files_in_folder(folder_path: str) -> list[str]:
    """
    ファイル内のに存在する全てのCSVファイルの絶対パスをリストで返す関数
    """
    
    # フォルダ内のCSVファイルのパスを格納するリスト
    csv_files = []
    # フォルダ内のすべてのファイルとディレクトリをチェック
    for file_name in os.listdir(folder_path):
        # 絶対パスを取得
        file_path = os.path.join(folder_path, file_name)
        # ファイルがCSVファイルであるかを確認
        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            csv_files.append(file_path)
    
    return csv_files


def check_missing_data(converter: CSVToJSONConverter, is_missing_data: dict) -> None:
    """
    見つからなかった値がGAAP指標かNon-GAAP指標か確認して報告する関数
    返り値はない
    """
    GAAP = ("Sales", "NetIncome", "Assets", "Liabilities",
            "CurrentAssets", "NonCurrentAssets", 
            "NetAssets", "CurrentLiabilities",
            "NonCurrentLiabilities")
    # NonGAAP = ("OperatingProfits", "Interest-bearingCurrentLiabilities",
    #           "Interest-bearingNonCurrentLiabilities")
    for key, is_missing in is_missing_data.items():
        if is_missing:
            if key in GAAP:
                converter.missing_GAAP = True
                print(f'**GAAP指標である{converter.data[key][0]}が見つかりませんでした。**')
            else:
                print(f'Non-GAAP指標である{converter.data[key][0]}が見つかりませんでした。')


def extract_target_csv(zip_path, extract_to, target_csv_name=None):
    """
    ZIPファイルから目的のCSVファイルを抽出する
    
    Parameters
    ----------

    :param extract_to: 抽出先のディレクトリ
    :param target_csv_name: 抽出したいCSVファイル名（指定しない場合はすべてのCSVを抽出）
    """
    # ZIPファイルが存在するか確認
    if not os.path.exists(zip_path):
        print(f"指定されたZIPファイルが存在しません: {zip_path}")
        return
    
    # 抽出先ディレクトリが存在しない場合は作成
    if not os.path.isdir(extract_to):
        os.makedirs(extract_to, exist_ok=True)
        print(f"抽出先ディレクトリを作成しました: {extract_to}")
    
    # ZIPファイルを開く
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # ZIP内のファイルリストを取得
        all_files = zip_ref.namelist()
        
        # CSVファイルのみをフィルタリング
        csv_files = [f for f in all_files if f.endswith('.csv')]
        
        if not csv_files:
            print("ZIPファイル内にCSVファイルが存在しません。")
            return
        
        if target_csv_name:
            # 指定されたCSVが存在するか確認
            if target_csv_name in csv_files:
                zip_ref.extract(target_csv_name, extract_to)
                print(f"{target_csv_name} を {extract_to} に抽出しました。")
            else:
                print(f"{target_csv_name} はZIPファイル内に存在しません。")
        else:
            # すべてのCSVを抽出
            zip_ref.extractall(extract_to, members=csv_files)
            print(f"すべてのCSVファイルを {extract_to} に抽出しました。")



def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    extract_target_csv()
    folder_path = input("CSV folder path: ")
    paths = find_csv_files_in_folder(folder_path)
    if paths == []:
        print('CSVファイルが見つかりませんでした。')
    missing_GAAP = []
    for file_path in paths:
        converter = CSVToJSONConverter(file_path)
        converter.load_csv()
        converter.process_data()
        print(f'-----{converter.data["CompanyName"][1]}-----')
        converter.save_to_json()
        chart = Barchart(converter.json_file_path, config["show_chart"])
        chart.plot()
        check_missing_data(converter, chart.is_missing_data)
        print("---------------" + '-'*int(1.5*len(converter.data["CompanyName"][1])))
        if converter.missing_GAAP:
            missing_GAAP.append(converter.data['CompanyName'][1])
    if missing_GAAP != []:
        print('以下の会社からGAAP指標を抜き出すことに失敗しました。')
        for name in missing_GAAP:
            print(name)



if __name__ == "__main__":
    main()