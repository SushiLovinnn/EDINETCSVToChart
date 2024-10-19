import json
import matplotlib.pyplot as plt
import matplotlib
import matplotlib_fontja
import matplotlib.ticker as ticker
from typing import Dict

matplotlib.use('Agg')


class DataItem:
    """
    DataItem クラスは、データ項目を表します。

    属性:
        name (str): データ項目の名前。
        value (int | str): データ項目の値。整数(-1)または文字列。
        unit (str): データ項目の単位。
        ifrs_flag (int): IFRSフラグ。1か0の整数。

    メソッド:
        __str__(): データ項目を文字列として返します。
    """
    def __init__(self, name: str, value: int | str, unit: str, ifrs_flag: int):
        self.name = name
        self.value = value
        self.unit = unit
        self.ifrs_flag = ifrs_flag

    def __str__(self):
        return f'{self.name}: {self.value} {self.unit}'

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

class Barchart():
    """
    JSONファイルからデータを読み込み、棒グラフを生成するクラス。

    Attributes
    ----------
    json_file_path : str
        読み込むJSONファイルのパス。
    is_missing_data : dict
        データが欠落しているかどうかを示すフラグの辞書。
    show_chart : bool
        棒グラフを表示するかどうかのフラグ。
    data : dict
        JSONファイルから読み込んだデータ。
    isIFRS : bool
        データがIFRSかどうかを示すフラグ。

    Methods
    -------
    reading_json(json_file_path: str) -> dict
        JSONファイルを読み込んでデータを返す。
    plot()
        棒グラフを生成して表示する。
    """

    def __init__(self, json_file_path: str, show_chart: bool,
                 save_fig=True, save_path='') -> None:
        self.json_file_path = json_file_path
        self.data = self.reading_json(json_file_path)
        self.is_missing_data = self.check_missing_data()
        self.show_chart = show_chart
        self.isIFRS = True if isIFRS(self.data) else False
        self.save_fig = save_fig
        self.save_path = save_path


    def reading_json(self, json_file_path: str) -> Dict[str, DataItem]:
        """
        jsonファイルを読み込んでBarchartのdataを返す関数

        Parameters
        ----------
        json_file_path: str
            jsonファイルのパス
        
        Returns
        -------
        data: Dict[str, DataItem]
            図のプロットに必要なデータが入った辞書
        """
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        data = {}
        for key, value in json_data.items():
            data[key] = DataItem(name=value['name'], value=value['value'], 
                                 unit=value['unit'], ifrs_flag=value['ifrs_flag'])
        return data
    
    
    def check_missing_data(self) -> Dict[str, bool]:
            is_missing_data = {}
            for key, value in self.data.items():
                is_missing_data[key] = value.value == -1
        
            return is_missing_data


    def plot(self) -> None:
        """
        jsonファイルの読み込みからグラフの作成まで行う関数
        """
        
        def billions(y, pos):
            """
            y軸の単位を十億円に変更するフォーマッター.
            """
            return f'{y * 1e-8:,.0f}億円'
        
        
        # figとaxオブジェクトを作成.
        fig, ax = plt.subplots(figsize=(9, 7))
        # y軸にフォーマッターを適用.
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(billions))
        
        # グラフのタイトルを設定.
        ax.set_title(f"{self.data['CompanyName'].value} 決算締日: {self.data['EndDate'].value}", fontsize=16, loc='center')
        if self.isIFRS:
            # 色の指定.
            colors = {
                'IFRSAssets': '#1f77b4',
                'IFRSNonCurrentAssets': '#468cb3',
                'IFRSCurrentAssets': '#aec7e8',
                'IFRSNetAssets': '#2ca02c',
                'IFRSLiabilities': '#d62728',
                'IFRSNonCurrentLiabilities': '#b41028',
                'IFRSCurrentLiabilities': '#ff9896',
                'IFRSInterest-bearingNonCurrentLiabilities': '#9467bd',
                'IFRSInterest-bearingCurrentLiabilities': '#c5b0d5',
                'IFRSSales': '#ff7f0e', 
                'IFRSOperatingProfits': '#d874ea',
                'IFRSNetIncome': '#f63ad6'
                }

            
            if self.show_chart == False:
                return

            # 貸借対照表(借方)の棒グラフ.
            if self.is_missing_data['IFRSAssets'] == False:
                bar_Assets = ax.bar(1, self.data['IFRSAssets'].value, width=1, color=colors['IFRSAssets'])[0]
                ax.text(bar_Assets.get_x() + bar_Assets.get_width() / 2, bar_Assets.get_height() / 2,
                        self.data['IFRSAssets'].name, ha='center', va='center', color='white', fontsize=12)
            if self.is_missing_data['IFRSNonCurrentAssets'] == False:
                bar_NonCurrentAssets = ax.bar(1.25, self.data['IFRSNonCurrentAssets'].value, width=0.5, color=colors['IFRSNonCurrentAssets'])[0]
            if self.is_missing_data['IFRSCurrentAssets'] == False:
                bar_CurrentAssets = ax.bar(1.25, self.data['IFRSCurrentAssets'].value, bottom=self.data['IFRSNonCurrentAssets'].value, width=0.5, color=colors['IFRSCurrentAssets'])[0]

            # 貸借対照表(貸方)の棒グラフ.
            if self.is_missing_data['IFRSNetAssets'] == False:
                bar_NetAssets = ax.bar(2, self.data['IFRSNetAssets'].value, width=1, color=colors['IFRSNetAssets'])[0]
            if self.is_missing_data['IFRSLiabilities'] == False:
                bar_Liabilities = ax.bar(2, 
                                         self.data['IFRSLiabilities'].value, bottom=self.data['IFRSNetAssets'].value, width=1,
                                         color=colors['IFRSLiabilities'])[0]
            if self.is_missing_data['IFRSNonCurrentLiabilities'] == False:
                bar_NonCurrentLiabilities = ax.bar(1.75, 
                                                   self.data['IFRSNonCurrentLiabilities'].value, bottom=self.data['IFRSNetAssets'].value, 
                                                   width=0.5, color=colors['IFRSNonCurrentLiabilities'])[0]
            if self.is_missing_data['IFRSCurrentLiabilities'] == False:
                bar_CurrentLiabilities = ax.bar(1.75, 
                                                self.data['IFRSCurrentLiabilities'].value, bottom=self.data['IFRSNonCurrentLiabilities'].value+self.data['IFRSNetAssets'].value, 
                                                width=0.5, color=colors['IFRSCurrentLiabilities'])[0]

            # 有利子負債の棒グラフ.
            if self.is_missing_data['IFRSInterest-bearingNonCurrentLiabilities'] == False:
                bar_InterestbearingNonCurrentLiabilities = ax.bar(2.75, 
                                                                  self.data['IFRSInterest-bearingNonCurrentLiabilities'].value, 
                                                                  bottom=bar_CurrentLiabilities.get_y()-self.data['IFRSInterest-bearingNonCurrentLiabilities'].value, 
                                                                  width=0.5, color=colors['IFRSInterest-bearingNonCurrentLiabilities'])[0]
            if self.is_missing_data['IFRSInterest-bearingCurrentLiabilities'] == False:
                bar_InterestbearingCurrentLiabilities = ax.bar(2.75, 
                                                               self.data['IFRSInterest-bearingCurrentLiabilities'].value, 
                                                               bottom=bar_CurrentLiabilities.get_y(), width=0.5, 
                                                               color=colors['IFRSInterest-bearingCurrentLiabilities'])[0]

            # 損益計算書の棒グラフ.
            if self.is_missing_data['IFRSSales'] == False:
                bar_Sales = ax.bar(4, self.data['IFRSSales'].value, width=1, color=colors['IFRSSales'])[0]
            if self.is_missing_data['IFRSOperatingProfits'] == False:
                bar_OperatingProfits = ax.bar(3.75, self.data['IFRSOperatingProfits'].value, width=0.5, color=colors['IFRSOperatingProfits'])[0]
            if self.is_missing_data['IFRSNetIncome'] ==  False:
                bar_NetIncome = ax.bar(4.25, self.data['IFRSNetIncome'].value, width=0.5, color=colors['IFRSNetIncome'])[0]

            # 貸借対照表(借方)につけるテキスト.
            if self.is_missing_data['IFRSNonCurrentAssets'] == False:
                ax.text(bar_NonCurrentAssets.get_x() + bar_NonCurrentAssets.get_width() / 2, bar_NonCurrentAssets.get_height() / 2,
                        self.data['IFRSNonCurrentAssets'].name, ha='center', va='center', color='black', fontsize=10)
            if self.is_missing_data['IFRSCurrentAssets'] == False:
                ax.text(bar_CurrentAssets.get_x() + bar_CurrentAssets.get_width() / 2,
                        bar_CurrentAssets.get_y() + bar_CurrentAssets.get_height() / 2,
                        self.data['IFRSCurrentAssets'].name, ha='center', va='center', color='black', fontsize=10)

            # 貸借対照表(貸方)につけるテキスト.
            if self.is_missing_data['IFRSNetAssets'] == False:
                ax.text(bar_NetAssets.get_x() + bar_NetAssets.get_width() / 2, bar_NetAssets.get_height() / 2,
                        self.data['IFRSNetAssets'].name, ha='center', va='center', color='white', fontsize=12)
            if self.is_missing_data['IFRSLiabilities'] == False:
                ax.text(bar_Liabilities.get_x() + bar_Liabilities.get_width() / 2, 
                        bar_Liabilities.get_y() + bar_Liabilities.get_height() / 2,
                        self.data['IFRSLiabilities'].name, ha='center', va='center', color='white', fontsize=12)
            if self.is_missing_data['IFRSNonCurrentLiabilities'] == False:
                ax.text(bar_NonCurrentLiabilities.get_x() + bar_NonCurrentLiabilities.get_width() / 2,
                        bar_NonCurrentLiabilities.get_y() + bar_NonCurrentLiabilities.get_height() / 2,
                        self.data['IFRSNonCurrentLiabilities'].name, ha='center', va='center', color='black', fontsize=10)
            if self.is_missing_data['IFRSCurrentLiabilities'] == False:
                ax.text(bar_CurrentLiabilities.get_x() + bar_CurrentLiabilities.get_width() / 2,
                        bar_CurrentLiabilities.get_y() + bar_CurrentLiabilities.get_height() / 2,
                        self.data['IFRSCurrentLiabilities'].name, ha='center', va='center', color='black', fontsize=10)

            # 有利子負債につけるテキスト.
            if self.is_missing_data['IFRSInterest-bearingNonCurrentLiabilities'] == False:
                ax.text(bar_InterestbearingNonCurrentLiabilities.get_x() + bar_InterestbearingNonCurrentLiabilities.get_width() / 2,
                        bar_InterestbearingNonCurrentLiabilities.get_y() + bar_InterestbearingNonCurrentLiabilities.get_height() / 2,
                        self.data['IFRSInterest-bearingNonCurrentLiabilities'].name, ha='center', va='center', color='black', fontsize=10)
            if self.is_missing_data['IFRSInterest-bearingCurrentLiabilities'] == False:
                ax.text(bar_InterestbearingCurrentLiabilities.get_x() + bar_InterestbearingCurrentLiabilities.get_width() / 2,
                        bar_InterestbearingCurrentLiabilities.get_y() + bar_InterestbearingCurrentLiabilities.get_height() / 2,
                        self.data['IFRSInterest-bearingCurrentLiabilities'].name, ha='center', va='center', color='black', fontsize=10)

            # 損益計算書につけるテキスト.
            if self.is_missing_data['IFRSSales'] == False:
                ax.text(bar_Sales.get_x() + bar_Sales.get_width() / 2, bar_Sales.get_height() / 2,
                        self.data['IFRSSales'].name, ha='center', va='center', color='white', fontsize=12)
            if self.is_missing_data['IFRSNetIncome'] == False:
                ax.text(bar_NetIncome.get_x() + 0.25, bar_NetIncome.get_height() / 2,
                        self.data['IFRSNetIncome'].name, ha='center', va='center', color='black', fontsize=10)
            if self.is_missing_data['IFRSOperatingProfits'] == False:
                ax.text(bar_OperatingProfits.get_x(), bar_OperatingProfits.get_height() / 2,
                        self.data['IFRSOperatingProfits'].name, ha='center', va='center', color='black', fontsize=10)
                    
            # B/SからP/Lに線を引く.
            if (self.is_missing_data['IFRSLiabilities'] or self.is_missing_data['IFRSSales']) == False:
                plt.plot([bar_Liabilities.get_x() + bar_Liabilities.get_width(), bar_Sales.get_x()],
                         [bar_Liabilities.get_y() + bar_Liabilities.get_height(), bar_Sales.get_height()],
                         color='#751d1f')
            # x軸の目盛りを消す.
            ax.get_xaxis().set_visible(False)

            # y軸のグリッドラインを追加
            ax.yaxis.grid(True, linestyle='--', color='gray', alpha=0.7)
            
            if True:
                plt.savefig(self.save_path)
                print(f"(in plot_web): Plot saved to {self.save_path}")

            return fig
        else:
                # 色の指定.
            colors = {
                'Assets': '#1f77b4',
                'NonCurrentAssets': '#468cb3',
                'CurrentAssets': '#aec7e8',
                'NetAssets': '#2ca02c',
                'Liabilities': '#d62728',
                'NonCurrentLiabilities': '#b41028',
                'CurrentLiabilities': '#ff9896',
                'Interest-bearingNonCurrentLiabilities': '#9467bd',
                'Interest-bearingCurrentLiabilities': '#c5b0d5',
                'Sales': '#ff7f0e', 
                'OperatingProfits': '#d874ea',
                'NetIncome': '#f63ad6'
                }
            
            
            if self.show_chart == False:
                return

            # 貸借対照表(借方)の棒グラフ.
            if self.is_missing_data['Assets'] == False:
                bar_Assets = ax.bar(1, self.data['Assets'].value, width=1, color=colors['Assets'])[0]
                ax.text(bar_Assets.get_x() + bar_Assets.get_width() / 2, bar_Assets.get_height() / 2,
                    self.data['Assets'].name, ha='center', va='center', color='white', fontsize=12)
            if self.is_missing_data['NonCurrentAssets'] == False:
                bar_NonCurrentAssets = ax.bar(1.25, self.data['NonCurrentAssets'].value, width=0.5, color=colors['NonCurrentAssets'])[0]
            if self.is_missing_data['CurrentAssets'] == False:
                bar_CurrentAssets = ax.bar(1.25, self.data['CurrentAssets'].value, bottom=self.data['NonCurrentAssets'].value, width=0.5, color=colors['CurrentAssets'])[0]


            # 貸借対照表(貸方)の棒グラフ.
            if self.is_missing_data['NetAssets'] == False:
                bar_NetAssets = ax.bar(2, self.data['NetAssets'].value, width=1, color=colors['NetAssets'])[0]
            if self.is_missing_data['Liabilities'] == False:
                bar_Liabilities = ax.bar(2, 
                                        self.data['Liabilities'].value, bottom=self.data['NetAssets'].value, width=1,
                                        color=colors['Liabilities'])[0]
            if self.is_missing_data['NonCurrentLiabilities'] == False:
                bar_NonCurrentLiabilities = ax.bar(1.75, 
                                                self.data['NonCurrentLiabilities'].value, bottom=self.data['NetAssets'].value, 
                                                width=0.5, color=colors['NonCurrentLiabilities'])[0]
            if self.is_missing_data['CurrentLiabilities'] == False:
                bar_CurrentLiabilities = ax.bar(1.75, 
                                                self.data['CurrentLiabilities'].value, bottom=self.data['NonCurrentLiabilities'].value+self.data['NetAssets'].value, 
                                                width=0.5, color=colors['CurrentLiabilities'])[0]


            # 有利子負債の棒グラフ.
            if self.is_missing_data['Interest-bearingNonCurrentLiabilities'] == False:
                bar_InterestbearingNonCurrentLiabilities = ax.bar(2.75, 
                                                                self.data['Interest-bearingNonCurrentLiabilities'].value, 
                                                                bottom=bar_CurrentLiabilities.get_y()-self.data['Interest-bearingNonCurrentLiabilities'].value, 
                                                                width=0.5, color=colors['Interest-bearingNonCurrentLiabilities'])[0]
            if self.is_missing_data['Interest-bearingCurrentLiabilities'] == False:
                bar_InterestbearingCurrentLiabilities = ax.bar(2.75, 
                                                            self.data['Interest-bearingCurrentLiabilities'].value, 
                                                            bottom=bar_CurrentLiabilities.get_y(), width=0.5, 
                                                            color=colors['Interest-bearingCurrentLiabilities'])[0]


            # 損益計算書の棒グラフ.
            if self.is_missing_data['Sales'] == False:
                bar_Sales = ax.bar(4, self.data['Sales'].value, width=1, color=colors['Sales'])[0]
            if self.is_missing_data['OperatingProfits'] == False:
                bar_OperatingProfits = ax.bar(3.75, self.data['OperatingProfits'].value, width=0.5, color=colors['OperatingProfits'])[0]
            if self.is_missing_data['NetIncome'] ==  False:
                bar_NetIncome = ax.bar(4.25, self.data['NetIncome'].value, width=0.5, color=colors['NetIncome'])[0]


            # 貸借対照表(借方)につけるテキスト.
            if self.is_missing_data['NonCurrentAssets'] == False:
                ax.text(bar_NonCurrentAssets.get_x() + bar_NonCurrentAssets.get_width() / 2, bar_NonCurrentAssets.get_height() / 2,
                    self.data['NonCurrentAssets'].name, ha='center', va='center', color='black', fontsize=10)
            if self.is_missing_data['CurrentAssets'] == False:
                ax.text(bar_CurrentAssets.get_x() + bar_CurrentAssets.get_width() / 2,
                    bar_CurrentAssets.get_y() + bar_CurrentAssets.get_height() / 2,
                    self.data['CurrentAssets'].name, ha='center', va='center', color='black', fontsize=10)

            # 貸借対照表(貸方)につけるテキスト.
            if self.is_missing_data['NetAssets'] == False:
                ax.text(bar_NetAssets.get_x() + bar_NetAssets.get_width() / 2, bar_NetAssets.get_height() / 2,
                    self.data['NetAssets'].name, ha='center', va='center', color='white', fontsize=12)
            if self.is_missing_data['Liabilities'] == False:
                ax.text(bar_Liabilities.get_x() + bar_Liabilities.get_width() / 2, 
                    bar_Liabilities.get_y() + bar_Liabilities.get_height() / 2,
                    self.data['Liabilities'].name, ha='center', va='center', color='white', fontsize=12)
            if self.is_missing_data['NonCurrentLiabilities'] == False:
                ax.text(bar_NonCurrentLiabilities.get_x() + bar_NonCurrentLiabilities.get_width() / 2,
                    bar_NonCurrentLiabilities.get_y() + bar_NonCurrentLiabilities.get_height() / 2,
                    self.data['NonCurrentLiabilities'].name, ha='center', va='center', color='black', fontsize=10)
            if self.is_missing_data['CurrentLiabilities'] == False:
                ax.text(bar_CurrentLiabilities.get_x() + bar_CurrentLiabilities.get_width() / 2,
                    bar_CurrentLiabilities.get_y() + bar_CurrentLiabilities.get_height() / 2,
                    self.data['CurrentLiabilities'].name, ha='center', va='center', color='black', fontsize=10)

            # 有利子負債につけるテキスト.
            if self.is_missing_data['Interest-bearingNonCurrentLiabilities'] == False:
                ax.text(bar_InterestbearingNonCurrentLiabilities.get_x() + bar_InterestbearingNonCurrentLiabilities.get_width() / 2,
                    bar_InterestbearingNonCurrentLiabilities.get_y() + bar_InterestbearingNonCurrentLiabilities.get_height() / 2,
                    self.data['Interest-bearingNonCurrentLiabilities'].name, ha='center', va='center', color='black', fontsize=10)
            if self.is_missing_data['Interest-bearingCurrentLiabilities'] == False:
                ax.text(bar_InterestbearingCurrentLiabilities.get_x() + bar_InterestbearingCurrentLiabilities.get_width() / 2,
                    bar_InterestbearingCurrentLiabilities.get_y() + bar_InterestbearingCurrentLiabilities.get_height() / 2,
                    self.data['Interest-bearingCurrentLiabilities'].name, ha='center', va='center', color='black', fontsize=10)

            # 損益計算書につけるテキスト.
            if self.is_missing_data['Sales'] == False:
                ax.text(bar_Sales.get_x() + bar_Sales.get_width() / 2, bar_Sales.get_height() / 2,
                    self.data['Sales'].name, ha='center', va='center', color='white', fontsize=12)
            if self.is_missing_data['NetIncome'] == False:
                ax.text(bar_NetIncome.get_x() + 0.25, bar_NetIncome.get_height() / 2,
                    self.data['NetIncome'].name, ha='center', va='center', color='black', fontsize=10)
            if self.is_missing_data['OperatingProfits'] == False:
                ax.text(bar_OperatingProfits.get_x(), bar_OperatingProfits.get_height() / 2,
                    self.data['OperatingProfits'].name, ha='center', va='center', color='black', fontsize=10)
                    
            # B/SからP/Lに線を引く.
            if (self.is_missing_data['Liabilities'] or self.is_missing_data['Sales']) == False:
                plt.plot([bar_Liabilities.get_x() + bar_Liabilities.get_width(), bar_Sales.get_x()],
                    [bar_Liabilities.get_y() + bar_Liabilities.get_height(), bar_Sales.get_height()],
                    color='#751d1f')

            # x軸の目盛りを消す.
            ax.get_xaxis().set_visible(False)

            # y軸のグリッドラインを追加
            ax.yaxis.grid(True, linestyle='--', color='gray', alpha=0.7)

            if self.save_fig:
                plt.savefig(self.save_path)

            return fig
