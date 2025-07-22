import requests
from Public.address.mom import get_url, pdaUrl, apiScanLabel, apiLabelSplit
from Toolbox.log_module import Logger
from Toolbox.config_headers import get_headers

class LabelOperation:
    """
    PDA标签相关接口封装
    """
    def __init__(self, timezone=None):
        self.headers = get_headers(timezone=timezone)
        self.logger = Logger(name="LabelOperation").get_logger()

    def scan_label(self, sn):
        """
        扫描标签
        """
        uploads = {
            "SN": sn,
            "OpBusinessType": "LabelSplitLabel",
            "FactoryCode": "00000.00001",
            "CompanyCode": "00000"
        }
        url_scan = pdaUrl + apiScanLabel
        try:
            response = requests.post(url=url_scan, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"扫描标签请求失败: {str(e)}\nURL: {url_scan}\nHeaders: {self.headers}\nBody: {uploads}")
            return None

    def label_split(self, split_body):
        """
        标签拆分
        :param split_body: dict，标签拆分完整请求体
        """
        url_split = pdaUrl + apiLabelSplit
        try:
            response = requests.post(url=url_split, headers=self.headers, json=split_body)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"标签拆分请求失败: {str(e)}\nURL: {url_split}\nHeaders: {self.headers}\nBody: {split_body}")
            return None 