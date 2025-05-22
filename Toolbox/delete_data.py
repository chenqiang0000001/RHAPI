from typing import Optional
import requests
from Toolbox.log_module import Logger
from Business.mom_admin.factory_modeling.product_materials import ProductMaterials
from Business.mom_admin.factory_modeling.production_process import ProcessRelated

# 配置日志
logger = Logger(name="delete_data").get_logger()


class DataCleaner:
    """自动化测试数据清除工具"""

    def delete_data(self, data_type: int = 1) -> Optional[dict]:
        """根据数据类型删除对应测试数据"""
        try:
            # 获取对应的删除方法并执行
            delete_method = self._get_delete_method(data_type)
            response = delete_method()

            # 验证响应并返回结果
            response.raise_for_status()
            logger.info(f"{self._get_data_type_name(data_type)}删除成功")
            return response.json()

        except Exception as e:
            if isinstance(e, requests.RequestException):
                logger.error(f"请求异常: {e}")
                return {"code": 500, "message": f"请求异常: {str(e)}"}
            elif isinstance(e, ValueError):
                logger.error(f"响应解析错误: {e}")
                return {"code": 500, "message": f"响应解析错误: {str(e)}"}
            else:
                logger.error(f"未知错误: {e}", exc_info=True)
                return {"code": 500, "message": f"未知错误: {str(e)}"}

    def _get_delete_method(self, data_type: int):
        """映射数据类型到删除方法"""
        method_map = {
            1: self._delete_material_data,
            2: self._delete_process_data,  # 新增工艺数据删除映射
            3: self._delete_process_routing_data,  # 新增工艺路线数据删除映射
            # 可继续添加新数据类型...
        }
        return method_map.get(data_type, lambda: self._unsupported_data_type(data_type))

    def _delete_material_data(self):
        """删除物料数据"""
        # 直接返回requests.Response对象
        return ProductMaterials().removeMaterialInfoData()

    def _delete_process_data(self):
        """删除工序数据"""
        process_related = ProcessRelated()
        # 假设需要删除的工序编码和名称，实际使用时可根据需求调整
        process_code = "example_process_code"
        process_name = "example_process_name"
        return process_related.removeProcessInfoData(ProcessCode=process_code, ProcessName=process_name)

    def _delete_process_routing_data(self):
        """删除工艺路线数据"""
        process_related = ProcessRelated()
        # 假设需要删除的工艺路线编码，实际使用时可根据需求调整
        process_routing_code = "example_routing_code"
        return process_related.removeProcessRoutingData(ProcessRoutingCode=process_routing_code)

    def _unsupported_data_type(self, data_type):
        """处理不支持的数据类型"""
        raise ValueError(f"不支持的数据类型: {data_type}")

    def _get_data_type_name(self, data_type: int) -> str:
        """映射数据类型ID到友好名称"""
        name_map = {
            1: "物料数据",
            2: "工序数据",  # 新增友好名称
            3: "工艺路线数据",  # 新增友好名称
            # 可继续添加新名称...
        }
        return name_map.get(data_type, f"数据类型{data_type}")


# 使用示例
if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.delete_data(1) # 删除物料数据
    cleaner.delete_data(2) # 删除工序数据
    cleaner.delete_data(3) # 删除工艺路线数据

