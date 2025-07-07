import sys
from pathlib import Path


# 将项目根目录添加到Python路径
sys.path.append(str(Path(__file__).parent.parent))
import json
from typing import Optional
import requests
from Public.address.mom import apiGetEquipmentLedgerAutoQueryDatas
from Business.mom_admin.equipment_management.equipment_ledger_management import \
    EquipmentLedgerManagement
from Toolbox.log_module import Logger
from Business.mom_admin.factory_modeling.product_materials import ProductMaterials,MaterialsBOM
from Business.mom_admin.factory_modeling.production_process import ProcessRelated
from Business.mom_admin.production_modeling.factory_model import FactoryModel
from Public.variables.mom_admin.factory_modeling import *


class DataCleaner:
    """自动化测试数据清除工具 - 按照主流程删除逻辑组织"""

    def __init__(self):
        self.logger = Logger(name="delete_data").get_logger()

    def delete_data(self, data_type: int = 1) -> Optional[dict]:
        """根据数据类型删除对应测试数据"""
        try:
            # 获取对应的删除方法并执行
            delete_method = self._get_delete_method(data_type)
            response = delete_method()
            
            if not response:
                self.logger.error("接口返回空响应")
                return {"code": 500, "message": "接口返回空响应"}

            # 验证响应并返回结果
            response.raise_for_status()
            self.logger.info(f"{self._get_data_type_name(data_type)}删除成功")
            return response.json()

        except Exception as e:
            if isinstance(e, requests.RequestException):
                self.logger.error(f"请求异常: {e}")
                return {"code": 500, "message": f"请求异常: {str(e)}"}
            elif isinstance(e, ValueError):
                self.logger.error(f"响应解析错误: {e}")
                return {"code": 500, "message": f"响应解析错误: {str(e)}"}
            else:
                self.logger.error(f"未知错误: {e}", exc_info=True)
                return {"code": 500, "message": f"未知错误: {str(e)}"}

    def _get_delete_method(self, data_type: int):
        """映射数据类型到删除方法 - 按照主流程删除顺序"""
        method_map = {
            0: self.clean_related_data,
            1: self._delete_material_data,
            2: self._delete_process_data,
            3: self._delete_process_routing_data,
            4: self._delete_product_process_route_data,  # 新增：产品工艺路线
            5: self._delete_material_bom_data,
            6: self._delete_equipment_ledger_data,
            7: self._delete_production_line_data,
            8: self._delete_workshop_data,
            # 可继续添加新数据类型...
        }
        return method_map.get(data_type, lambda: self._unsupported_data_type(data_type))

    def _delete_material_data(self):
        """删除物料数据 - 先查询ID再删除"""
        # 1. 查询物料ID
        product_materials = ProductMaterials()
        query_response = product_materials.getMaterialInfoAutoQueryDatas()
        if not query_response:
            self.logger.error("物料查询接口返回空响应")
            raise RuntimeError("物料查询失败: 接口返回空响应")
        try:
            query_response.raise_for_status()
            query_data = query_response.json()
            self.logger.debug(f"物料查询完整响应: {json.dumps(query_data, ensure_ascii=False)}")
            if not query_data.get("Attach") or len(query_data["Attach"]) == 0:
                self.logger.info("未查询到物料数据，跳过删除操作")
                return None
            material_id = query_data["Attach"][0]["Id"]
            self.logger.info(f"获取物料ID成功: {material_id}")
        except (requests.RequestException, KeyError) as e:
            self.logger.error(f"物料ID查询失败: {str(e)}")
            return None

        # 2. 使用ID执行删除
        response = product_materials.removeMaterialInfoData(material_id)
        if not response:
            self.logger.error("物料删除接口返回空响应")
            raise RuntimeError("物料删除失败: 接口返回空响应")
        try:
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"物料删除HTTP异常: {str(e)}")
            raise

    def _delete_process_data(self):
        """删除工序数据 - 先查询ID再删除"""
        # 1. 查询工序ID
        process_related = ProcessRelated()
        query_response = process_related.GetProcessInfoAutoQueryDatas()
        if not query_response:
            self.logger.error("工序查询接口返回空响应")
            raise RuntimeError("工序查询失败: 接口返回空响应")
        try:
            query_response.raise_for_status()
            query_data = query_response.json()
            self.logger.debug(f"工序查询完整响应: {json.dumps(query_data, ensure_ascii=False)}")
            if not query_data.get("Attach") or len(query_data["Attach"]) == 0:
                self.logger.info("未查询到工序数据，跳过删除操作")
                return None
            process_id = query_data["Attach"][0]["Id"]
            self.logger.info(f"获取工序ID成功: {process_id}")
        except (requests.RequestException, KeyError) as e:
            self.logger.error(f"工序ID查询失败: {str(e)}")
            return None

        # 2. 使用ID执行删除
        response = process_related.removeProcessInfoData(process_id)
        if not response:
            self.logger.error("工序删除接口返回空响应")
            raise RuntimeError("工序删除失败: 接口返回空响应")
        try:
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"工序删除HTTP异常: {str(e)}")
            raise

    def _delete_process_routing_data(self):
        """删除工艺路线数据 - 先查询ID再删除"""
        # 1. 查询工艺路线ID
        process_related = ProcessRelated()
        query_response = process_related.getProcessRoutingAutoQueryDatas()
        if not query_response:
            self.logger.error("工艺路线查询接口返回空响应")
            raise RuntimeError("工艺路线查询失败: 接口返回空响应")
        try:
            query_response.raise_for_status()
            query_data = query_response.json()
            self.logger.debug(f"工艺路线查询完整响应: {json.dumps(query_data, ensure_ascii=False)}")
            if not query_data.get("Attach") or len(query_data["Attach"]) == 0:
                self.logger.info("未查询到工艺路线数据，跳过删除操作")
                return None
            routing_id = query_data["Attach"][0]["Id"]
            self.logger.info(f"获取工艺路线ID成功: {routing_id}")
        except (requests.RequestException, KeyError) as e:
            self.logger.error(f"工艺路线ID查询失败: {str(e)}")
            return None

        # 2. 使用ID执行删除
        response = process_related.removeProcessRoutingData(routing_id)
        if not response:
            self.logger.error("工艺路线删除接口返回空响应")
            raise RuntimeError("工艺路线删除失败: 接口返回空响应")
        try:
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"工艺路线删除HTTP异常: {str(e)}")
            raise

    def _delete_product_process_route_data(self):
        """删除产品工艺路线数据 - 先查询ID再删除"""
        # 1. 查询产品工艺路线ID
        process_related = ProcessRelated()
        query_response = process_related.GetProductProcessRouteAutoQueryDatas()
        if not query_response:
            self.logger.error("产品工艺路线查询接口返回空响应")
            raise RuntimeError("产品工艺路线查询失败: 接口返回空响应")
        try:
            query_response.raise_for_status()
            query_data = query_response.json()
            self.logger.debug(f"产品工艺路线查询完整响应: {json.dumps(query_data, ensure_ascii=False)}")
            if not query_data.get("Attach") or len(query_data["Attach"]) == 0:
                self.logger.info("未查询到产品工艺路线数据，跳过删除操作")
                return None
            product_process_id = query_data["Attach"][0]["Id"]
            self.logger.info(f"获取产品工艺路线ID成功: {product_process_id}")
        except (requests.RequestException, KeyError) as e:
            self.logger.error(f"产品工艺路线ID查询失败: {str(e)}")
            return None

        # 2. 使用ID执行删除
        response = process_related.RemoveBatchProductProcessRouteDatas(product_process_id)
        if not response:
            self.logger.error("产品工艺路线删除接口返回空响应")
            raise RuntimeError("产品工艺路线删除失败: 接口返回空响应")
        try:
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"产品工艺路线删除HTTP异常: {str(e)}")
            raise

    def _delete_material_bom_data(self):
        """删除物料BOM数据 - 先查询ID和版本号再删除"""
        # 1. 查询物料BOM ID和版本号
        try:
            query_response = MaterialsBOM().getGetBomMasterViewAutoQueryDatas()
            if not query_response:
                self.logger.error("物料BOM查询接口返回空响应")
                raise RuntimeError("物料BOM查询失败: 接口返回空响应")
            query_response.raise_for_status()
            query_data = query_response.json()
            self.logger.debug(f"物料BOM查询完整响应: {json.dumps(query_data, ensure_ascii=False)}")
            if not query_data.get("Attach") or len(query_data["Attach"]) == 0:
                self.logger.info("未查询到物料BOM数据，跳过删除操作")
                return None
            material_bom_id = query_data["Attach"][0]["Id"]
            bom_version = query_data["Attach"][0].get("BOMVersion", "RUNL8249604")  # 默认版本号
            self.logger.info(f"获取物料BOM ID成功: {material_bom_id}, 版本号: {bom_version}")
        except (requests.RequestException, KeyError) as e:
            self.logger.error(f"物料BOM ID查询失败: {str(e)}")
            return None

        # 2. 使用ID和版本号执行删除
        try:
            materials_bom = MaterialsBOM()
            response = materials_bom.removeManufactureBomData(bom_version, material_bom_id)
            if not response:
                self.logger.error("物料BOM删除接口返回空响应")
                raise RuntimeError("物料BOM删除失败: 接口返回空响应")
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"物料BOM删除HTTP异常: {str(e)}")
            return None

    def _delete_equipment_ledger_data(self, url=None):
        """删除设备台账数据 - 先查询ID再删除"""
        equipment_ledger = EquipmentLedgerManagement()
        try:
            # 查询设备台账数据获取ID
            query_response = equipment_ledger.getEquipmentLedgerAutoQueryDatas()
            if not query_response:
                self.logger.error("设备台账查询接口返回空响应")
                raise RuntimeError("设备台账查询失败: 接口返回空响应")
            try:
                query_response.raise_for_status()
                query_data = query_response.json()
                self.logger.debug(f"设备台账查询完整响应: {json.dumps(query_data, ensure_ascii=False)}")
                if not query_data.get("Attach") or len(query_data["Attach"]) == 0:
                    self.logger.info("未查询到设备台账数据，跳过删除操作")
                    return None
                equipment_id = query_data["Attach"][0]["Id"]
                self.logger.info(f"获取设备台账ID成功: {equipment_id}")
            except (requests.RequestException, KeyError) as e:
                self.logger.error(f"设备台账ID查询失败: {str(e)}")
                return None

            # 使用ID执行删除
            response = equipment_ledger.removeBatchEquipmentLedger(equipment_id)
            if not response:
                self.logger.error("设备台账删除接口返回空响应")
                raise RuntimeError("设备台账删除失败: 接口返回空响应")
            
            response.raise_for_status()
            return response

        except requests.RequestException as e:
            self.logger.error(f"网络请求异常: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {str(e)}")
            raise RuntimeError("接口返回非法数据格式") from e
        except Exception as e:
            self.logger.error(f"处理异常: {type(e).__name__}", exc_info=True)
            raise

    def _delete_production_line_data(self):
        """删除产线数据 - 先查询ID再删除"""
        # 1. 查询产线ID
        query_response = FactoryModel().GetProductionLineAutoQueryDatas()
        if not query_response:
            self.logger.error("产线查询接口返回空响应")
            raise RuntimeError("产线查询失败: 接口返回空响应")
        try:
            query_response.raise_for_status()
            query_data = query_response.json()
            self.logger.debug(f"产线查询完整响应: {json.dumps(query_data, ensure_ascii=False)}")
            if not query_data.get("Attach") or len(query_data["Attach"]) == 0:
                self.logger.info("未查询到产线数据，跳过删除操作")
                return None
            production_line_id = query_data["Attach"][0]["Id"]
            self.logger.info(f"获取产线ID成功: {production_line_id}")
        except (requests.RequestException, KeyError) as e:
            self.logger.error(f"产线ID查询失败: {str(e)}")
            return None

        # 2. 使用ID执行删除
        response = FactoryModel().removeOrganizationStructureData_productionline(production_line_id)
        if not response:
            self.logger.error("产线删除接口返回空响应")
            raise RuntimeError("产线删除失败: 接口返回空响应")
        try:
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"产线删除HTTP异常: {str(e)}")
            return None

    def _delete_workshop_data(self):
        """删除车间数据 - 先查询ID再删除"""
        # 1. 查询车间ID
        query_response = FactoryModel().GetWorkshopAutoQueryDatas()
        if not query_response:
            self.logger.error("车间查询接口返回空响应")
            raise RuntimeError("车间查询失败: 接口返回空响应")
        try:
            query_response.raise_for_status()
            query_data = query_response.json()
            self.logger.debug(f"车间查询完整响应: {json.dumps(query_data, ensure_ascii=False)}")
            if not query_data.get("Attach") or len(query_data["Attach"]) == 0:
                self.logger.info("未查询到车间数据，跳过删除操作")
                return None
            workshop_id = query_data["Attach"][0]["Id"]
            self.logger.info(f"获取车间ID成功: {workshop_id}")
        except (requests.RequestException, KeyError) as e:
            self.logger.error(f"车间ID查询失败: {str(e)}")
            return None

        # 2. 使用ID执行删除
        response = FactoryModel().removeOrganizationStructureData(workshop_id)
        if not response:
            self.logger.error("车间删除接口返回空响应")
            raise RuntimeError("车间删除失败: 接口返回空响应")
        try:
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"车间删除HTTP异常: {str(e)}")
            return None

    def _unsupported_data_type(self, data_type):
        """处理不支持的数据类型"""
        raise ValueError(f"不支持的数据类型: {data_type}")

    def _get_data_type_name(self, data_type: int) -> str:
        """映射数据类型ID到友好名称"""
        name_map = {
            0: "所有数据",
            1: "物料数据",
            2: "工序数据",
            3: "工艺路线数据",
            4: "产品工艺路线数据",
            5: "物料BOM数据",
            6: "设备台账数据",
            7: "产线数据",
            8: "车间数据",
            # 可继续添加新名称...
        }
        return name_map.get(data_type, f"数据类型{data_type}")

    def clean_related_data(self):
        """批量清理所有测试数据 - 按照主流程删除顺序"""
        # 按照主流程删除顺序：先删除依赖数据，再删除基础数据
        deletion_tasks = [
            (self._delete_material_bom_data, "物料BOM数据"),
            (self._delete_process_data, "工序数据"),
            (self._delete_process_routing_data, "工艺路线数据"),
            (self._delete_product_process_route_data, "产品工艺路线数据"),
            (self._delete_material_data, "物料数据"),
            (self._delete_equipment_ledger_data, "设备台账数据"),
            (self._delete_production_line_data, "产线数据"),
            (self._delete_workshop_data, "车间数据")
        ]

        for delete_func, data_name in deletion_tasks:
            try:
                result = delete_func()
                if result is None:
                    self.logger.info(f"{data_name}不存在或已被清理，跳过删除")
                else:
                    self.logger.info(f"{data_name}清理完成")
            except Exception as e:
                self.logger.error(f"{data_name}清理失败: {str(e)}", exc_info=True)


# 使用示例
if __name__ == "__main__":
    # cleaner = DataCleaner()
    # cleaner.delete_data(1) # 删除物料数据
    # cleaner.delete_data(2) # 删除工序数据
    # cleaner.delete_data(3) # 删除工艺路线数据
    # cleaner.delete_data(4) # 删除产品工艺路线数据
    # cleaner.delete_data(5) # 删除物料BOM数据
    # cleaner.delete_data(6) # 删除设备台账数据
    # cleaner.delete_data(7) # 删除产线数据
    # cleaner.delete_data(8) # 删除车间数据
    DataCleaner().clean_related_data()  # 清理所有数据