import allure
import json
from typing import Optional, Dict, Any
from Toolbox.log_module import Logger


class BaseTest:
    """基础测试类，提供通用的测试方法和工具"""
    
    def __init__(self):
        self.logger = Logger(name=self.__class__.__name__).get_logger()
    
    def verify_api_response(self, 
                           response, 
                           expected_status: int = 200, 
                           expected_message: Optional[str] = None,
                           expected_success: Optional[bool] = None,
                           check_token: bool = False) -> Dict[str, Any]:
        """
        验证API响应
        
        Args:
            response: API响应对象
            expected_status: 期望的HTTP状态码
            expected_message: 期望的响应消息
            expected_success: 期望的Success字段值
            check_token: 是否检查token字段
            
        Returns:
            响应体字典
        """
        try:
            # 检查响应是否为空
            assert response is not None, "API响应为空"
            
            # 检查状态码
            assert response.status_code == expected_status, \
                f"期望状态码{expected_status}，实际为{response.status_code}"
            
            # 解析响应体
            response_body = response.json()
            
            # 检查Success字段
            if expected_success is not None:
                assert response_body.get('Success') == expected_success, \
                    f"期望Success={expected_success}，实际为{response_body.get('Success')}"
            
            # 检查消息字段
            if expected_message is not None:
                actual_message = response_body.get('Message', '')
                assert actual_message == expected_message, \
                    f"期望消息'{expected_message}'，实际为'{actual_message}'"
            
            # 检查token字段
            if check_token:
                assert 'token' in response_body, "响应中缺少token字段"
                assert response_body['token'], "token字段为空"
            
            return response_body
            
        except AssertionError as e:
            self.logger.error(f"API响应验证失败: {str(e)}")
            if response:
                self.logger.error(f"实际响应: {response.text}")
            raise e
        except Exception as e:
            self.logger.error(f"API响应验证异常: {str(e)}")
            raise e
    
    def log_test_info(self, test_name: str, response_body: Dict[str, Any], expected_result: str):
        """
        记录测试信息
        
        Args:
            test_name: 测试方法名
            response_body: 响应体
            expected_result: 期望结果描述
        """
        self.logger.info(f"测试方法: {test_name}")
        self.logger.info(f"期望结果: {expected_result}")
        self.logger.info(f"实际响应: {json.dumps(response_body, ensure_ascii=False, indent=2)}")
        
        # 添加到Allure报告
        allure.attach(
            json.dumps(response_body, ensure_ascii=False, indent=2),
            name="API响应",
            attachment_type=allure.attachment_type.JSON
        )
    
    def log_test_error(self, test_name: str, error_message: str, response_text: Optional[str] = None):
        """
        记录测试错误信息
        
        Args:
            test_name: 测试方法名
            error_message: 错误消息
            response_text: 响应文本（可选）
        """
        self.logger.error(f"测试方法: {test_name}")
        self.logger.error(f"错误信息: {error_message}")
        
        if response_text:
            self.logger.error(f"响应内容: {response_text}")
            allure.attach(
                response_text,
                name="错误响应",
                attachment_type=allure.attachment_type.TEXT
            )
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        pass
    
    def teardown_method(self):
        """每个测试方法执行后的清理"""
        pass 