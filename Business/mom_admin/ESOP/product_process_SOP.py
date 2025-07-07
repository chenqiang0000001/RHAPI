import sys
import os
from pprint import pformat

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import requests
from Public.address.mom import *
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.get_token import get_token

class ProductProcessSOP:
    """
    产品工艺文档相关接口封装
    """
    def __init__(self):
        authorization = get_token()
        self.headers = {
            "authorization": authorization
        }
        self.logger = Logger(name="ProcessRelated").get_logger()
        self.logger.debug("初始化ProductProcessSOP类，已获取授权令牌")

    def upLoadESopFileMaterialCollection(self, file_path=r"D:\apiAutomationRH\test.pdf", material_code=MaterialCode, material_name=MaterialName):
        """
        上传物料文档
        """
        self.logger.debug(f"开始上传物料文档: 文件路径={file_path}, 物料编码={material_code}, 物料名称={material_name}")
        if not os.path.exists(file_path):
            self.logger.error(f"文件路径不存在: {file_path}")
            return None

        urlUpLoadESopFileMaterialCollection = url + apiUpLoadESopFileMaterialCollection
        try:
            with open(file_path, 'rb') as f:
                files = [
                    ('SopType', (None, '-1:ProductMaterialFile:SopData')),  # 物料文档类型
                    ('BusinessKey', (None, '-1:ProductMaterialFile')),
                    ('MaterialCode', (None, material_code)),
                    ('MaterialName', (None, material_name)),
                    ('IsEnable', (None, 'true')),
                    ('CompanyCode', (None, '00000')),
                    ('FactoryCode', (None, '00000.00001')),
                    ('Files', (os.path.basename(file_path), f, 'application/pdf'))
                ]
                self.logger.debug(f"完整请求体结构验证:\n{pformat(files, depth=2)}")
                response = requests.post(
                    url=urlUpLoadESopFileMaterialCollection,
                    headers=self.headers,
                    files=files
                )
                self.logger.debug(
                    f"[请求验证] 完整请求参数:\nURL: {urlUpLoadESopFileMaterialCollection}\n"
                    f"HEADERS: {self.headers}\n"
                    f"FILES: {pformat(files, depth=3)}\n"
                    "+"*50 + "\n"
                    f"[响应验证] 状态码: {response.status_code}\n"
                    f"响应头: {response.headers}\n"
                    f"原始响应: {response.text}"
                )
                try:
                    response_json = response.json()
                    if not response_json.get('Success'):
                        self.logger.error(f"接口业务逻辑失败: {response.text}")
                except ValueError:
                    self.logger.error(f"响应不是有效的JSON格式: {response.text}")
                response.raise_for_status()
                self.logger.info(f"产品工艺文档上传成功，状态码={response.status_code}")
                self.logger.info(f"物料文档审核成功，状态码={response.status_code}")
                self.logger.info(f"物料文档上传成功，状态码={response.status_code}")
                return response
            
        except FileNotFoundError as e:
            self.logger.error(f"文件未找到: {e}")
            return None
        except requests.RequestException as e:
            self.logger.error(f"文件上传请求失败: {str(e)}\nURL: {urlUpLoadESopFileMaterialCollection}\nHeaders: {self.headers}\nFiles: {files}")
            return None

    def AuditESopMaterialDatas(self, Material_documentation_id=1, MaterialCode=MaterialCode, MaterialName=MaterialName):
        """
        审核物料文档
        """
        self.logger.debug(f"开始审核物料文档: 文档ID={Material_documentation_id}, 物料编码={MaterialCode}, 物料名称={MaterialName}")
        uploads = {
            "MaterialCode": MaterialCode,
            "MaterialName": MaterialName,
            "SopStatus": "Pass",
            "SopType": "-1:ProductMaterialFile:SopData",
            "Id":Material_documentation_id
        }
        urlCreateProductInspectSchemaData = url + apiCreateProductInspectSchemaData
        try:
            response = requests.post(url=urlCreateProductInspectSchemaData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlCreateProductInspectSchemaData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def uploadProductProcessDocumentation(self, file_path=r"D:\apiAutomationRH\test.pdf", material_code=MaterialCode, process_routing_code=ProcessRoutingCode, process_code=ProcessCode, process_name=ProcessName):
        """
        上传产品工艺文档
        """
        self.logger.debug(f"开始上传产品工艺文档: 文件路径={file_path}, 物料编码={material_code}, 工艺路线编码={process_routing_code}, 工序编码={process_code}, 工序名称={process_name}")
        if not os.path.exists(file_path):
            self.logger.error(f"文件路径不存在: {file_path}")
            return None

        urlUpLoadESopFileProcessCollection = url + apiUpLoadESopFileProcessCollection
        try:
            with open(file_path, 'rb') as f:
                files = [
                    ('SopType', (None, '1:ProductProcessFile:SopData')),  # 严格匹配抓包成功格式
                    ('BusinessKey', (None, '1:ProductProcessFile')),
                    ('MaterialCode', (None, material_code)),
                    ('MaterialName', (None, f'Material-{material_code}')),  # 动态生成物料名称
                    ('ProcessRoutingCode', (None, process_routing_code)),
                    ('ProcessCode', (None, process_code)),
                    ('ProcessName', (None, process_name)),
                    ('IsEnable', (None, 'true')),
                    ('CompanyCode', (None, '00000')),
                    ('FactoryCode', (None, '00000.00001')),
                    ('Files', (os.path.basename(file_path), f, 'application/pdf'))
                ]
                self.logger.debug(f"完整请求体结构验证:\n{pformat(files, depth=2)}")
                response = requests.post(
                    url=urlUpLoadESopFileProcessCollection,
                    headers=self.headers,
                    files=files
                )
                self.logger.debug(
                    f"[请求验证] 完整请求参数:\nURL: {urlUpLoadESopFileProcessCollection}\n"
                    f"HEADERS: {self.headers}\n"
                    f"FILES: {pformat(files, depth=3)}\n"
                    "+"*50 + "\n"
                    f"[响应验证] 状态码: {response.status_code}\n"
                    f"响应头: {response.headers}\n"
                    f"原始响应: {response.text}"
                )
                try:
                    response_json = response.json()
                    if not response_json.get('Success'):
                        self.logger.error(f"接口业务逻辑失败: {response.text}")
                except ValueError:
                    self.logger.error(f"响应不是有效的JSON格式: {response.text}")
                response.raise_for_status()
                self.logger.info(f"产品工艺文档上传成功，状态码={response.status_code}")
                self.logger.info(f"物料文档审核成功，状态码={response.status_code}")
                self.logger.info(f"物料文档上传成功，状态码={response.status_code}")
                return response
            
        except FileNotFoundError as e:
            self.logger.error(f"文件未找到: {e}")
            return None
        except requests.RequestException as e:
            self.logger.error(f"文件上传请求失败: {str(e)}\nURL: {urlUpLoadESopFileProcessCollection}\nHeaders: {self.headers}\nFiles: {files}")
            return None

    def AuditESopMaterialProcessRoutingDatas(self, audit_data_list):
        """
        审核工艺路线ESOP文件
        :param audit_data_list: 审核数据列表（list of dict）
        """
        url_audit = url + "ESopApi/AuditESopMaterialProcessRoutingDatas"
        self.logger.debug(f"审核工艺路线ESOP文件，请求体: {audit_data_list}")
        try:
            response = requests.post(url=url_audit, headers=self.headers, json=audit_data_list)
            self.logger.debug(f"响应: 状态码={getattr(response, 'status_code', None)}, 内容={getattr(response, 'text', response)}")
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"审核工艺路线ESOP文件请求失败: {str(e)}\nURL: {url_audit}\nHeaders: {self.headers}\nBody: {audit_data_list}")
            return None

    def getESopMaterialAutoQueryDatas(self, material_code=MaterialCode, material_category_code="DQJ", page_size=10, page_index=1):
        """
        查询物料ESOP文件，返回接口原始响应
        """
        url_query = url + "ESopApi/GetESopMaterialAutoQueryDatas"
        body = {
            "MaterialCode": material_code,
            "MaterialCategoryCode": material_category_code,
            "MaterialName": "",
            "SopStatus": None,
            "IsPaged": True,
            "PageSize": page_size,
            "PageIndex": page_index,
            "CompanyCode": CompanyCode,
            "FactoryCode": "00000.00001"
        }
        self.logger.debug(f"查询物料ESOP文件，请求体: {body}")
        try:
            response = requests.post(url=url_query, headers=self.headers, json=body)
            self.logger.debug(f"响应: 状态码={getattr(response, 'status_code', None)}, 内容={getattr(response, 'text', response)}")
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"查询物料ESOP文件请求失败: {str(e)}\nURL: {url_query}\nHeaders: {self.headers}\nBody: {body}")
            return None

    def getESopMaterialProcessRoutingAutoQueryDatas(self, process_routing_code=ProcessRoutingCode, material_code=MaterialCode):
        """
        查询工艺路线ESOP文件，返回接口原始响应
        """
        url_query = url + "ESopApi/GetESopMaterialProcessRoutingAutoQueryDatas"
        body = {
            "ProcessRoutingCode": process_routing_code,
            "MaterialCode": material_code,
            "CompanyCode": CompanyCode,
            "FactoryCode": "00000.00001"
        }
        self.logger.debug(f"查询工艺路线ESOP文件，请求体: {body}")
        try:
            response = requests.post(url=url_query, headers=self.headers, json=body)
            self.logger.debug(f"响应: 状态码={getattr(response, 'status_code', None)}, 内容={getattr(response, 'text', response)}")
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"查询工艺路线ESOP文件请求失败: {str(e)}\nURL: {url_query}\nHeaders: {self.headers}\nBody: {body}")
            return None

if __name__ == '__main__':
    response = ProductProcessSOP().uploadProductProcessDocumentation(
        file_path=r"D:\apiAutomationRH\test.pdf",
        material_code="cecec",
        process_routing_code="cecec1-1",  # 确保这个值是有效的工艺路线编码
        process_code="GX001",             # 示例工序编码
        process_name="注塑工序"            # 示例工序名称
    )
    print(response.json()) 