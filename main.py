import pandas as pd
import json
from plot import Plot

class CSVToJSONConverter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ID_expression_dict = {
            ('jpcrp_cor:CompanyNameCoverPage', 'FilingDateInstant'): ['会社名', -1, '単位'],
            ('jpcrp030000-asr_E02144-000:OperatingRevenuesIFRSKeyFinancialData', 'CurrentYearDuration'): ['売上高(IFRS)', -1, '単位'],
            ('jpigp_cor:OperatingProfitLossIFRS', 'CurrentYearDuration'): ['営業利益(IFRS)', -1, '単位'],
            ('jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults', 'CurrentYearDuration'): ['当期純利益(IFRS)', -1, '単位'],
            ('jpigp_cor:AssetsIFRS', 'CurrentYearInstant'): ['資産(IFRS)', -1, '単位'],
            ('jpigp_cor:LiabilitiesIFRS', 'CurrentYearInstant'): ['負債(IFRS)', -1, '単位'],
            ('jpigp_cor:CurrentAssetsIFRS', 'CurrentYearInstant'): ['流動資産(IFRS)', -1, '単位'],
            ('jpigp_cor:NonCurrentAssetsIFRS', 'CurrentYearInstant'): ['固定資産(IFRS)', -1, '単位'],
            ('jpdei_cor:CurrentPeriodEndDateDEI', 'FilingDateInstant'): ['当会計期間終了日', -1, '単位'],
            ('jpigp_cor:EquityIFRS', 'CurrentYearInstant'): ['資本(IFRS)', -1, '単位'],
            ('jpigp_cor:TotalCurrentLiabilitiesIFRS', 'CurrentYearInstant'): ['流動負債(IFRS)', -1, '単位'],
            ('jpigp_cor:NonCurrentLabilitiesIFRS', 'CurrentYearInstant'): ['固定負債(IFRS)', -1, '単位'],
            ('jpigp_cor:InterestBearingLiabilitiesCLIFRS', 'CurrentYearInstant'): ['有利子流動負債(IFRS)', -1, '単位'],
            ('jpigp_cor:InterestBearingLiabilitiesNCLIFRS', 'CurrentYearInstant'): ['有利子固定負債(IFRS)', -1, '単位']
        }
        self.df = None
        self.data = {}
        self.json_file_path = ''

    def load_csv(self):
        try:
            self.df = pd.read_csv(self.file_path, encoding='utf-16le', delimiter='\t')
        except Exception as e:
            print(f"読み込みエラー: {e}")
            exit()

    def process_data(self):
        def update_id_expression_dict(row):
            key = (row['要素ID'], row['コンテキストID'])
            if key in self.ID_expression_dict:
                try:
                    self.ID_expression_dict[key][1] = int(row['値'])
                except ValueError:
                    self.ID_expression_dict[key][1] = row['値']
                self.ID_expression_dict[key][2] = row['単位']

        self.df.apply(update_id_expression_dict, axis=1)

    def create_json_data(self):
        self.data = {
            'CompanyName': self.ID_expression_dict[('jpcrp_cor:CompanyNameCoverPage', 'FilingDateInstant')],
            'Sales': self.ID_expression_dict[('jpcrp030000-asr_E02144-000:OperatingRevenuesIFRSKeyFinancialData', 'CurrentYearDuration')],
            'OperatingProfits': self.ID_expression_dict[('jpigp_cor:OperatingProfitLossIFRS', 'CurrentYearDuration')],
            'NetIncome': self.ID_expression_dict[('jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults', 'CurrentYearDuration')],
            'Assets': self.ID_expression_dict[('jpigp_cor:AssetsIFRS', 'CurrentYearInstant')],
            'Liabilities': self.ID_expression_dict[('jpigp_cor:LiabilitiesIFRS', 'CurrentYearInstant')],
            'CurrentAssets': self.ID_expression_dict[('jpigp_cor:CurrentAssetsIFRS', 'CurrentYearInstant')],
            'NonCurrentAssets': self.ID_expression_dict[('jpigp_cor:NonCurrentAssetsIFRS', 'CurrentYearInstant')],
            'EndDate': self.ID_expression_dict[('jpdei_cor:CurrentPeriodEndDateDEI', 'FilingDateInstant')],
            'NetAssets': self.ID_expression_dict[('jpigp_cor:EquityIFRS', 'CurrentYearInstant')],
            'CurrentLiabilities': self.ID_expression_dict[('jpigp_cor:TotalCurrentLiabilitiesIFRS', 'CurrentYearInstant')],
            'NonCurrentLiabilities': self.ID_expression_dict[('jpigp_cor:NonCurrentLabilitiesIFRS', 'CurrentYearInstant')],
            'Interest-bearingCurrentLiabilities': self.ID_expression_dict[('jpigp_cor:InterestBearingLiabilitiesCLIFRS', 'CurrentYearInstant')],
            'Interest-bearingNonCurrentLiabilities': self.ID_expression_dict[('jpigp_cor:InterestBearingLiabilitiesNCLIFRS', 'CurrentYearInstant')]
        }

    def save_to_json(self):
        self.json_file_path = f'json_file/{self.data["CompanyName"][1]}{self.data["EndDate"][1]}.json'
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(self.data, json_file, ensure_ascii=False, indent=4)
            print(f"JSONファイルを保存しました: {self.json_file_path}")
        except Exception as e:
            print(f"JSONファイル保存エラー: {e}")
            exit()

def main():
    file_path = input("CSV file path: ")
    converter = CSVToJSONConverter(file_path)
    converter.load_csv()
    converter.process_data()
    converter.create_json_data()
    converter.save_to_json()
    chart = Plot(converter.json_file_path)
    chart.plot()

if __name__ == "__main__":
    main()