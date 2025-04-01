import json
import os
import subprocess
import requests
import time
import uuid
from Toolbox.log_module import Logger

logger = Logger(name="my_logger").get_logger()  # 实例化日志记录器


def run_tests():
    """执行 pytest 测试并生成 Allure 数据"""
    try:
        # 清理历史数据
        if os.path.exists("allure-results"):
            if os.name == 'nt':  # Windows 系统
                subprocess.run(["rmdir", "/s", "/q", "allure-results"], check=True, shell=True)
            else:  # Linux 或 macOS 系统
                subprocess.run(["rm", "-rf", "allure-results"], check=True)

        # 执行测试命令
        command = f"pytest D:\\apiAutomationRH\\TestCase --alluredir=./allure-results -v"
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'  # 编码指定
        )
        if result.returncode != 0:
            logger.error(f"测试执行失败，错误信息: {result.stderr}")
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"执行测试命令时出错: {e}")
        return 1


def generate_report():
    """生成 Allure 测试报告"""
    try:
        report_dir = f"allure-report/{uuid.uuid4().hex[:8]}"
        command = ["allure", "generate", "./allure-results", "-o", report_dir, "--clean"]
        subprocess.run(command, check=True, shell=True)
        return report_dir
    except subprocess.CalledProcessError as e:
        logger.error(f"生成测试报告时出错: {e}")
        return None


def send_dingtalk(report_path, test_result):
    try:
        with open("test_stats.json", "r", encoding="utf-8") as f:
            test_data = json.load(f)
    except FileNotFoundError:
        test_data = {"total": 0, "passed": 0, "failed": 0,
                     "priority_stats": {"grade_1": 0, "grade_2": 0, "grade_3": 0, "grade_4": 0}}
    webhook_url = os.getenv("DINGTALK_WEBHOOK")
    if not webhook_url:
        logger.error("未配置钉钉 Webhook")
        return 500

    status_text = "成功" if test_result == 0 else "失败"
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": "自动化测试报告详情",
            "text": f"### 测试执行{status_text}\n"
                    f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"**用例总数**: {test_data['total']}\n"
                    f"**成功数量**: {test_data['passed']}\n"
                    f"**优先级统计**: \n"
                    f" - @grade_1: {test_data['priority_stats']['grade_1']}\n"
                    f" - @grade_2: {test_data['priority_stats']['grade_2']}\n"
                    f" - @grade_3: {test_data['priority_stats']['grade_3']}\n"
                    f" - @grade_4: {test_data['priority_stats']['grade_4']}\n"
        }
    }
    response = requests.post(webhook_url, json=message)
    response.raise_for_status()
    return response.status_code


if __name__ == "__main__":
    # 执行测试用例
    test_result = run_tests()

    # 生成测试报告
    report_dir = generate_report()

    if report_dir:
        # 发送钉钉通知
        ding_status = send_dingtalk(report_dir, test_result)
        logger.info(f"钉钉发送状态码: {ding_status}")
    else:
        logger.warning("测试报告生成失败，跳过钉钉通知。")
