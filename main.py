import os
import zipfile
import shutil
import json
import pandas as pd
from typing import Dict
from plot import Barchart


class DataItem:
    """
    データ項目を表すクラス。

    Attributes
    ----------
    name : str
        データ項目の名前。
    value : int | str
        データ項目の値。数値(-1: 値が見つからないことを表す)または文字列。
    unit : str
        データ項目の単位。
    ifrs_flag : int
        IFRSかどうかを示すフラグ。1の場合はIFRS、0の場合はIFRSでない。
    """

    def __init__(self, name: str, value: int | str, unit: str, ifrs_flag: int):
        self.name = name
        self.value = value
        self.unit = unit
        self.ifrs_flag = ifrs_flag

    def __str__(self):
        return f'{self.name}: {self.value} {self.unit}'


class CSVProcessor:
    """
    CSVファイルを処理してデータを抽出し、JSON形式で保存するクラス。

    Attributes
    ----------
    file_path : str
        処理するCSVファイルのパス。
    missing_GAAP : bool
        GAAP指標が欠落しているかどうかを示すフラグ。
    missing_main_measure : bool
        主要な指標が欠落しているかどうかを示すフラグ。
    data : dict
        データ項目の辞書。各キーはデータ項目名であり、値はDataItemオブジェクト.
    """
    def __init__(self, file_path: str):
        self.secCode = file_path.split('_')[-1][:-4]
        self.data = {
            'CompanyName': DataItem('会社名', -1, '単位', 0),
            'IFRSSales': DataItem('売上収益(IFRS)', -1, '単位', 1),
            'Sales': DataItem('売上収益', -1, '単位', 0),
            'IFRSOperatingProfits': DataItem('営業利益(IFRS)', -1, '単位', 1),
            'OperatingProfits': DataItem('営業利益', -1, '単位', 0),
            'IFRSNetIncome': DataItem('当期純利益(IFRS)', -1, '単位', 1),
            'NetIncome': DataItem('当期純利益', -1, '単位', 0),
            'IFRSAssets': DataItem('資産(IFRS)', -1, '単位', 1),
            'Assets': DataItem('資産', -1, '単位', 0),
            'IFRSLiabilities': DataItem('負債(IFRS)', -1, '単位', 1),
            'Liabilities': DataItem('負債', -1, '単位', 0),
            'IFRSCurrentAssets': DataItem('流動資産(IFRS)', -1, '単位', 1),
            'CurrentAssets': DataItem('流動資産', -1, '単位', 0),
            'IFRSNonCurrentAssets': DataItem('固定資産(IFRS)', -1, '単位', 1),
            'NonCurrentAssets': DataItem('固定資産', -1, '単位', 0),
            'EndDate': DataItem('当会計期間終了日', -1, '単位', 0),
            'IFRSNetAssets': DataItem('資本(IFRS)', -1, '単位', 1),
            'NetAssets': DataItem('純資産', -1, '単位', 0),
            'IFRSCurrentLiabilities': DataItem('流動負債(IFRS)', -1, '単位', 1),
            'CurrentLiabilities': DataItem('流動負債', -1, '単位', 0),
            'IFRSNonCurrentLiabilities': DataItem('固定負債(IFRS)', -1, '単位', 1),
            'NonCurrentLiabilities': DataItem('固定負債', -1, '単位', 0),
            'IFRSInterest-bearingCurrentLiabilities': DataItem('有利子流動負債(IFRS)', -1, '単位', 1),
            'Interest-bearingCurrentLiabilities': DataItem('有利子流動負債', -1, '単位', 0),
            'IFRSInterest-bearingNonCurrentLiabilities': DataItem('有利子固定負債(IFRS)', -1, '単位', 1),
            'Interest-bearingNonCurrentLiabilities': DataItem('有利子固定負債', -1, '単位', 0),
            'secCode': DataItem('secCode', -1 if self.secCode == None else self.secCode, '単位', 0)
        }
        ### 会社情報の要素IDとコンテキストID
        self.CompanyName_IDs = (
            ('jpcrp_cor:CompanyNameCoverPage', 'FilingDateInstant'),
        )
        self.EndDate_IDs = (
            ('jpdei_cor:CurrentPeriodEndDateDEI', 'FilingDateInstant'),
        )
        ### 損益計算書の要素IDとコンテキストID
        self.IFRSSales_IDs = (
            ('jpcrp030000-asr_E02144-000:OperatingRevenuesIFRSKeyFinancialData', 'CurrentYearDuration'),
            ('jpcrp_cor:RevenueIFRSSummaryOfBusinessResults', 'CurrentYearDuration'),
            ('jpcrp030000-asr_E01807-000:NetSalesIFRSSummaryOfBusinessResults', 'CurrentYearDuration'),
            ('jpcrp030000-asr_E01097-000:NetSalesIFRSSummaryOfBusinessResults', 'CurrentYearDuration'),
        )
        self.Sales_IDs = (
            ('jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults', 'CurrentYearDuration'),
            ('jpcrp_cor:NetSalesSummaryOfBusinessResults', 'CurrentYearDuration'),
        )
        self.IFRSOperatingProfits_IDs = (
            ('jpigp_cor:OperatingProfitLossIFRS', 'CurrentYearDuration'),
        )
        self.OperatingProfits_IDs = (
            ('jppfs_cor:OperatingIncome', 'CurrentYearDuration'),
            )
        self.IFRSNetIncome_IDs = (
            ('jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults', 'CurrentYearDuration'),
            ('jpcrp_cor:ProfitLossIFRSSummaryOfBusinessResults', 'CurrentYearDuration')
        )
        self.Netincome_IDs = (
            ('jppfs_cor:ProfitLoss', 'CurrentYearDuration'),
        )

        ### 貸借対照表の要素IDとコンテキストID
        ## 資産の部
        self.IFRSAssets_IDs = (
            ('jpigp_cor:AssetsIFRS', 'CurrentYearInstant'),
        )
        self.Assets_IDs = (
            ('jppfs_cor:Assets', 'CurrentYearInstant'),
        )
        self.IFRSCurrentAssets_IDs = (
            ('jpigp_cor:CurrentAssetsIFRS', 'CurrentYearInstant'),
        )
        self.CurrentAssets_IDs = (
            ('jppfs_cor:CurrentAssets', 'CurrentYearInstant'),
        )
        self.IFRSNonCurrentAssets_IDs = (
            ('jpigp_cor:NonCurrentAssetsIFRS', 'CurrentYearInstant'),
        )
        self.NonCurrentAssets_IDs = (
            ('jppfs_cor:NoncurrentAssets', 'CurrentYearInstant'),
        )
        ## 負債の部
        self.IFRSLiabilities_IDs = (
            ('jpigp_cor:LiabilitiesIFRS', 'CurrentYearInstant'),
        )
        self.Liabilities_IDs = (
            ('jppfs_cor:Liabilities', 'CurrentYearInstant'),
        )
        self.IFRSCurrentLiabilities_IDs = (
            ('jpigp_cor:TotalCurrentLiabilitiesIFRS', 'CurrentYearInstant'),
        )
        self.CurrentLiabilities_IDs = (
            ('jppfs_cor:CurrentLiabilities', 'CurrentYearInstant'),
        )
        self.IFRSNonCurrentLiabilities_IDs = (
            ('jpigp_cor:NonCurrentLabilitiesIFRS', 'CurrentYearInstant'),
        )
        self.NonCurrentLiabilities_IDs = (
            ('jppfs_cor:NoncurrentLiabilities', 'CurrentYearInstant'),
        )
        self.InterestBearingCurrentLiabilities_IDs  = (

        )
        self.IFRSInterestBearingCurrentLiabilities_IDs = (
            ('jpigp_cor:InterestBearingLiabilitiesCLIFRS', 'CurrentYearInstant'),
        )
        self.InterestBearingNonCurrentLiabilities_IDs = (

        )
        self.IFRSInterestBearingNonCurrentLiabilities_IDs = (
            ('jpigp_cor:InterestBearingLiabilitiesNCLIFRS', 'CurrentYearInstant'),
        )
        ## 純資産の部
        self.IFRSNetAssets_IDs = (
            ('jpigp_cor:EquityIFRS', 'CurrentYearInstant'),
        )
        self.NetAssets_IDs = (
            ('jppfs_cor:NetAssets', 'CurrentYearInstant'),
        )
        
        
        self.ID_expression_dict = {
            self.CompanyName_IDs: 'CompanyName',
            self.IFRSSales_IDs: 'IFRSSales',
            self.Sales_IDs: 'Sales',
            self.IFRSOperatingProfits_IDs: 'IFRSOperatingProfits',
            self.OperatingProfits_IDs: 'OperatingProfits',
            self.IFRSNetIncome_IDs: 'IFRSNetIncome',
            self.Netincome_IDs: 'NetIncome',
            self.IFRSAssets_IDs: 'IFRSAssets',
            self.Assets_IDs: 'Assets',
            self.IFRSLiabilities_IDs: 'IFRSLiabilities',
            self.Liabilities_IDs: 'Liabilities',
            self.IFRSCurrentAssets_IDs: 'IFRSCurrentAssets',
            self.CurrentAssets_IDs: 'CurrentAssets',
            self.IFRSNonCurrentAssets_IDs: 'IFRSNonCurrentAssets',
            self.NonCurrentAssets_IDs: 'NonCurrentAssets',
            self.EndDate_IDs: 'EndDate',
            self.IFRSNetAssets_IDs: 'IFRSNetAssets',
            self.NetAssets_IDs: 'NetAssets',
            self.IFRSCurrentLiabilities_IDs: 'IFRSCurrentLiabilities',
            self.CurrentLiabilities_IDs: 'CurrentLiabilities',
            self.IFRSNonCurrentLiabilities_IDs: 'IFRSNonCurrentLiabilities',
            self.NonCurrentLiabilities_IDs: 'NonCurrentLiabilities',
            self.IFRSInterestBearingCurrentLiabilities_IDs: 'IFRSInterest-bearingCurrentLiabilities',
            self.InterestBearingCurrentLiabilities_IDs: 'Interest-bearingCurrentLiabilities',
            self.IFRSInterestBearingNonCurrentLiabilities_IDs: 'IFRSInterest-bearingNonCurrentLiabilities',
            self.InterestBearingNonCurrentLiabilities_IDs: 'Interest-bearingNonCurrentLiabilities',
        }
        self.df = None
        self.json_file_path = ''
        self.file_path = file_path
        self.data_to_json = {}
        self.missing_GAAP = False
        self.missing_main_measure = False

    def load_csv(self):
        try:
            self.df = pd.read_csv(self.file_path, encoding='utf-16le', delimiter='\t')
            self.secCode = self.file_path
        except Exception as e:
            print(f"読み込みエラー: {e}")
            exit()

    def process_data(self):
        """
        データフレームの各行を処理し、条件に基づいてデータを更新します。

        各行の要素IDとコンテキストIDの組み合わせをキーとして使用し、
        `self.ID_expression_dict`内のIDタプルと一致する場合にデータを更新します。
        値が整数に変換可能な場合は整数として、そうでない場合はそのままの値を使用します。
        単位が'－'でない場合はその値を使用し、'－'の場合は空文字列を設定します。

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            key = (row['要素ID'], row['コンテキストID'])
            for IDs in self.ID_expression_dict.keys():
                if key in IDs:
                    try:
                        self.data[self.ID_expression_dict[IDs]].value = int(row['値'])
                    except ValueError:
                        self.data[self.ID_expression_dict[IDs]].value = row['値']
                    self.data[self.ID_expression_dict[IDs]].unit = row['単位'] if row['単位'] != '－' else ''

    def convert_dataitem_to_dict(self) -> dict:
        """
        DataItemオブジェクトを辞書に変換する関数

        Returns
        -------
        dict
            DataItemオブジェクトを辞書に変換したもの
        """
        data_dict = {}
        for key, val in self.data.items():
            data_dict[key] = {
                'name': val.name,
                'value': val.value,
                'unit': val.unit,
                'ifrs_flag': val.ifrs_flag
            }
        return data_dict

    def save_to_json(self) -> None:
        """
        dataをjsonファイルにして保存する関数
        """
        self.data_to_json = self.convert_dataitem_to_dict()
        self.json_file_path = f'json_file/{self.data["CompanyName"].value}{self.data["EndDate"].value}.json'
        # ディレクトリが存在しなければ作成
        json_dir = os.path.dirname(self.json_file_path)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        if not os.path.exists('file_path_by_secCode.json'):
            # debug
            print('file_path_by_secCode.jsonが存在しません。')
            with open('file_path_by_secCode.json', 'w') as f:
                json.dump({self.data["secCode"].value: [self.json_file_path]}, f, ensure_ascii=False, indent=4)
        else:
            # debug
            print('file_path_by_secCode.jsonが存在します。')
            with open('file_path_by_secCode.json', 'r') as f:
                data = json.load(f)
            if self.data["secCode"].value in data.keys():
                data[self.data["secCode"].value].append(self.json_file_path)
                data[self.data["secCode"].value] = list(set(data[self.data["secCode"].value]))
            else:
                data[self.data["secCode"].value] = [self.json_file_path]
            with open('file_path_by_secCode.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(self.data_to_json, json_file, ensure_ascii=False, indent=4)
            print(f"JSONファイルを保存しました: {self.json_file_path}")
        except Exception as e:
            print(f"JSONファイル保存エラー: {e}")

    def rename_csv_file(self) -> None:
        """
        CSVファイルの名前を変更する関数
        {会社名}{決算締日}.csv として名前を変更する。
        """
        new_csv_file_path = f'CSVs/{self.data["CompanyName"].value}{self.data["EndDate"].value}.csv'
        csv_dir = os.path.dirname(new_csv_file_path)
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        
        try:
            os.rename(self.file_path, new_csv_file_path)
            print(f"CSVファイルの名前を変更しました: {new_csv_file_path}")
        except Exception as e:
            print(f"CSVファイルの名前変更エラー: {e}")


def find_csv_files_in_folder(folder_path: str) -> list[str]:
    """
    指定されたフォルダ内に存在する全てのCSVファイルの絶対パスをリストで返す関数。

    Parameters
    ----------
    folder_path : str
        CSVファイルを検索するフォルダのパス。

    Returns
    -------
    list of str
        フォルダ内の全てのCSVファイルの絶対パスを含むリスト。

    Notes
    -----
    この関数は、指定されたフォルダ内の全てのファイルとディレクトリをチェックし、
    拡張子が`.csv`であるファイルの絶対パスをリストに追加する。
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


def check_missing_data(converter: CSVProcessor, is_missing_data: dict, isIFRS: bool) -> None:
    """
    見つからなかった値がGAAP指標かNon-GAAP指標か確認して報告する関数

    Parameters
    ----------
    converter : CSVToJSONConverter
        CSVからJSONへの変換を行うオブジェクト。
    is_missing_data : dict
        データが欠落しているかどうかを示す辞書。keyはデータ項目名、値は欠落している場合はTrue、そうでない場合はFalse。
    isIFRS : bool
        与えられたデータがIFRS基準かどうかを示すフラグ。
    Returns
    -------
    None

    Notes
    -----
    GAAP指標が欠落している場合、`converter.missing_GAAP`がTrueに設定され、GAAP指標の欠落が報告される。
    Non-GAAP指標が欠落している場合、その旨が報告される。
    """
    if isIFRS:
        GAAP = ("IFRSSales", "IFRSNetIncome", "IFRSAssets", "IFRSLiabilities",
                "IFRSCurrentAssets", "IFRSNonCurrentAssets", 
                "IFRSNetAssets", "IFRSCurrentLiabilities",
                "IFRSNonCurrentLiabilities")
        NonGAAP = ("IFRSOperatingProfits", "IFRSInterest-bearingCurrentLiabilities",
                  "IFRSInterest-bearingNonCurrentLiabilities")
        for key, is_missing in is_missing_data.items():
            if is_missing:
                if key in GAAP:
                    converter.missing_GAAP = True
                    print(f'**GAAP指標である{converter.data[key].name}が見つかりませんでした。**')
                elif key in NonGAAP:
                    print(f'Non-GAAP指標である{converter.data[key].name}が見つかりませんでした。')
    else:
        main_measures = ("Sales", "OperatingProfits", "NetIncome", "Assets", "Liabilities",
                           "CurrentAssets", "NonCurrentAssets", 
                           "NetAssets", "CurrentLiabilities",
                           "NonCurrentLiabilities")

        supplementary_measures = ("Interest-bearingCurrentLiabilities",
                                  "Interest-bearingNonCurrentLiabilities")
        for key, is_missing in is_missing_data.items():
            if is_missing:
                if key in main_measures:
                    converter.missing_main_measure = True
                    print(f'**主要な指標である{converter.data[key].name}が見つかりませんでした。**')
                elif key in supplementary_measures:
                    print(f'補完的な指標である{converter.data[key].name}が見つかりませんでした。')

def extract_target_csv(zip_folder_path: str, extract_to: str):
    """
    ZIPファイルから目的のCSVファイルを抽出し、抽出後にZIPファイルを削除します。
    
    Parameters
    ----------
    zip_folder_path: str
        抽出するZIPファイルが格納されているディレクトリのパス
    extract_to: str
        抽出先ディレクトリのパス

    Returns
    -------
    None
    """
    zip_files = []
    
    # フォルダ内のすべてのファイルとディレクトリをチェック
    for file_name in os.listdir(zip_folder_path):
        # 絶対パスを取得
        file_path = os.path.join(zip_folder_path, file_name)
        # ファイルがZIPファイルであるかを確認
        if os.path.isfile(file_path) and file_name.endswith('.zip'):
            zip_files.append(file_path)
    
    for zip_path in zip_files:
        # ZIPファイルが存在するか確認
        if not os.path.exists(zip_path):
            print(f"指定されたZIPファイルが存在しません: {zip_path}")
            continue
        
        # 抽出先ディレクトリが存在しない場合は作成
        if not os.path.isdir(extract_to):
            os.makedirs(extract_to, exist_ok=True)
            print(f"抽出先ディレクトリを作成しました: {extract_to}")
        
        # ZIPファイルを開く
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # ZIP内のファイルリストを取得
            all_files = zip_ref.namelist()
            
            # 目的のCSVファイルのみをフィルタリング
            target_csv_file = ''
            for f in all_files:
                if f.startswith('XBRL_TO_CSV/jpcrp030000') and f.endswith('.csv'):
                    target_csv_file = f
            
            if target_csv_file == '':
                print(f"ZIPファイル内に目的のCSVファイルが存在しません: {zip_path}")
                continue
            else:
                # 抽出されたCSVファイルを指定のディレクトリに保存
                with zip_ref.open(target_csv_file) as source_file:
                    # 保存するファイル名はパス部分を削除したもの
                    secCode = os.path.basename(zip_path).split('_')[1].split('.')[0]
                    output_file_path = os.path.join(extract_to, f'{os.path.basename(target_csv_file)[:-4]}_{secCode}.csv')
                    with open(output_file_path, 'wb') as output_file:
                        shutil.copyfileobj(source_file, output_file)
                
                print(f"{target_csv_file} を {output_file_path} に抽出しました。")
        
        # ZIPファイルを削除
        try:
            os.remove(zip_path)
            print(f"ZIPファイルを削除しました: {zip_path}")
        except Exception as e:
            print(f"ZIPファイルの削除に失敗しました: {zip_path} - {e}")

def isIFRS(data: Dict[str, DataItem]) -> bool:
    """
    会社のデータがIFRS基準かどうかを判定する関数

    data : Dict[str, DataItem]
    ----------
    data : DataItem
        有報から抽出したデータを格納した辞書

    Returns
    -------
    bool
        IFRS基準の要素が一つでも格納されていればTrue、そうでなければFalse
    """
    for key, val in data.items():
        if val.ifrs_flag and val.value != -1:
            return True

    return False


def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    folder_path = 'CSVs'
    extract_target_csv('ZIPs', folder_path)
    paths = find_csv_files_in_folder(folder_path)
    if config["process_unprocessed_csv_only"] and paths:
        print('未処理のCSVファイルのみを処理します。')    
    if config["select_data"] == True:
        paths = [input("CSV file path: ")]
        

    if paths == []:
        print('CSVファイルが見つかりませんでした。')
    missing_GAAP = []
    missing_main_measure = []
    for file_path in paths:
        if config["process_unprocessed_csv_only"]:
            if not file_path.startswith('CSVs/jpcrp030000'):
                continue
        processor = CSVProcessor(file_path)
        processor.load_csv()
        processor.process_data()
        print(f'-----{processor.data["CompanyName"].value}-----')
        processor.save_to_json()
        processor.rename_csv_file()
        chart = Barchart(processor.json_file_path, config["show_chart"], isIFRS=isIFRS(processor.data))
        chart.plot()
        check_missing_data(processor, chart.is_missing_data, isIFRS=isIFRS(processor.data))
        print("---------------" + '-'*int(1.5*len(processor.data["CompanyName"].value)))
        if processor.missing_GAAP:
            missing_GAAP.append(processor.data['CompanyName'].value)
        if processor.missing_main_measure:
            missing_main_measure.append(processor.data['CompanyName'].value)

    if missing_GAAP != []:
        print('以下の会社からGAAP指標を抜き出すことに失敗しました。')
        for name in missing_GAAP:
            print(name)
    if missing_main_measure != []:
        print('以下の会社から主要な指標を抜き出すことに失敗しました。')
        for name in missing_main_measure:
            print(name)



if __name__ == "__main__":
    main()