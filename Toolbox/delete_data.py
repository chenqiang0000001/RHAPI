import json
from typing import Optional
import requests
from Business.mom_admin.equipment_management.equipment_ledger_management import \
    EquipmentLedgerManagement
from Toolbox.log_module import Logger
from Business.mom_admin.factory_modeling.product_materials import ProductMaterials
from Business.mom_admin.factory_modeling.production_process import ProcessRelated



class DataCleaner:
    """自动化测试数据清除工具"""

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
        """映射数据类型到删除方法"""
        method_map = {
            0: self.clean_related_data,
            1: self._delete_material_data,
            2: self._delete_process_data,
            3: self._delete_process_routing_data,
            4: self._delete_equipment_ledger_data,
            # 可继续添加新数据类型...
        }
        return method_map.get(data_type, lambda: self._unsupported_data_type(data_type))

    def _delete_material_data(self):
        """删除物料数据"""
        response = ProductMaterials().removeMaterialInfoData()
        if not response:
            self.logger.error("物料接口返回空响应")
            raise RuntimeError("物料删除失败: 接口返回空响应")
        try:
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"物料删除HTTP异常: {str(e)}")
            raise

    def _delete_process_data(self):
        """删除工序数据"""
        process_related = ProcessRelated()
        response = process_related.removeProcessInfoData()
        if not response:
            self.logger.error("工序接口返回空响应")
            raise RuntimeError("工序删除失败: 接口返回空响应")
        try:
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"工序删除HTTP异常: {str(e)}")
            raise

    def _delete_process_routing_data(self):
        """删除工艺路线数据"""
        process_related = ProcessRelated()
        response = process_related.removeProcessRoutingData()
        if not response:
            self.logger.error("工艺路线接口返回空响应")
            raise RuntimeError("工艺路线删除失败: 接口返回空响应")
        try:
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"工艺路线删除HTTP异常: {str(e)}")
            raise

    def _delete_equipment_ledger_data(self):
        """删除设备台账数据"""
        equipment_ledger = EquipmentLedgerManagement()
        # 增强响应验证机制
        try:
            # 执行删除请求
            response = equipment_ledger.removeBatchEquipmentLedger()

            # 基础验证
            if not isinstance(response, requests.Response):
                error_type = type(response).__name__
                self.logger.error(f"无效响应类型: {error_type}")
                raise TypeError(f"预期Response对象，实际得到{error_type}")

            # 记录调试信息
            self.logger.debug(f"请求详情 => URL: {response.request.url}  Body: {response.request.body}")

            # 统一响应验证
            response.raise_for_status()
            response_data = response.json()

            if not response_data.get('Success'):
                error_msg = response_data.get('Message', '未知业务错误')
                self.logger.error(f"业务校验失败: {error_msg}")
                self.logger.debug(f"完整响应: {response.text[:500]}")
                raise ValueError(f"业务处理失败: {error_msg}")

            return response

        except requests.RequestException as e:
            self.logger.error(f"网络请求异常: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {str(e)}")
            self.logger.debug(f"原始响应: {response.text[:500]}" if response else "无有效响应")
            raise RuntimeError("接口返回非法数据格式") from e
        except Exception as e:
            self.logger.error(f"处理异常: {type(e).__name__}", exc_info=True)
            raise

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
            4: "设备台账数据",
            # 可继续添加新名称...
        }
        return name_map.get(data_type, f"数据类型{data_type}")

    def clean_related_data(self):
        """批量清理所有测试数据"""
        try:
            self._delete_material_data()
            self.logger.info("物料数据清理完成")
            self._delete_process_data()
            self.logger.info("工序数据清理完成")
            self._delete_process_routing_data()
            self.logger.info("工艺路线数据清理完成")
            self._delete_equipment_ledger_data()
            self.logger.info("设备台账数据清理完成")
        except Exception as e:
            self.logger.error(f"数据清理过程中发生错误: {e}", exc_info=True)
            raise


# 使用示例
if __name__ == "__main__":
    # cleaner = DataCleaner()
    # cleaner.delete_data(1) # 删除物料数据
    # cleaner.delete_data(2) # 删除工序数据
    # cleaner.delete_data(3) # 删除工艺路线数据
    DataCleaner().delete_data(0) #删除设备台账数据