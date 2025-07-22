import requests
from Public.address.mom import get_url, apiStoreAndonCallHandleRulesData, apiRemoveBatchAndonCallHandleRulesDatas, \
    apiGetAndonCallHandleRulesAutoQueryDatas, apiUpdateAndonCallCategoryParametersData
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.config_headers import get_headers

class LightingConfiguration:
    """
    安灯配置维护
    """
    def __init__(self, timezone=None):
        self.headers = get_headers(timezone=timezone)
        self.logger = Logger(name="FactoryModel").get_logger()
        self.url = get_url()

    def StoreAndonCallHandleRulesData(self,OrganizationStructureCode=OrganizationStructureCode, OrganizationStructureName=OrganizationStructureName):
        """
        新增安灯规则
        :param OrganizationStructureCode: 车间编码
        :param OrganizationStructureName: 车间名称
        :return: 响应对象
        """
        uploads = {
            "CallRuleLevelName": "自动化测试安灯",
            "CallRuleGrade": 1,
            "CallCategoryCode": "ZDH",
            "CallCategoryName": "自动化测试一级分类",
            "CallCategoryItemCode": "ZDH02",
            "CallCategoryItemName": "自动化测试二级分类",
            "OrganizationStructureCode": OrganizationStructureCode,
            "OrganizationStructureName": OrganizationStructureName,
            "OrganizationStructureExternalCode": "",
            "ResponsePersonCode": "CQ",
            "ResponsePersonName": "CQ",
            "ResponseGroupCode": "AndonResponseGroup",
            "ResponseGroupName": "安灯响应组",
            "StartProcessorCode": "CQ",
            "StartProcessorName": "CQ",
            "StartProcessorGroupCode": "AndonStartProcessGroup",
            "StartProcessorGroupName": "安灯开始处理组",
            "EndProcessorCode": "CQ",
            "EndProcessorName": "CQ",
            "EndProcessorGroupCode": "AndonEndProcessGroup",
            "EndProcessorGroupName": "安灯结束处理组",
            "CheckerCode": "CQ",
            "CheckerName": "CQ",
            "CheckerGroupCode": "AndonConfirmGroup",
            "CheckerGroupName": "安灯确认组",
            "BusinessProcessFlowName": "",
            "OpSign": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreAndonCallHandleRulesData = self.url + apiStoreAndonCallHandleRulesData
        try:
            response = requests.post(url=urlStoreAndonCallHandleRulesData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"新建安灯规则响应{response.json()}")
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStoreAndonCallHandleRulesData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def GetAndonCallHandleRulesAutoQueryDatas(self):
        """
        查询安灯规则
        :return: 响应对象
        """
        uploads = {
            "CallRuleLevelCode": "",
            "CallCategoryCode": None,
            "CallCategoryItemCode": "",
            "CallCategoryItemName": "",
            "IsPaged": True,
            "PageSize": 10,
            "PageIndex": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlGetAndonCallHandleRulesAutoQueryDatas = self.url + apiGetAndonCallHandleRulesAutoQueryDatas
        try:
            response = requests.post(url=urlGetAndonCallHandleRulesAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlGetAndonCallHandleRulesAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def RemoveBatchAndonCallHandleRulesDatas(self,Id):
        """
        删除安灯规则
        :return: 响应对象
        """
        uploads = [{
            "CallRuleGrade": 1,
            "CallRuleLevelCode": "AdR202507100053",
            "CallRuleLevelName": "测试安灯",
            "CallCategoryCode": "ZDH",
            "CallCategoryName": "自动化测试一级分类",
            "CallCategoryItemCode": "ZDH02",
            "CallCategoryItemName": "自动化测试二级分类",
            "OrganizationStructureCode": "00000.00001.00001",
            "OrganizationStructureName": "注塑车间",
            "OrganizationStructureExternalCode": "",
            "ResponseGroupCode": "AndonResponseGroup",
            "ResponseGroupName": "安灯响应组",
            "ResponsePersonCode": "CQ",
            "ResponsePersonName": "CQ",
            "StartProcessorCode": "CQ",
            "StartProcessorName": "CQ",
            "StartProcessorGroupCode": "AndonStartProcessGroup",
            "StartProcessorGroupName": "安灯开始处理组",
            "EndProcessorCode": "CQ",
            "EndProcessorName": "CQ",
            "EndProcessorGroupCode": "AndonEndProcessGroup",
            "EndProcessorGroupName": "安灯结束处理组",
            "CheckerGroupCode": "AndonConfirmGroup",
            "CheckerGroupName": "安灯确认组",
            "CheckerCode": "CQ",
            "CheckerName": "CQ",
            "IsUsePushDownStrategy": False,
            "UnResponsePushDownTime": None,
            "UnResponsePushDownTimeUnit": None,
            "NextRuleLevelCode": None,
            "NextRuleLevelName": "",
            "IsUseIntegrateBusinessFlow": False,
            "BusinessProcessFlowCode": None,
            "BusinessProcessFlowName": "",
            "CallRuleLevelStatus": "Created",
            "Auditor": None,
            "AuditTime": None,
            "CreatorUserId": 10402,
            "CreatorUserName": "CQ",
            "CreatorUserRealName": "陈强",
            "CreationTime": "2025-07-10T13:28:13.593+08:00",
            "LastModifierUserId": None,
            "LastModifierUserName": None,
            "LastModifierUserRealName": "",
            "LastModificationTime": None,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {},
            "Id": Id,
            "Remark": "",
            "expand": False,
            "index": 1,
            "select": False,
            "__edit": True,
            "__edit_disable": False,
            "__delete": True,
            "__delete_disable": False
        }]

        urlRemoveBatchAndonCallHandleRulesDatas = self.url + apiRemoveBatchAndonCallHandleRulesDatas
        try:
            response = requests.post(url=urlRemoveBatchAndonCallHandleRulesDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlRemoveBatchAndonCallHandleRulesDatas}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def UpdateAndonCallCategoryParametersData(self,OrganizationStructureCode=OrganizationStructureParentCode, OrganizationStructureName=OrganizationStructureName):
        """
        更新andon二级类别参数
        :return: 响应对象
        """
        uploads = {
            "CallCategoryCode": "ZDH",
            "CallCategoryName": "自动化测试一级分类",
            "CallCategoryItemCode": "ZDH02",
            "CallCategoryItemName": "自动化测试二级分类",
            "IsUse": True,
            "OrganizationStructureCode": OrganizationStructureCode,
            "OrganizationStructureName": OrganizationStructureName,
            "OrganizationStructureExternalCode": None,
            "CreatorUserId": 10402,
            "CreatorUserName": "CQ",
            "CreatorUserRealName": "陈强",
            "CreationTime": "2025-06-13T14:11:30.897+08:00",
            "LastModifierUserId": 10402,
            "LastModifierUserName": "CQ",
            "LastModifierUserRealName": "陈强",
            "LastModificationTime": "2025-07-10T13:38:49.527+08:00",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {
                "OrganizationStructureName": OrganizationStructureName,
                "Id": 64
            },
            "Id": 64,
            "Remark": "",
            "expand": False,
            "index": 1,
            "select": False,
            "__edit": True,
            "__edit_disable": False,
            "__delete": True,
            "__delete_disable": False
        }
        UpdateAndonCallCategoryParametersData = self.url + apiUpdateAndonCallCategoryParametersData
        try:
            response = requests.post(url=UpdateAndonCallCategoryParametersData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {UpdateAndonCallCategoryParametersData}，请求头: {self.headers}，请求体: {uploads}")
            raise e



if __name__ == '__main__':
    res = LightingConfiguration().UpdateAndonCallCategoryParametersData()
    # res1 = LightingConfiguration().GetAndonCallHandleRulesAutoQueryDatas()
    # id = res1.json()['Attach'][0]['Id']
    # res2 = LightingConfiguration().RemoveBatchAndonCallHandleRulesDatas(27)
    print(res.json())
    # print(res1.json())
    # print(id)
    # print(res2.json())