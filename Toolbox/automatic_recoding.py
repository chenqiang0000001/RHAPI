import requests
import random
import json
from datetime import datetime, timedelta
from get_token import get_token

class AutomaticRecodingTool:
    """
    SPC自动数据录入工具类
    """
    def __init__(self):
        # 配置项
        self.config = {
            # API地址配置
            "api_url": "http://192.168.0.135:8282/SpcDataAnalysisApi/StoreSpcAcquireDataLibData",
            # SPC项目编码
            "spc_item_code": "hkyceshi001",
            # SPC项目名称
            "spc_item_name": "轴承内径-移动极差图",
            # 物料编码
            "material_code": "Zh-Test-03",
            # 设备编码
            "equipment_code": "A135",
            # 开始日期
            "start_date": "2025-06-01",
            # 结束日期
            "end_date": "2025-07-31",
            # 检验项目编码
            "inspect_item_code": "CESHI02",
            # 检验项目名称
            "inspect_item_name": "卷心菜测试项目02",
            # 公司编码
            "company_code": "00000",
            # 工厂编码
            "factory_code": "00000.00001",
            # 创建人用户ID
            "creator_user_id": 10402,
            # 创建人用户名
            "creator_user_name": "CQ",
            # 创建人真实姓名
            "creator_real_name": "陈强",
            # 每条记录中的随机数值数量
            "data_count": 10,
            # 随机数最小值
            "min_value": 100,
            # 随机数最大值
            "max_value": 111,
            # 要提交的数据记录数量
            "record_count": 1    # 默认为1条记录
        }
        # 请求头
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": get_token()
            # 如需认证，请在此处添加Authorization头
        }

    def generate_random_data(self, count):
        """生成指定数量的随机数值"""
        return [random.randint(self.config["min_value"], self.config["max_value"]) for _ in range(count)]

    def create_request_payload(self, random_data):
        """构建API请求体"""
        current_time = datetime.utcnow().isoformat() + "Z"
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        date_time_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.728Z")

        # 构建检测数据字典
        inspect_data = {}
        for i, value in enumerate(random_data, 1):
            inspect_data[f"InspectData{i}"] = value
        # 填充剩余的检测数据字段为null
        for i in range(len(random_data)+1, 11):
            inspect_data[f"InspectData{i}"] = None

        payload = {
            "SpcItemCode": self.config["spc_item_code"],
            "SpcItemName": self.config["spc_item_name"],
            "MaterialCode": self.config["material_code"],
            "EquipmentCode": self.config["equipment_code"],
            "StartInspectDateRange": [self.config["start_date"], self.config["end_date"]],
            "InspectDataCode": None,
            "MaterialName": self.config["material_code"],
            "MaterialSpecification": None,
            "EquipmentName": "高温注塑机",
            "ProcessCode": "Zh-Test-03",
            "ProcessName": "Zh-Test-03",
            "InspectItemCode": self.config["inspect_item_code"],
            "InspectItemName": self.config["inspect_item_name"],
            "SampleQty": 0,
            "StartInspectDate": date_time_str,
            "StartInspectTime": date_time_str,
            "EndInspectDate": None,
            "EndInspectTime": None,
            "InspectDataType": None,
            "MaxValue": self.config["max_value"],
            "MinValue": self.config["min_value"],
            "ToleranceValue": self.config["max_value"] - self.config["min_value"],
            "CentralValue": (self.config["max_value"] + self.config["min_value"]) / 2,
            "ControlUpperValue": 280.9840442773028,
            "ControlLowerValue": -69.9840442773028,
            "CenterLineValue": (self.config["max_value"] + self.config["min_value"]) / 2,
            "StandardDeviationValue": 58.4946814257676,
            **inspect_data,
            "CreatorUserId": self.config["creator_user_id"],
            "CreatorUserName": self.config["creator_user_name"],
            "CreatorUserRealName": self.config["creator_real_name"],
            "CreationTime": current_time,
            "LastModifierUserId": None,
            "LastModifierUserName": None,
            "LastModifierUserRealName": None,
            "LastModificationTime": None,
            "CompanyCode": self.config["company_code"],
            "FactoryCode": self.config["factory_code"],
            "NeedUpdateFields": None,
            "Id": 0,
            "Remark": None,
            "IsAdd": True,
            "isEdit": True,
            "__saveRule": True,
            "__saveRule_disable": False,
            "__cancelSave": True,
            "__cancelSave_disable": False,
            "__editRule": False,
            "__deleteRule": False,
            "expand": False,
            "index": 1,
            "MaxCount": 5,
            "ControlChart": "10",
            "IsSampling": True,
            "SamplingRuleCode": "QYGZ001",
            "SamplingRuleName": "QYGZ001",
            "GroupQty": 0,
            "EachGroupQty": 0,
            "JudgementRuleCode": "PY003",
            "JudgementRuleName": "PY003",
            "AlarmRuleCode": "GJ003",
            "AlarmRuleName": "GJ003",
            "AllSampleQty": 70,
            "MeanValue": 31.82857142857143,
            "Pp": 0.03134188081116257,
            "Ppk": -0.3884765070931631,
            "Ppm": 1087951.083361293,
            "Ppl": -0.3884765070931631,
            "Ppu": 0.45116026871548826,
            "Cpm": 0.019489096590894428,
            "Cp": 0.03134188081116257,
            "Ca": -12.394805194805194,
            "Cpk": -0.3884765070931631,
            "Cpl": -0.3884765070931631,
            "Cpu": 0.45116026871548826
        }
        return payload

    def send_request(self, payload):
        """发送POST请求到API"""
        try:
            response = requests.post(
                url=self.config["api_url"],
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"请求发生错误: {e}")
            print(f"请求URL: {self.config['api_url']}")
            print(f"请求体: {json.dumps(payload, indent=2, ensure_ascii=False)}")
            return None

    def run(self, data_count=None, record_count=None):
        """运行自动补录工具

        参数:
            data_count: 每条记录中的随机数值数量，若为None则使用配置中的默认值
            record_count: 要提交的数据记录数量，若为None则使用配置中的默认值
        """
        # 使用指定的数据数量或配置中的默认值
        data_count = data_count if data_count is not None else self.config["data_count"]
        # 使用指定的记录数量或配置中的默认值
        record_count = record_count if record_count is not None else self.config["record_count"]

        results = []
        for i in range(record_count):
            print(f"正在提交第{i+1}/{record_count}条记录...")
            # 生成随机数据
            random_data = self.generate_random_data(data_count)
            # 创建请求体
            payload = self.create_request_payload(random_data)
            # 发送请求
            response = self.send_request(payload)
            # 处理响应
            if response:
                print(f"第{i+1}条记录提交成功!")
                print(f"响应结果: {json.dumps(response, indent=2, ensure_ascii=False)}")
                results.append(response)
            else:
                print(f"第{i+1}条记录提交失败")

        if results:
            print(f"所有记录提交完成，成功{len(results)}/{record_count}条")
            return results
        else:
            print("所有记录提交失败")
            return None

if __name__ == "__main__":
    # 创建工具实例
    tool = AutomaticRecodingTool()
    # 运行SPC自动数据录入工具，可通过参数指定每条记录的数据数量和总记录数
    # 例如: tool.run(data_count=5, record_count=3) 表示生成3条记录，每条包含5个随机数
    tool.run(data_count=10, record_count=5)  # 使用配置中的默认值