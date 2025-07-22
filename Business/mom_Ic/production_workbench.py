import requests
from Public.address.mom import get_url, apiGetCanProductionDispatchOrderDatas, apiStartProduction, \
    apiScanFeedingMaterialLabelData, apiProductionReport, apiCreateFirstInspectOrder, apiCompletedProduction, \
    apiGetESopMaterialProcessRoutingAutoQueryDatas, apiGetProductionDispatchOrderDataByCode, \
    apiStoreFeedingMaterialLabelDatas
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.config_headers import get_headers

class SingleUnitMaterial:
    """
    单机单料相关接口
    """
    def __init__(self, timezone=None):
        self.headers = get_headers(timezone=timezone)
        self.logger = Logger(name="FactoryModel").get_logger()

    def getCanProductionDispatchOrderDatas(self):
        """
        查询选择派工单
        :param self:
        :param OrganizationStructureCode: 组织架构编码
        :param EquipmentCode: 设备编码
        :param CompanyCode: 公司编码
        :param FactoryCode: 工厂编码
        """
        uploads = {
            "OrganizationStructureCode": OrganizationStructureCode,
            "EquipmentCode": EquipmentCode,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlGetCanProductionDispatchOrderDatas = get_url() + apiGetCanProductionDispatchOrderDatas
        try:
            response = requests.post(url=urlGetCanProductionDispatchOrderDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlGetCanProductionDispatchOrderDatas}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def getProductionDispatchOrderDataByCode(self,ProductionDispatchCode,ProductionPlanCode):
        """
        查询派工单详情
        :ProductionDispatchCode: 派工单编码
        :param ProductionPlanCode: 生产计划编码
        """
        uploads = {
            "ProductionDispatchCode": ProductionDispatchCode,
            "ProductionPlanCode": ProductionPlanCode,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlGetProductionDispatchOrderDataByCode = get_url() + apiGetProductionDispatchOrderDataByCode
        try:
            response = requests.post(url=urlGetProductionDispatchOrderDataByCode, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlGetProductionDispatchOrderDataByCode}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def getESopMaterialProcessRoutingAutoQueryDatas(self,):
        """
        查看ESOP文件
        """
        uploads = {
            "ProcessRoutingCode": ProcessRoutingCode,
            "MaterialCode": MaterialCode,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlGetESopMaterialProcessRoutingAutoQueryDatas = get_url() + apiGetESopMaterialProcessRoutingAutoQueryDatas
        try:
            response = requests.post(url=urlGetESopMaterialProcessRoutingAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlGetESopMaterialProcessRoutingAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def startProduction(self, dispatch_code, plan_code, process_task_code, process_code, process_name, workshop_code,equipment_code, equipment_name, assign_work_id,**kwargs):
        """
        启动生产，所有参数均为动态传入
        :param dispatch_code: 派工单编码
        :param plan_code: 生产计划编码
        :param process_task_code: 工序任务单编码
        :param process_code: 工序编码
        :param process_name: 工序名称
        :param process_seq: 工序顺序
        :param workshop_code: 车间编码
        :param workshop_name: 车间名称
        :param production_line_code: 产线编码
        :param production_line_name: 产线名称
        :param equipment_code: 设备编码
        :param equipment_name: 设备名称
        :param organization_structure_code: 组织结构编码
        :param organization_structure_name: 组织结构名称
        :param assign_work_id: 派工单ID
        :param kwargs: 其它可选参数
        """
        uploads = {
            "IsUsePackingList": False,
            "IsExportFlowCard": True,
            "IsPauseDataGather": False,
            "AuxiliaryEmployeeList": [],
            "IsSingleMachine": False,
            "MaterialShrinkImage": None,
            "ProductionDispatchCode": dispatch_code,
            "BindProductionDispatchCode": None,
            "ProcessTaskCode": process_code,
            "LastProcessTaskCode": None,
            "NextProcessTaskCode": process_task_code,
            "ProcessCode": process_code,
            "ProcessName": process_name,
            "ProcessSeq": 1,
            "ProcessRoutingEntryCode": "792a9a37-3faa-4d58-8c9f-cf374e91f7b0",
            "ProductionPlanCode":plan_code,
            "ErpProductionPlanCode": None,
            "ErpProductionPlanRowNo": None,
            "ErpProductionPlanRowNoId": 0,
            "SaleOrderCode": "",
            "SaleOrderRowNo": None,
            "RelationProductionCode": None,
            "RelationProductionRowNo": None,
            "ProductionType": "Normal",
            "PlanCategory": None,
            "PlanScheduler": None,
            "ProcessRoutingCode": ProcessRoutingCode2,
            "ProcessRoutingName": ProcessRoutingName,
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "ProductSpecification": "",
            "MaterialDrawCode": None,
            "ProductionPlanSource": None,
            "PlanStartDate": "2025-06-26T00:00:00+08:00",
            "PlanStartTime": "2025-06-26T00:00:00+08:00",
            "PlanEndDate": "2025-06-30T00:00:00+08:00",
            "PlanEndTime": "2025-06-30T00:00:00+08:00",
            "ActualStartDate": None,
            "ActualStartTime": None,
            "ActualEndDate": None,
            "ActualEndTime": None,
            "PlanIssuedDate": "2025-06-26T00:00:00+08:00",
            "PlanIssuedTime": "2025-06-26T08:58:52.68+08:00",
            "PlanClosedDate": None,
            "PlanClosedTime": None,
            "PlanQty": 88,
            "DispatchQty": 88,
            "CompeletedQty": 0,
            "UnCompeletedQty": 88,
            "GoodQty": 0,
            "BadQty": 0,
            "ScrappedQty": 0,
            "OneGoodQty": 0,
            "OneBadQty": 0,
            "OneScrappedQty": 0,
            "ReworkGoodQty": 0,
            "ReworkBadQty": 0,
            "ReworkScrappedQty": 0,
            "ActualInputQty": 0,
            "ActualOutPutQty": 0,
            "InWarehouseQty": 0,
            "AcquireQty": 0,
            "DifferQty": 0,
            "PackingListLabelPrintQty": 0,
            "OrderStatus": "WaitProduct",
            "ControlStatus": "Enable",
            "ControlReason": None,
            "OrganizationStructureCode": "00000.00001.00001",
            "OrganizationStructureName": workshop_code,
            "OrganizationStructureDisplayName": None,
            "OrganizationStructureExternalCode": None,
            "WorkShopInfoCode": "00000.00001.00001",
            "WorkShopInfoName": workshop_code,
            "ProductionLineCode": None,
            "ProductionLineName": None,
            "EquipmentCode": equipment_code,
            "EquipmentName": equipment_name,
            "OperatorCode": "CQ",
            "OperatorName": "CQ",
            "ClassShiftCode": None,
            "ClassShiftName": None,
            "ClassTypeCode": None,
            "ClassTypeName": None,
            "ClassGroupCode": None,
            "ClassGroupName": None,
            "EmergencySort": 0,
            "DispatcherCode": "CQ",
            "DispatcherName": "陈强",
            "DispatchTime": "2025-06-26T08:58:21.637+08:00",
            "DispatchDate": "2025-06-26T00:00:00+08:00",
            "MouldCode": "hcx-20250516-01",
            "MouldName": "hcx-20250516-01",
            "MouldSpecification": None,
            "AuxiliaryEmployee": "",
            "PlanTimeRange": None,
            "LastAcquireTime": None,
            "IsKeyComponent": False,
            "SnList": None,
            "CreatorUserId": 10402,
            "CreatorUserName": "CQ",
            "CreatorUserRealName": "陈强",
            "CreationTime": "2025-06-26T08:58:21.933+08:00",
            "LastModifierUserId": 10402,
            "LastModifierUserName": "CQ",
            "LastModifierUserRealName": "陈强",
            "LastModificationTime": "2025-06-26T08:58:52.68+08:00",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {},
            "Id": assign_work_id,
            "Remark": ""
        }
        print(f"开工请求参数: {uploads}")
        uploads.update(kwargs)
        urlStartProduction = get_url() + apiStartProduction
        try:
            response = requests.post(url=urlStartProduction, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStartProduction}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def scanFeedingMaterialLabelData(self,SN):
        """
        扫描投料物料标签
        """
        uploads = {
            "SN":SN
        }
        urlScanFeedingMaterialLabelData = get_url() + apiScanFeedingMaterialLabelData
        try:
            response = requests.post(url=urlScanFeedingMaterialLabelData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlScanFeedingMaterialLabelData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def storeFeedingMaterialLabelDatas(self,ProductionDispatchCode,SN):
        """
        确认上料
        """
        uploads = {
            "ProductionDispatchCode": ProductionDispatchCode,
            "LabelDtos": [{
                "InventoryQty": 1,
                "FreezeQty": 0,
                "AvailableQty": 0,
                "TraySN": None,
                "GroupingTrayTime": None,
                "GroupingCreatorCode": None,
                "GroupingCreatorName": None,
                "IsTray": False,
                "SN": SN,
                "LabelType": "PurchaseMaterialLabel",
                "OrderId": None,
                "OrderCode": "PurR20250417009",
                "OrderRowNum": "5",
                "SourceOrderId": None,
                "SourceOrderRowNum": "556",
                "LabelQty": 1,
                "MaterialCode": "CQ-20250319",
                "MaterialName": "CQ-20250319",
                "MaterialSpecification": "",
                "MeasureUnit": None,
                "PackageQty": 801,
                "LotNum": "25271701",
                "LotNumDate": None,
                "WarehouseCode": None,
                "WarehouseName": None,
                "WarehouseAreaCode": None,
                "WarehouseAreaName": None,
                "WarehouseShelfCode": None,
                "WarehouseShelfName": None,
                "StorageLocationCode": None,
                "StorageLocationName": None,
                "SupplierCode": "zdh",
                "SupplierName": "自动化测试供应商（勿动）",
                "SupplierLotNum": "",
                "PurchaseDate": "2025-04-17T09:27:45.827+08:00",
                "OrderCreateDate": None,
                "CustomerCode": None,
                "CustomerName": None,
                "DeliveryDate": None,
                "OrganizationStructureCode": None,
                "OrganizationStructureDisplayName": None,
                "OrganizationStructureName": None,
                "ProductDate": None,
                "ProductionType": None,
                "PlanStartDate": None,
                "PlanEndDate": None,
                "ResourceName": None,
                "ResourceCode": None,
                "PlanScheduler": None,
                "WorkCenterCode": None,
                "WorkCenterName": None,
                "NeededQty": None,
                "HadDoneQty": None,
                "CurrentStatus": None,
                "BusinessStatus": None,
                "ManageOpStatus": None,
                "UpperLimit": None,
                "LowwerLimit": None,
                "PrintTemplateSpecify": None,
                "FactoryCode": "00000.00001",
                "PrintTemplateCode": "天安0401",
                "PrintTemplateName": "天安0401",
                "PrintTemplateId": "174",
                "MaterialAttribute": None,
                "MaterialCategory": None,
                "ExpiryDays": 0,
                "ExpiryUnit": None,
                "ExpirationDate": None,
                "RelativeOrderCode": None,
                "RelativeOrderRowNum": None,
                "InventoryAuxQty": 0,
                "OpSign": 1
            }],
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreFeedingMaterialLabelDatas = get_url() + apiStoreFeedingMaterialLabelDatas
        try:
            response = requests.post(url=urlStoreFeedingMaterialLabelDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStoreFeedingMaterialLabelDatas}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def productionReport(self,ProductionDispatchCode):
        """
        生产报工
        :param ProductionDispatchCode: 派工单编码
        """
        uploads = {
            "OneGoodQty": 99,
            "OpSign": 1,
            "ApplianceCode": None,
            "ReportUserCode": "CQ",
            "ReportUserName": "CQ",
            "IsUsingReportAndLoading":False,
            "ProductionDispatchCode": ProductionDispatchCode,
            "WorkShopInfoName": OrganizationStructureCode,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlProductionReport = get_url() + apiProductionReport
        try:
            response = requests.post(url=urlProductionReport, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlProductionReport}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def createFirstInspectOrder(self,ProductionDispatchCode):
        """
        发起首检
        """
        uploads = {
            "OneGoodQty": 7,
            "OpSign": 1,
            "ReportUserCode": "CQ",
            "ReportUserName": "CQ",
            "ProductionDispatchCode": ProductionDispatchCode,
            "EquipmentCode": EquipmentCode,
            "EquipmentName": EquipmentName,
            "WorkShopInfoName": OrganizationStructureCode,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlCreateFirstInspectOrder = get_url() + apiCreateFirstInspectOrder
        try:
            response = requests.post(url=urlCreateFirstInspectOrder, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlCreateFirstInspectOrder}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def completedProduction(self,ProductionDispatchCode):
        """
        完成生产
        """
        uploads = {
            "OneGoodQty": 7,
            "OpSign": 1,
            "ReportUserCode": "CQ",
            "ReportUserName": "CQ",
            "ProductionDispatchCode": ProductionDispatchCode,
            "EquipmentCode": EquipmentCode,
            "EquipmentName": EquipmentName,
            "WorkShopInfoName": OrganizationStructureCode,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlCompletedProduction = get_url() + apiCompletedProduction
        try:
            response = requests.post(url=urlCompletedProduction, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlCompletedProduction}，请求头: {self.headers}，请求体: {uploads}")
            raise e

if __name__ == '__main__':
    res = SingleUnitMaterial().createFirstInspectOrder("DL202505150875").json()
    print(res)