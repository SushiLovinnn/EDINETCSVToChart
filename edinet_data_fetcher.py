from edinet import Edinet
from datetime import datetime
import json
import requests
import os
from dotenv import load_dotenv
import time

class Document:
    """
    メタデータの識別子です。

    Attributes:
        docID (str): 書類管理番号
        edinetCode (str): 提出者 EDINET コード
        secCode (str): 提出者証券コード
        JCN (str): 提出者法人番号
        filerName (str): 提出者名
        fundCode (str): ファンドコード
        ordinanceCode (str): 府令コード
        formCode (str): 様式コード
        docTypeCode (str): 書類種別コード
        periodStart (str): 期間（自）
        periodEnd (str): 期間（至）
        submitDateTime (str): 提出日時
        docDescription (str): 提出書類概要
        issuerEdinetCode (str): 発行会社 EDINET コード
        subjectEdinetCode (str): 対象 EDINET コード
        subsidiaryEdinetCode (str): 子会社 EDINET コード
        currentReportReason (str): 臨報提出事由
        parentDocID (str): 親書類管理番号
        opeDateTime (str): 操作日時
        withdrawalStatus (str): 取下区分
        docInfoEditStatus (str): 書類情報修正区分
        disclosureStatus (str): 開示不開示区分
        xbrlFlag (str): XBRL 有無フラグ
        pdfFlag (str): PDF 有無フラグ
        attachDocFlag (str): 代替書面・添付文書有無フラグ
        englishDocFlag (str): 英文ファイル有無フラグ
        csvFlag (str): CSV 有無フラグ
        legalStatus (str): 縦覧区分
        -------------------------
        詳しくはEDINET_APIの仕様書を参照してください。
    """

    def __init__(self, docID: str, edinetCode: str, secCode: str, JCN: str,
                 filerName: str, fundCode: str, ordinanceCode: str, formCode: str,
                 docTypeCode: str, periodStart: str, periodEnd: str, submitDateTime: str,
                 docDescription: str, issuerEdinetCode: str, subjectEdinetCode: str,
                 subsidiaryEdinetCode: str, currentReportReason: str, parentDocID: str,
                 opeDateTime: str, withdrawalStatus: str, docInfoEditStatus: str,
                 disclosureStatus: str, xbrlFlag: str, pdfFlag: str, attachDocFlag: str,
                 englishDocFlag: str, csvFlag: str, legalStatus: str):
        self.docID = docID
        self.edinetCode = edinetCode
        self.docDescription = docDescription
        self.secCode = secCode
        self.JCN = JCN
        self.filerName = filerName
        self.fundCode = fundCode
        self.ordinanceCode = ordinanceCode
        self.formCode = formCode
        self.docTypeCode = docTypeCode
        self.periodStart = periodStart
        self.periodEnd = periodEnd
        self.submitDateTime = submitDateTime
        self.issuerEdinetCode = issuerEdinetCode
        self.subjectEdinetCode = subjectEdinetCode
        self.subsidiaryEdinetCode = subsidiaryEdinetCode
        self.currentReportReason = currentReportReason
        self.parentDocID = parentDocID
        self.opeDateTime = opeDateTime
        self.withdrawalStatus = withdrawalStatus
        self.docInfoEditStatus = docInfoEditStatus
        self.disclosureStatus = disclosureStatus
        self.xbrlFlag = xbrlFlag
        self.pdfFlag = pdfFlag
        self.attachDocFlag = attachDocFlag
        self.englishDocFlag = englishDocFlag
        self.csvFlag = csvFlag
        self.legalStatus = legalStatus

    def __str__(self):
        return f"{self.secCode}: {self.filerName} ({self.docID})"

class EdinetDataFetcher():
    def __init__(self, dates_string: str, sleep_time=1):   
        self.date_string = dates_string
        self.sleep_time = sleep_time
        """
        Args:
        dates_string (str): 取得する日付の文字列（YYYY-MM-DD）.
        sleep_time (int): スリープ時間（秒）デフォルトは1秒.
        """
    
    def fetch_data(self):
        # .envファイルから環境変数を読み込む
        load_dotenv()

        # APIのトークンを環境変数から取得
        API_TOKEN = os.getenv("API_TOKEN")

        if not API_TOKEN:
            raise ValueError("API_TOKEN is not set in the environment variables")

        edn = Edinet(API_TOKEN)

        # ドキュメントのリストを取得
        specified_date = datetime.strptime(self.date_string, "%Y-%m-%d")
        doc_list = edn.get_document_list(specified_date, type_=2)

        for document in doc_list["results"]:
            doc = Document(
                docID=document["docID"],
                edinetCode=document["edinetCode"],
                secCode=document["secCode"],
                JCN=document["JCN"],
                filerName=document["filerName"],
                fundCode=document["fundCode"],
                ordinanceCode=document["ordinanceCode"],
                formCode=document["formCode"],
                docTypeCode=document["docTypeCode"],
                periodStart=document["periodStart"],
                periodEnd=document["periodEnd"],
                submitDateTime=document["submitDateTime"],
                docDescription=document["docDescription"],
                issuerEdinetCode=document["issuerEdinetCode"],
                subjectEdinetCode=document["subjectEdinetCode"],
                subsidiaryEdinetCode=document["subsidiaryEdinetCode"],
                currentReportReason=document["currentReportReason"],
                parentDocID=document["parentDocID"],
                opeDateTime=document["opeDateTime"],
                withdrawalStatus=document["withdrawalStatus"],
                docInfoEditStatus=document["docInfoEditStatus"],
                disclosureStatus=document["disclosureStatus"],
                xbrlFlag=document["xbrlFlag"],
                pdfFlag=document["pdfFlag"],
                attachDocFlag=document["attachDocFlag"],
                englishDocFlag=document["englishDocFlag"],
                csvFlag=document["csvFlag"],
                legalStatus=document["legalStatus"]
            )
            #書類がCSVファイルで、縦覧可能で、有価証券報告書で、ファンドでない場合にcsvファイルを取得.
            if doc.csvFlag == '1' and doc.legalStatus == '1' and doc.docTypeCode == "120" and doc.fundCode is None:
                print(doc)
                doc_data = edn.get_document(doc.docID, 5)
                with open(f"ZIPs/{doc.docID}.zip", "wb") as f:
                    f.write(doc_data)
                time.sleep(self.sleep_time)
