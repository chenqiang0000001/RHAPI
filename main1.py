import json
import os
import subprocess
import requests
import time
import uuid
import zipfile
import smtplib
import subprocess
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from datetime import datetime
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


def send_email(report_dir):
    # 邮件配置
    sender = 'chq18870425154@163.com'
    receivers = ['chenqiangt@cptgroup.cn']
    smtp_server = 'smtp.163.com'
    smtp_port = 465
    username = 'chq18870425154@163.com'
    password = 'SZgTA33Q25dzp9u7'  # 邮箱授权码

    # 邮件标题
    current_date = datetime.now().strftime("%Y-%m-%d")
    subject = f"陈强的自动化测试报告{current_date}"

    # 创建邮件对象
    message = MIMEMultipart()
    message['From'] = Header(sender, 'utf-8')
    message['To'] = Header(", ".join(receivers), 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    # 生成 Allure 报告链接
    report_link = None
    if report_dir:
        try:
            # 启动 Python 简易 HTTP 服务器
            server_port = 8000
            # 在后台启动服务器，避免阻塞主线程
            if os.name == 'nt':  # Windows 系统
                subprocess.Popen(f'python -m http.server {server_port} --directory {report_dir}', shell=True)
            else:  # Linux 或 macOS 系统
                subprocess.Popen(f'python3 -m http.server {server_port} --directory {report_dir}', shell=True)
            report_link = f"http://192.168.88.1:{server_port}"
        except Exception as e:
            logger.error(f"启动 HTTP 服务器失败: {e}")

    if report_link:
        body = f"测试 Allure 报告链接：{report_link}"
    else:
        body = "测试报告生成失败，无报告链接"

    message.attach(MIMEText(body, 'plain', 'utf-8'))

    smtp_obj = None
    try:
        # 连接 SMTP 服务器
        smtp_obj = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp_obj.login(username, password)
        # 发送邮件
        smtp_obj.sendmail(sender, receivers, message.as_string())
        logger.info("邮件发送成功")
    except smtplib.SMTPException as e:
        logger.error(f"邮件发送失败: {e}")
    finally:
        if smtp_obj:
            try:
                smtp_obj.quit()
            except smtplib.SMTPServerDisconnected:
                pass


if __name__ == "__main__":
    # 执行测试用例
    test_result = run_tests()

    # 生成测试报告
    report_dir = generate_report()

    if report_dir:
        # 发送钉钉通知
        ding_status = send_dingtalk(report_dir, test_result)
        logger.info(f"钉钉发送状态码: {ding_status}")

        # 发送邮件
        send_email(report_dir)
    else:
        logger.warning("测试报告生成失败，跳过钉钉通知和邮件发送。")
