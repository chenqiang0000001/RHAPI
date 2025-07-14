import sys
import os
# 将项目根目录添加到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Business.mom_admin.production_modeling.factory_model import FactoryModel
from Business.mom_admin.factory_modeling.production_process import ProcessRelated
from Business.mom_admin.factory_modeling.product_materials import ProductMaterials
from Business.mom_admin.factory_modeling.product_materials import MaterialsBOM
from Business.mom_admin.equipment_management.equipment_ledger_management import EquipmentLedgerManagement
from Business.mom_admin.quality_control.QC_scheme import ProductInspectionPlan, InspectionSheet
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.log_module import Logger
from Business.mom_admin.production_management.production_plan import ProductionPlan, ProductionScheduling
from Business.mom_Ic.production_workbench import SingleUnitMaterial
from Business.mom_admin.ESOP.product_process_SOP import ProductProcessSOP
from Toolbox.random_container import random_characters
from Business.pda.label_operation import LabelOperation
from Public.variables.mom_admin import factory_modeling as fm


class DebugMainProcess:
    """
    DebugMainProcess 调试主流程类。
    用于端到端自动化调试生产主流程，包括基础数据、生产计划、派工、生产、SOP、检验、PDA等全流程。
    每个成员变量均有详细注释，便于理解和维护。
    """
    
    def __init__(self):
        """
        初始化调试主流程所需的所有业务对象和参数。
        各成员变量说明：
        self.logger: 日志记录器，用于记录调试日志。
        self.factory_model: 工厂模型业务对象，负责车间、产线等基础数据操作。
        self.process_related: 工艺相关业务对象，负责工序、工艺路线等操作。
        self.product_materials: 产品物料业务对象，负责物料相关操作。
        self.bom: BOM业务对象，负责物料BOM及明细操作。
        self.equipment_ledger: 设备台账业务对象，负责设备相关操作。
        self.production_plan: 生产计划业务对象，负责生产计划单相关操作。
        self.production_workbench: 生产作业业务对象，负责生产执行、派工等操作。
        self.sop: SOP文档业务对象，负责ESOP文件上传、审核、查询等。
        self.QC: 检验方案业务对象，负责产品检验方案相关操作。
        self.label_op: PDA标签操作业务对象，负责标签扫描、拆分等操作。
        self.PS: 派工业务对象，负责生产计划排产、派工等操作。
        self.material_id: 物料ID，自动获取用于后续依赖。
        self.material_bom_id: 物料BOM ID。
        self.process_id: 工序ID。
        self.process_route_id: 工艺路线ID。
        self.process_route_id2: 产品工艺路线ID。
        self.equipment_ledger_id: 设备台账ID。
        self.workshop_id: 车间ID。
        self.production_line_id: 产线ID。
        self.BOMVersion: BOM版本号。
        self.file_code_material: 物料ESOP文件FileCode。
        self.file_id_material: 物料ESOP文件Id。
        self.file_code_route: 工艺路线ESOP文件FileCode。
        self.file_id_route: 工艺路线ESOP文件Id。
        self.production_plan_code: 生产计划单号。
        self.production_plan_id: 生产计划单Id。
        self.dispatch_code: 派工单号。
        self.process_task_code: 工序任务号。
        self.label_sn: 标签SN，PDA用。
        self.label_split_sn: 拆分后标签SN。
        self.inspect_order_code: 检验单号。
        """
        self.logger = Logger(name="debug_mainprocess").get_logger()  # 日志记录器
        self.factory_model = FactoryModel()  # 工厂模型业务对象
        self.process_related = ProcessRelated()  # 工艺相关业务对象
        self.product_materials = ProductMaterials()  # 产品物料业务对象
        self.bom = MaterialsBOM()  # BOM业务对象
        self.equipment_ledger = EquipmentLedgerManagement()  # 设备台账业务对象
        self.production_plan = ProductionPlan()  # 生产计划业务对象
        self.production_workbench = SingleUnitMaterial()  # 生产作业业务对象
        self.sop = ProductProcessSOP()  # SOP文档业务对象
        self.QC = ProductInspectionPlan()  # 检验方案业务对象
        self.label_op = LabelOperation()  # PDA标签操作业务对象
        self.PS = ProductionScheduling()  # 派工业务对象
        self.material_id = None  # 物料ID
        self.material_bom_id = None  # 物料BOM ID
        self.process_id = None  # 工序ID
        self.process_route_id = None  # 工艺路线ID
        self.process_route_id2 = None  # 产品工艺路线ID
        self.equipment_ledger_id = None  # 设备台账ID
        self.workshop_id = None  # 车间ID
        self.production_line_id = None  # 产线ID
        self.BOMVersion = None  # BOM版本号
        self.file_code_material = None  # 物料ESOP文件FileCode
        self.file_id_material = None  # 物料ESOP文件Id
        self.file_code_route = None  # 工艺路线ESOP文件FileCode
        self.file_id_route = None  # 工艺路线ESOP文件Id
        self.production_plan_code = None  # 生产计划单号
        self.production_plan_id = None  # 生产计划单Id
        self.dispatch_code = None  # 派工单号
        self.process_task_code = None  # 工序任务号
        self.label_sn = "20250417TP2025/4/17 9:27:450013"  # 标签SN，PDA用
        self.label_split_sn = None  # 拆分后标签SN
        self.inspect_order_code = None  # 检验单号
        self.inspection_sheet_id = None  # 检验单ID

    def cleanup_basic_data(self):
        """
        清理主流程调试过程中创建的所有基础数据。
        按照依赖顺序逆序删除，确保环境干净，避免数据残留影响后续测试。
        通常在流程结束或异常时自动调用。
        """
        print("触发数据清理...")
        try:
            if self.BOMVersion and self.material_bom_id:
                try:
                    self.bom.removeManufactureBomData(self.BOMVersion, self.material_bom_id)
                    print("✓ 删除物料BOM")
                except Exception as e:
                    print("删除物料BOM异常：", e)
            if self.process_id:
                try:
                    self.process_related.removeProcessInfoData(self.process_id)
                    print("✓ 删除工序")
                except Exception as e:
                    print("删除工序异常：", e)
            if self.process_route_id:
                try:
                    self.process_related.removeProcessRoutingData(self.process_route_id)
                    print("✓ 删除工艺路线")
                except Exception as e:
                    print("删除工艺路线异常：", e)
            if self.process_route_id2:
                try:
                    self.process_related.RemoveBatchProductProcessRouteDatas(self.process_route_id2)
                    print("✓ 删除产品工艺路线")
                except Exception as e:
                    print("删除产品工艺路线异常：", e)
            if self.material_id:
                try:
                    self.product_materials.removeMaterialInfoData(self.material_id)
                    print("✓ 删除物料")
                except Exception as e:
                    print("删除物料异常：", e)
            if self.equipment_ledger_id:
                try:
                    self.equipment_ledger.removeBatchEquipmentLedger(self.equipment_ledger_id)
                    print("✓ 删除设备台账")
                except Exception as e:
                    print("删除设备台账异常：", e)
            if self.production_line_id:
                try:
                    self.factory_model.removeOrganizationStructureData_productionline(self.production_line_id)
                    print("✓ 删除产线")
                except Exception as e:
                    print("删除产线异常：", e)
            if self.workshop_id:
                try:
                    self.factory_model.removeOrganizationStructureData(self.workshop_id)
                    print("✓ 删除车间")
                except Exception as e:
                    print("删除车间异常：", e)
            print("数据清理完成。")
        except Exception as e:
            print("数据清理时发生异常：", e)

    def run(self):
        """
        主流程调试入口函数。
        严格按照mainprocess_tests.py的业务顺序，依次自动化执行基础数据创建、生产计划、派工、生产、SOP、首检、检验、PDA等全流程。
        每一步均有详细日志和异常处理，便于定位问题。
        """
        print("="*60)
        print("开始执行调试脚本 - 严格按照主流程测试文件逻辑")
        print("="*60)
        
        try:
            # ========== 第一阶段：基础数据创建 ==========
            print("\n第一阶段：基础数据创建")
            
            # test_01: 新增物料
            print("test_01: 新增物料")
            response = self.product_materials.storeMaterialInfoData()
            if response and response.json().get('Success') == True:
                print("✓ 新增物料成功")
            else:
                print("✗ 新增物料失败")
            
            # test_02: 查询物料
            print("test_02: 查询物料")
            response = self.product_materials.getMaterialInfoAutoQueryDatas()
            if response and response.json().get('Success') == True:
                result = response.json()
                if result.get('Attach') and len(result['Attach']) > 0:
                    self.material_id = result['Attach'][0]['Id']
                    print(f"✓ 获取到物料ID: {self.material_id}")
                else:
                    print("✗ 未获取到物料ID")
            else:
                print("✗ 查询物料失败")
            
            # test_03: 新增物料BOM
            print("test_03: 新增物料BOM")
            self.BOMVersion = random_characters()
            response = self.bom.storeManufactureBomData(self.BOMVersion)
            if response and response.json().get('Success') == True:
                print(f"✓ 新增物料BOM成功，版本号: {self.BOMVersion}")
            else:
                print("✗ 新增物料BOM失败")
            
            # test_04: 新增物料BOM明细
            print("test_04: 新增物料BOM明细")
            response = self.bom.storeBatchManufactureBomDetailDatas(self.BOMVersion)
            if response and response.json().get('Success') == True:
                print("✓ 新增物料BOM明细成功")
            else:
                print("✗ 新增物料BOM明细失败")
            
            # test_05: 查询物料BOM
            print("test_05: 查询物料BOM")
            response = self.bom.getGetBomMasterViewAutoQueryDatas()
            if response and response.json().get('Success') == True:
                result = response.json()
                if result.get('Attach') and len(result['Attach']) > 0:
                    self.material_bom_id = result['Attach'][0]['Id']
                    print(f"✓ 获取到物料BOM ID: {self.material_bom_id}")
                else:
                    print("✗ 未获取到物料BOM ID")
            else:
                print("✗ 查询物料BOM失败")
            
            # test_06: 新增工序
            print("test_06: 新增工序")
            response = self.process_related.storeProcessInfoData()
            if response and response.json().get('Success') == True:
                print("✓ 新增工序成功")
            else:
                print("✗ 新增工序失败")
            
            # test_07: 查询工序
            print("test_07: 查询工序")
            response = self.process_related.GetProcessInfoAutoQueryDatas()
            if response and response.json().get('Success') == True:
                result = response.json()
                IsFirstInspect= result.get('Attach') and len(result['Attach']) > 0 and result['Attach'][0].get('IsFirstInspect')
                print(f"当前工序是否首检: {IsFirstInspect}")
                if result.get('Attach') and len(result['Attach']) > 0:
                    self.process_id = result['Attach'][0]['Id']
                    print(f"✓ 获取到工序ID: {self.process_id}")
                else:
                    print("✗ 未获取到工序ID")
            else:
                print("✗ 查询工序失败")
            
            # test_08: 新增工艺路线
            print("test_08: 新增工艺路线")
            response = self.process_related.storeProcessRoutingData()
            if response and response.json().get('Success') == True:
                print("✓ 新增工艺路线成功")
            else:
                print("✗ 新增工艺路线失败")
            
            # test_09: 查询工艺路线
            print("test_09: 查询工艺路线")
            response = self.process_related.getProcessRoutingAutoQueryDatas()
            if response and response.json().get('Success') == True:
                result = response.json()
                if result.get('Attach') and len(result['Attach']) > 0:
                    self.process_route_id = result['Attach'][0]['Id']
                    print(f"✓ 获取到工艺路线ID: {self.process_route_id}")
                else:
                    print("✗ 未获取到工艺路线ID")
            else:
                print("✗ 查询工艺路线失败")
            
            # test_10: 工艺路线绑定工序
            print("test_10: 工艺路线绑定工序")
            response = self.process_related.adjustProcessRoutingEntry()
            if response and response.json().get('Success') == True:
                print("✓ 工艺路线绑定工序成功")
            else:
                print("✗ 工艺路线绑定工序失败")
            
            # test_11: 产品绑定工艺路线
            print("test_11: 产品绑定工艺路线")
            response = self.process_related.StoreProductProcessRouteData()
            if response and response.json().get('Success') == True:
                print("✓ 产品绑定工艺路线成功")
            else:
                print("✗ 产品绑定工艺路线失败")
            
            # test_12: 工艺路线绑定产品
            print("test_12: 工艺路线绑定产品")
            response = self.process_related.StoreBatchProductProcessRouteDatas()
            if response and response.json().get('Success') == True:
                print("✓ 工艺路线绑定产品成功")
            else:
                print("✗ 工艺路线绑定产品失败")
            
            # test_13: 查询产品工艺路线
            print("test_13: 查询产品工艺路线")
            response = self.process_related.GetProductProcessRouteAutoQueryDatas()
            if response and response.json().get('Success') == True:
                result = response.json()
                if result.get('Attach') and len(result['Attach']) > 0:
                    self.process_route_id2 = result['Attach'][0]['Id']
                    print(f"✓ 获取到产品工艺路线ID: {self.process_route_id2}")
                else:
                    print("✗ 未获取到产品工艺路线ID")
            else:
                print("✗ 查询产品工艺路线失败")
            
            # test_14: 产品工序BOM绑定
            print("test_14: 产品工序BOM绑定")
            response = self.process_related.SelectManufactureBom(self.BOMVersion)
            if response and response.json().get('Success') == True:
                print("✓ 产品工序BOM绑定成功")
            else:
                print("✗ 产品工序BOM绑定失败")
            
            # test_15: 新增设备台账
            print("test_15: 新增设备台账")
            response = self.equipment_ledger.storeEquipmentLedgerData()
            if response and response.json().get('Success') == True:
                print("✓ 新增设备台账成功")
            else:
                print("✗ 新增设备台账失败")
            
            # test_16: 查询设备台账
            print("test_16: 查询设备台账")
            response = self.equipment_ledger.getEquipmentLedgerAutoQueryDatas()
            if response and response.json().get('Success') == True:
                result = response.json()
                if result.get('Attach') and len(result['Attach']) > 0:
                    self.equipment_ledger_id = result['Attach'][0]['Id']
                    print(f"✓ 获取到设备台账ID: {self.equipment_ledger_id}")
                else:
                    print("✗ 未获取到设备台账ID")
            else:
                print("✗ 查询设备台账失败")
            
            # ========== 第二阶段：ESOP文件处理 ==========
            print("\n第二阶段：ESOP文件处理")
            
            # test_17: 新增ESOP文件
            print("test_17: 新增ESOP文件")
            response = self.sop.uploadProductProcessDocumentation(
                file_path=r"D:\apiAutomationRH\test.pdf"
            )
            if response and response.json().get('Success') == True:
                print("✓ 新增ESOP文件成功")
            else:
                print("✗ 新增ESOP文件失败")
            
            # test_18: 审核ESOP文件
            print("test_18: 审核ESOP文件")
            query_resp = self.sop.getESopMaterialAutoQueryDatas(
                material_code=MaterialCode,
                material_category_code="DQJ"
            )
            if query_resp and query_resp.json().get('Success') == True:
                query_data = query_resp.json()
                attach = query_data.get('Attach')
                if attach and isinstance(attach, list) and len(attach) > 0:
                    file_id_material = attach[0].get('Id')
                    audit_resp = self.sop.AuditESopMaterialDatas(
                        Material_documentation_id=file_id_material,
                        MaterialCode=MaterialCode,
                        MaterialName="测试物料"
                    )
                    if audit_resp and audit_resp.json().get('Success') == True:
                        print("✓ 审核ESOP文件成功")
                    else:
                        print("✗ 审核ESOP文件失败")
                else:
                    print("✗ 未获取到ESOP文件ID")
            else:
                print("✗ 查询ESOP文件失败")
            
            # test_19: 新增工艺路线ESOP文件
            print("test_19: 新增工艺路线ESOP文件")
            response = self.sop.uploadProductProcessDocumentation(
                file_path=r"D:\apiAutomationRH\test.pdf",
                material_code=MaterialCode,
                process_routing_code=ProcessRoutingCode,
                process_code=ProcessCode,
                process_name=ProcessName
            )
            if response and response.json().get('Success') == True:
                print("✓ 新增工艺路线ESOP文件成功")
            else:
                print("✗ 新增工艺路线ESOP文件失败")
            
            # test_20: 审核工艺路线ESOP文件
            print("test_20: 审核工艺路线ESOP文件")
            esop_query_resp = self.production_workbench.getESopMaterialProcessRoutingAutoQueryDatas()
            if esop_query_resp and esop_query_resp.json().get('Success') == True:
                esop_data = esop_query_resp.json()
                if esop_data.get('Attach') and len(esop_data['Attach']) > 0:
                    file_id_route = esop_data['Attach'][0].get('Id')
                    audit_data = [{
                        "MaterialCode": MaterialCode,
                        "MaterialName": "测试物料",
                        "ProcessRoutingCode": ProcessRoutingCode,
                        "ProcessRoutingName": ProcessRoutingName,
                        "FileCode": esop_data['Attach'][0].get('FileCode') or "",
                        "FileName": "1111.pdf",
                        "VersionCode": "V0.0.1",
                        "IsEnable": True,
                        "SopType": "-1:ProductProcessFile:SopData",
                        "SopStatus": "Pass",
                        "AuditorCode": 10402,
                        "AuditorName": "陈强",
                        "AuditMind": "",
                        "AuditTime": None,
                        "CreatorUserId": 10402,
                        "CreatorUserName": "CQ",
                        "CreatorUserRealName": "陈强",
                        "CreationTime": "2025-06-27T16:31:28.71+08:00",
                        "LastModifierUserId": None,
                        "LastModifierUserName": None,
                        "LastModifierUserRealName": "",
                        "LastModificationTime": None,
                        "CompanyCode": CompanyCode,
                        "FactoryCode": "00000.00001",
                        "NeedUpdateFields": {},
                        "Id": file_id_route or 0,
                        "Remark": "",
                        "expand": False,
                        "index": 1,
                        "select": True,
                        "__delete": False,
                        "__preview": True,
                        "__preview_disable": False,
                        "__log": True,
                        "__log_disable": False,
                        "__replace": True,
                        "__replace_disable": False,
                        "__download": True,
                        "__download_disable": False,
                        "__processFile": True,
                        "__processFile_disable": False,
                        "isEdit": True
                    }]
                    audit_resp = self.sop.AuditESopMaterialProcessRoutingDatas(audit_data)
                    if audit_resp and audit_resp.json().get('Success') == True:
                        print("✓ 审核工艺路线ESOP文件成功")
                    else:
                        print("✗ 审核工艺路线ESOP文件失败")
                else:
                    print("✗ 未获取到工艺路线ESOP文件ID")
            else:
                print("✗ 查询工艺路线ESOP文件失败")
            
            # ========== 第三阶段：工厂基础数据 ==========
            print("\n第三阶段：工厂基础数据")
            
            # test_21: 新增车间
            print("test_21: 新增车间")
            response = self.factory_model.storeOrganizationStructureData()
            if response and response.json().get('Success') == True:
                print("✓ 新增车间成功")
            else:
                print("✗ 新增车间失败")
            
            # test_23: 查询车间
            print("test_23: 查询车间")
            response = self.factory_model.GetWorkshopAutoQueryDatas()
            if response and response.json().get('Success') == True:
                result = response.json()
                if result.get('Attach') and len(result['Attach']) > 0:
                    self.workshop_id = result['Attach'][0]['Id']
                    print(f"✓ 获取到车间ID: {self.workshop_id}")
                else:
                    print("✗ 未获取到车间ID")
            else:
                print("✗ 查询车间失败")
            
            # test_24: 新增产线
            print("test_24: 新增产线")
            response = self.factory_model.storeOrganizationStructureData_productionline()
            if response and response.json().get('Success') == True:
                print("✓ 新增产线成功")
            else:
                print("✗ 新增产线失败")
            
            # test_25: 查询产线
            print("test_25: 查询产线")
            response = self.factory_model.GetProductionLineAutoQueryDatas()
            if response and response.json().get('Success') == True:
                result = response.json()
                if result.get('Attach') and len(result['Attach']) > 0:
                    self.production_line_id = result['Attach'][0]['Id']
                    print(f"✓ 获取到产线ID: {self.production_line_id}")
                else:
                    print("✗ 未获取到产线ID")
            else:
                print("✗ 查询产线失败")
            
            # test_26: 创建检验方案
            print("test_26: 创建检验方案")
            response = self.QC.createProductInspectSchemaData()
            if response and response.json().get('Success') == True:
                print("✓ 创建检验方案成功")
            else:
                print("✗ 创建检验方案失败")
            
            # ========== 第四阶段：生产计划管理 ==========
            print("\n第四阶段：生产计划管理")
            
            # test_27: 创建生产计划
            print("test_27: 创建生产计划")
            response = self.production_plan.storeProductionPlanOrderData()
            if response and response.json().get('Success') == True:
                result = response.json()
                attach = result.get('Attach')
                if attach:
                    self.production_plan_code = attach.get('ProductionPlanCode')
                    self.production_plan_id = attach.get('Id')
                    print(f"✓ 创建生产计划成功，计划号: {self.production_plan_code}")
                else:
                    print("✗ 未获取到生产计划信息")
            else:
                print("✗ 创建生产计划失败")
            
            # test_28: 确认生产计划
            print("test_28: 确认生产计划")
            if self.production_plan_code and self.production_plan_id:
                confirm_body = {
                    "ProductionPlanCode": self.production_plan_code,
                    "Id": self.production_plan_id,
                    "expand": False,
                    "index": 1,
                    "select": True,
                    "ProcessRoutingCode": ProcessRoutingCode2,
                    "__edit": True,
                    "__edit_disable": False,
                    "__delete": True,
                    "__delete_disable": False,
                    "isEdit": True,
                    "LastModifierUserName":"zdh01",
                    "LastModifierUserRealName":"zdh01",
                    "ProductCode": MaterialCode,
                    "ProductName": MaterialName
                }
                response = self.production_plan.confirmBatchProductionPlanOrderDatas([confirm_body])
                if response and response.json().get('Success') == True:
                    print("✓ 确认生产计划成功")
                else:
                    print("✗ 确认生产计划失败")
            else:
                print("✗ 无法确认生产计划，缺少必要参数")
            
            # test_29: 下达生产计划
            print("test_29: 下达生产计划")
            if self.production_plan_code and self.production_plan_id:
                BOMBasicCode = BOMCode + '_' + self.BOMVersion
                issued_body = {
                    "ProductionPlanCode": self.production_plan_code,
                    "MasterProductionPlanCode": None,
                    "ErpProductionPlanCode": None,
                    "ErpProductionPlanRowNo": None,
                    "ErpProductionPlanRowNoId": 0,
                    "SaleOrderCode": None,
                    "SaleOrderRowNo": None,
                    "RelationProductionCode": None,
                    "RelationProductionRowNo": None,
                    "CustomerCode": None,
                    "CustomerName": None,
                    "ProductionType": "Normal",
                    "PlanCategory": None,
                    "PlanScheduler": None,
                    "ProcessRoutingCode": ProcessRoutingCode2,
                    "ProcessRoutingName": None,
                    "ProductCode": MaterialCode,
                    "ProductName": MaterialName,
                    "ProductSpecification": None,
                    "BOMCode": BOMCode,
                    "BOMBasicCode": BOMBasicCode,
                    "ProductionPlanSource": None,
                    "PlanStartDate": "2025-06-24T00:00:00+08:00",
                    "PlanStartTime": None,
                    "PlanEndDate": "2025-08-31T00:00:00+08:00",
                    "PlanEndTime": None,
                    "ActualStartDate": None,
                    "ActualStartTime": None,
                    "ActualEndDate": None,
                    "ActualEndTime": None,
                    "PlanIssuedDate": None,
                    "PlanIssuedTime": None,
                    "PlanClosedDate": None,
                    "PlanClosedTime": None,
                    "PlanQty": 100,
                    "CompeletedQty": 0,
                    "UnCompeletedQty": 100,
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
                    "OrderStatus": "WaitIssued",
                    "ControlStatus": "Enable",
                    "ControlReason": None,
                    "OrganizationStructureCode": OrganizationStructureCode,
                    "OrganizationStructureName": OrganizationStructureName,
                    "OrganizationStructureDisplayName": None,
                    "OrganizationStructureExternalCode": None,
                    "WorkShopInfoCode": None,
                    "WorkShopInfoName": None,
                    "ProductionLineCode": None,
                    "ProductionLineName": None,
                    "EquipmentCode": None,
                    "EquipmentName": None,
                    "EmergencySort": 0,
                    "MouldCode": None,
                    "MouldName": None,
                    "MouldSpecification": None,
                    "CreatorUserId": 150,
                    "CreatorUserName": "DemoAdmin",
                    "CreatorUserRealName": "DemoAdmin",
                    "CreationTime": "2025-06-28T09:58:59.143+08:00",
                    "LastModifierUserId": 150,
                    "LastModifierUserName": "DemoAdmin",
                    "LastModifierUserRealName": "DemoAdmin",
                    "LastModificationTime": "2025-06-28T09:58:59.187+08:00",
                    "CompanyCode": "00000",
                    "FactoryCode": "00000.00001",
                    "NeedUpdateFields": {},
                    "Id": self.production_plan_id,
                    "Remark": "",
                    "expand": False,
                    "index": 1,
                    "select": True,
                    "__edit": True,
                    "__edit_disable": False,
                    "__flushAnalysis": False,
                    "isEdit": True
                }
                response = self.production_plan.issuedBatchProductionPlanOrderDatas([issued_body])
                print(issued_body)
                print(f"下达生产计划响应: {response.json()}")
                if response and response.json().get('Success') == True:
                    print("✓ 下达生产计划成功")
                else:
                    print("✗ 下达生产计划失败")
            else:
                print("✗ 无法下达生产计划，缺少必要参数")
            
            # ========== 第五阶段：生产执行 ==========
            print("\n第五阶段：生产执行")
            
            # test_30: 创建派工单
            print("test_30: 创建派工单")
            if self.production_plan_code:
                # 先查询工序任务单详情，获取工艺路线分录号
                print("[前置] 查询工序任务单（派工用）")
                task_query_body = {
                    "ProductionPlanCode": self.production_plan_code,
                    "ProcessTaskCode": "",
                    "ProductCode": None,
                    "ProductName": "",
                    "ProcessRoutingCode": None,
                    "ProcessCode": None,
                    "ProcessName": "",
                    "IsPaged": True,
                    "PageSize": 10,
                    "PageIndex": 1,
                    "CompanyCode": fm.CompanyCode,
                    "FactoryCode": "00000.00001"
                }
                print(f"查询工序任务单请求体为：{task_query_body}")
                task_query_resp = self.PS.getCanDispatchProcessTaskOrderDatas(task_query_body)
                if task_query_resp and task_query_resp.json().get('Success'):
                    task_data = task_query_resp.json()
                    task_attach = task_data.get('Attach')
                    if task_attach and isinstance(task_attach, list) and len(task_attach) > 0:
                        task_info = task_attach[0]
                        self.process_task_code = task_info.get('ProcessTaskCode')
                        process_routing_entry_code = task_info.get('ProcessRoutingEntryCode')
                        print(f"获取到工序任务单号: {self.process_task_code}, 工艺路线分录号: {process_routing_entry_code}")
                        
                        # 创建派工单
                        dispatch_data = [{
                            "ProductionPlanCode": self.production_plan_code,
                            "ProcessRoutingCode": fm.ProcessRoutingCode,  # 使用变量
                            "ProcessCode": fm.ProcessCode,  # 使用变量
                            "ProcessName": fm.ProcessName,  # 使用变量
                            "WorkshopCode": fm.OrganizationStructureCode,  # 使用变量
                            "WorkshopName": fm.OrganizationStructureName,  # 使用变量
                            "ProductionLineCode": self.production_line_id,  # 使用产线ID
                            "ProductionLineName": "自动化产线2",  # 使用产线名称
                            "EquipmentCode": fm.EquipmentCode,  # 使用变量
                            "EquipmentName": fm.EquipmentName,  # 使用变量
                            "PlanQty": fm.PlanQty,  # 使用变量
                            "CompanyCode": fm.CompanyCode,
                            "FactoryCode": "00000.00001",
                            "DispatchQty": fm.PlanQty,  # 使用变量
                            "ProcessTaskCode": self.process_task_code,
                            "ProcessRoutingEntryCode": process_routing_entry_code
                        }]
                        
                        print(f"ProcessRoutingCode3: {fm.ProcessRoutingCode}")
                        print(f"ProcessCode: {fm.ProcessCode}")
                        print(f"ProcessName: {fm.ProcessName}")
                        print(f"EquipmentCode: {fm.EquipmentCode}")
                        print(f"EquipmentName: {fm.EquipmentName}")
                        print(f"OrganizationStructureCode: {fm.OrganizationStructureCode}")
                        print(f"OrganizationStructureName: {fm.OrganizationStructureName}")
                        print(f"OrganizationStructureCode2: {fm.OrganizationStructureCode2}")
                        print(f"OrganizationStructureName2: {fm.OrganizationStructureName2}")
                        print(f"PlanQty: {fm.PlanQty}")
                        print(f"CompanyCode: {fm.CompanyCode}")
                        
                        response = self.PS.createBatchProductionDispatchOrder(dispatch_data)
                        if response and response.json().get('Success'):
                            print("✓ 创建派工单成功")
                        else:
                            print("✗ 创建派工单失败")
                            print(f"派工单接口返回状态码: {response.status_code}")
                            print(f"派工单接口返回内容: {response.text}")
                            print(f"派工单接口返回JSON: {response.json()}")
                    else:
                        print("✗ 未获取到工序任务单详情")
                else:
                    print("✗ 查询工序任务单失败")
            else:
                print("✗ 无法创建派工单，缺少生产计划单号")
            
            # test_31: 查询派工单（新接口）
            print("test_31: 查询派工单（新接口）")
            if self.production_plan_code:
                dispatch_query_body = {
                    "ProductionDispatchCode": "",
                    "BindProductionDispatchCode": "",
                    "ProcessTaskCode": "",
                    "ProductionPlanCode": self.production_plan_code,
                    "ProcessCode": None,
                    "ProcessName": "",
                    "EquipmentCode": None,
                    "EquipmentName": "",
                    "MouldCode": None,
                    "MouldName": "",
                    "ProductCode": None,
                    "ProductName": "",
                    "IsPaged": True,
                    "PageSize": 10,
                    "PageIndex": 1,
                    "CompanyCode": fm.CompanyCode,
                    "FactoryCode": "00000.00001"
                }
                dispatch_query_resp = self.PS.getProductionDispatchOrderAutoQueryDatas(dispatch_query_body)
                if dispatch_query_resp and dispatch_query_resp.json().get('Success'):
                    data = dispatch_query_resp.json()
                    attach = data.get('Attach')
                    if attach and isinstance(attach, list) and len(attach) > 0:
                        d = attach[0]
                        self.dispatch_code = d.get('ProductionDispatchCode')
                        self.process_task_code = d.get('ProcessTaskCode')
                        print(f"✓ 查询到派工单号: {self.dispatch_code}, 工序任务号: {self.process_task_code}")
                    else:
                        print("✗ 未查询到派工单")
                else:
                    print("✗ 查询派工单失败")
            else:
                print("✗ 无法查询派工单，缺少生产计划单号")
            
            # test_31.5: 派工单下达
            print("test_31.5: 派工单下达")
            if self.dispatch_code:
                # 先查询派工单详情用于下达
                dispatch_detail_body = {
                    "ProductionDispatchCode": self.dispatch_code,
                    "BindProductionDispatchCode": "",
                    "ProcessTaskCode": self.process_task_code,
                    "ProductionPlanCode": self.production_plan_code,
                    "ProcessCode": None,
                    "ProcessName": "",
                    "EquipmentCode": None,
                    "EquipmentName": "",
                    "MouldCode": None,
                    "MouldName": "",
                    "ProductCode": None,
                    "ProductName": "",
                    "IsPaged": True,
                    "PageSize": 10,
                    "PageIndex": 1,
                    "CompanyCode": fm.CompanyCode,
                    "FactoryCode": "00000.00001"
                }
                dispatch_detail_resp = self.PS.getProductionDispatchOrderAutoQueryDatas(dispatch_detail_body)
                if dispatch_detail_resp and dispatch_detail_resp.json().get('Success'):
                    detail_data = dispatch_detail_resp.json()
                    detail_attach = detail_data.get('Attach')
                    if detail_attach and isinstance(detail_attach, list) and len(detail_attach) > 0:
                        dispatch_detail = detail_attach[0]
                        # 下达派工单
                        issue_data = [dispatch_detail]
                        response = self.PS.IssuedBatchProductionDispatchOrderDatas(issue_data)
                        if response and response.json().get('Success'):
                            print("✓ 下达派工单成功")
                        else:
                            print("✗ 下达派工单失败")
                    else:
                        print("✗ 未获取到派工单详情")
                else:
                    print("✗ 查询派工单详情失败")
            else:
                print("✗ 无法下达派工单，缺少派工单号")
            
            # test_32: 查询选择派工单
            print("test_32: 查询选择派工单")
            if self.dispatch_code:
                dispatch_query_body = {
                    "ProductionDispatchCode": self.dispatch_code,
                    "BindProductionDispatchCode": "",
                    "ProcessTaskCode": self.process_task_code,
                    "ProductionPlanCode": self.production_plan_code,
                    "ProcessCode": None,
                    "ProcessName": "",
                    "EquipmentCode": None,
                    "EquipmentName": "",
                    "MouldCode": None,
                    "MouldName": "",
                    "ProductCode": None,
                    "ProductName": "",
                    "IsPaged": True,
                    "PageSize": 10,
                    "PageIndex": 1,
                    "CompanyCode": fm.CompanyCode,
                    "FactoryCode": "00000.00001"
                }
                dispatch_query_resp = self.PS.getProductionDispatchOrderAutoQueryDatas(dispatch_query_body)
                if dispatch_query_resp and dispatch_query_resp.json().get('Success'):
                    print("✓ 查询派工单成功")
                else:
                    print("✗ 查询派工单失败")
            else:
                print("✗ 无法查询派工单，缺少派工单号")
            
            # test_33: 开始生产
            print("test_33: 开始生产")
            if self.dispatch_code and self.production_plan_code and self.process_task_code:
                # 先查询派工单详情，确保状态正确
                dispatch_query_body = {
                    "ProductionDispatchCode": self.dispatch_code,
                    "BindProductionDispatchCode": "",
                    "ProcessTaskCode": self.process_task_code,
                    "ProductionPlanCode": self.production_plan_code,
                    "ProcessCode": None,
                    "ProcessName": "",
                    "EquipmentCode": None,
                    "EquipmentName": "",
                    "MouldCode": None,
                    "MouldName": "",
                    "ProductCode": None,
                    "ProductName": "",
                    "IsPaged": True,
                    "PageSize": 10,
                    "PageIndex": 1,
                    "CompanyCode": fm.CompanyCode,
                    "FactoryCode": "00000.00001"
                }
                dispatch_query_resp = self.PS.getProductionDispatchOrderAutoQueryDatas(dispatch_query_body)
                if dispatch_query_resp and dispatch_query_resp.json().get('Success'):
                    data = dispatch_query_resp.json()
                    attach = data.get('Attach')
                    if attach and isinstance(attach, list) and len(attach) > 0:
                        d = attach[0]
                        print(f"派工单状态: {d.get('OrderStatus')}")
                        print(f"派工单控制状态: {d.get('ControlStatus')}")
                        print(f"工序编码: {d.get('ProcessCode')}")
                        print(f"设备编码: {d.get('EquipmentCode')}")
                        print(f"车间编码: {d.get('WorkShopInfoCode')}")
                        print(f"产线编码: {d.get('ProductionLineCode')}")
                        
                        # 确保所有必要参数都有值，全部从派工单详情获取
                        # 获取派工单详情字段并进行空值检查
                        process_code = d.get('ProcessCode')
                        process_name = d.get('ProcessName')
                        process_seq = d.get('ProcessSeq')
                        workshop_code = d.get('WorkShopInfoCode')
                        workshop_name = d.get('WorkShopInfoName')
                        # 使用类属性中的生产线ID作为备选
                        production_line_code = d.get('ProductionLineCode') or self.production_line_id
                        production_line_name = d.get('ProductionLineName')
                        equipment_code = d.get('EquipmentCode')
                        equipment_name = d.get('EquipmentName')
                        organization_structure_code = d.get('OrganizationStructureCode')
                        organization_structure_name = d.get('OrganizationStructureName')
                        
                        # 检查关键参数是否存在
                        required_fields = {
                            'process_code': process_code,
                            'process_name': process_name,
                            'process_seq': process_seq,
                            'workshop_code': workshop_code,
                            'equipment_code': equipment_code
                        }
                        missing_fields = [k for k, v in required_fields.items() if not v]
                        if missing_fields:
                            print(f"✗ 派工单详情缺少必要字段: {', '.join(missing_fields)}")
                            return
                        
                        # 从派工单详情中提取assign_work_id
                        assign_work_id = d.get('Id')
                        if not assign_work_id:
                            print("✗ 未获取到派工单ID")
                            return
                        
                        print(f"开始生产参数:")
                        print(f"  dispatch_code: {self.dispatch_code}")
                        print(f"  plan_code: {self.production_plan_code}")
                        print(f"  process_task_code: {self.process_task_code}")
                        print(f"  process_code: {process_code}")
                        print(f"  process_name: {process_name}")
                        print(f"  process_seq: {process_seq}")
                        print(f"  workshop_code: {workshop_code}")
                        print(f"  workshop_name: {workshop_name}")
                        print(f"  production_line_code: {production_line_code}")
                        print(f"  production_line_name: {production_line_name}")
                        print(f"  equipment_code: {equipment_code}")
                        print(f"  equipment_name: {equipment_name}")
                        print(f"  organization_structure_code: {organization_structure_code}")
                        print(f"  organization_structure_name: {organization_structure_name}")
                        print(f"  assign_work_id: {assign_work_id}")
                        
                        response = self.production_workbench.startProduction(
                            dispatch_code=self.dispatch_code,
                            plan_code=self.production_plan_code,
                            process_task_code=self.process_task_code,
                            process_code=process_code,
                            process_name=process_name,
                            process_seq=process_seq,
                            workshop_code=workshop_code,
                            workshop_name=workshop_name,
                            production_line_code=production_line_code,
                            production_line_name=production_line_name,
                            equipment_code=equipment_code,
                            equipment_name=equipment_name,
                            organization_structure_code=organization_structure_code,
                            organization_structure_name=organization_structure_name,
                            assign_work_id=assign_work_id
                        )
                        print(f"开始生产响应: {response.json()}")
                        if response and response.json().get('Success'):
                            print("✓ 开始生产成功")
                        else:
                            print("✗ 开始生产失败")
                            print(f"失败原因: {response.json().get('Message', '未知错误')}")
                    else:
                        print("✗ 未获取到派工单详情，无法开始生产")
                else:
                    print("✗ 查询派工单详情失败，无法开始生产")
            else:
                print("✗ 无法开始生产，缺少派工单号/计划单号/工序任务单号")
            
            # test_34: 查看SOP
            print("test_34: 查看SOP")
            if self.dispatch_code:
                response = self.production_workbench.getESopMaterialProcessRoutingAutoQueryDatas()
                if response and response.json().get('Success') == True:
                    print("✓ 查看SOP成功")
                else:
                    print("✗ 查看SOP失败")
            else:
                print("✗ 无法查看SOP，缺少派工单号")
            
            # ========== 第六阶段：质量检验 ==========
            print("\n第六阶段：质量检验")
            
            # test_35: 创建首检单
            print("test_35: 创建首检单")
            if self.dispatch_code:
                response = self.production_workbench.createFirstInspectOrder(self.dispatch_code)
                print(f"创建首检单响应: {response.json()}")
                if response and response.json().get('Success') == True:
                    print("✓ 创建首检单成功")
                else:
                    print("✗ 创建首检单失败")
            else:
                print("✗ 无法创建首检单，缺少派工单号")
            
            # test_36: 查询检验单
            print("test_36: 查询检验单")
            sheet = InspectionSheet()
            if self.production_plan_code:
                response = sheet.getIpqcProductInspectOrderDatas(self.production_plan_code)
                if response and response.json().get('Success') == True:
                    result = response.json()
                    attach = result.get('Attach')
                    if attach and isinstance(attach, list) and len(attach) > 0:
                        self.inspect_order_code = attach[0].get('InspectOrderCode')
                        self.inspection_sheet_id = attach[0].get('Id')
                        print(f"✓ 获取到检验单号: {self.inspect_order_code}")
                    else:
                        print("✗ 未获取到检验单号")
                else:
                    print("✗ 查询检验单失败")
            else:
                print("✗ 无法查询检验单，缺少生产计划单号")
            
            # test_37: 开始检验
            print("test_37: 开始检验")
            if self.inspect_order_code:
                response = sheet.startInspectProcessInspectOrder(self.inspect_order_code,self.inspection_sheet_id)
                print(f"开始检验响应: {response.json()}")
                if response and response.json().get('Success') == True:
                    print("✓ 开始检验成功")
                else:
                    print("✗ 开始检验失败")
            else:
                print("✗ 无法开始检验，缺少检验单号")
            
            # test_38: 提交检验结果
            print("test_38: 提交检验结果")
            if self.inspect_order_code:
                response = sheet.submitProcessInspectOrderData(self.inspect_order_code, self.dispatch_code, self.production_plan_code,self.inspection_sheet_id)
                if response and response.json().get('Success') == True:
                    print("✓ 提交检验结果成功")
                else:
                    print("✗ 提交检验结果失败")
            else:
                print("✗ 无法提交检验结果，缺少检验单号")
            
            # ========== 第七阶段：PDA操作 ==========
            print("\n第七阶段：PDA操作")
            
            # test_39: 扫描标签
            print("test_39: 扫描标签")
            response = self.label_op.scan_label(self.label_sn)
            if response and response.json().get('Success') == True:
                print("✓ 扫描标签成功")
            else:
                print("✗ 扫描标签失败")
            
            # test_40: 标签拆分
            print("test_40: 标签拆分")
            scan_resp = self.label_op.scan_label(self.label_sn)
            if scan_resp and scan_resp.json().get('Success') == True:
                scan_data = scan_resp.json()
                attach = scan_data.get('Attach')
                if attach and isinstance(attach, list) and len(attach) > 0:
                    split_body = attach[0].copy()
                    split_body['TransactQty'] = 1
                    split_body['Qty'] = 1
                    split_body['OrderCreatorName'] = "陈强"
                    split_body['OrderCreatorCode'] = "CQ"
                    
                    split_resp = self.label_op.label_split(split_body)
                    if split_resp and split_resp.json().get('Success') == True:
                        split_result = split_resp.json()
                        split_attach = split_result.get('Attach')
                        if split_attach and isinstance(split_attach, list):
                            for item in split_attach:
                                if item.get('LabelQty') == 1.0:
                                    self.label_split_sn = item.get('SN')
                                    print(f"✓ 标签拆分成功，拆分后SN: {self.label_split_sn}")
                                    break
                    else:
                        print("✗ 标签拆分失败")
                else:
                    print("✗ 未获取到标签数据")
            else:
                print("✗ 扫描标签失败")
            
            # test_41: 上料扫描SN
            print("test_41: 上料扫描SN")
            if self.label_split_sn:
                response = self.production_workbench.scanFeedingMaterialLabelData(self.label_split_sn)
                if response and response.json().get('Success') == True:
                    print("✓ 上料扫描SN成功")
                else:
                    print("✗ 上料扫描SN失败")
            else:
                print("✗ 无法上料扫描SN，缺少拆分后SN")
            
            # test_42: 确认上料
            print("test_42: 确认上料")
            if self.dispatch_code and self.label_split_sn:
                response = self.production_workbench.storeFeedingMaterialLabelDatas(self.dispatch_code, self.label_split_sn)
                if response and response.json().get('Success') == True:
                    print("✓ 确认上料成功")
                else:
                    print("✗ 确认上料失败")
            else:
                print("✗ 无法确认上料，缺少必要参数")
            
            # test_43: 生产报工
            print("test_43: 生产报工")
            if self.dispatch_code:
                response = self.production_workbench.productionReport(self.dispatch_code)
                if response and response.json().get('Success') == True:
                    print("✓ 生产报工成功")
                else:
                    print("✗ 生产报工失败")
            else:
                print("✗ 无法生产报工，缺少派工单号")
            
            # test_44: 完工
            print("test_44: 完工")
            if self.dispatch_code:
                response = self.production_workbench.completedProduction(self.dispatch_code)
                if response and response.json().get('Success') == True:
                    print("✓ 完工成功")
                else:
                    print("✗ 完工失败")
            else:
                print("✗ 无法完工，缺少派工单号")
            
            # ========== 最后阶段：数据清理 ==========
            print("\n最后阶段：数据清理")
            
            self.cleanup_basic_data()
            
            print("\n" + "="*60)
            print("调试脚本执行完成")
            print("="*60)
            
        except Exception as e:
            print("流程异常：", e)
            self.cleanup_basic_data()
            raise
        else:
            self.cleanup_basic_data()


if __name__ == "__main__":
    DebugMainProcess().run()