# import smtplib
# from email.header import Header
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication
#
#
# class SendEmail:
#
#     # 初始化服务器信息
#     def __init__(self, mail_host, mail_user, mail_pass, sender, receives):
#         self.mail_host = mail_host
#         self.mail_user = mail_user
#         self.mail_pass = mail_pass
#         self.sender = sender
#         self.receivers = receives
#
#     # 以文本的形式发送邮件
#     def make_email_by_text(self, context, subject, from_address, to_address):
#         message = MIMEText(context, 'plain', 'UTF-8')
#         message['Subject'] = subject  # 邮件标题
#         message['From'] = Header(from_address, "utf-8")  # 邮件主体中发送者名称
#         message['To'] = Header(to_address, "utf-8")  # 邮件主体中接收者名称
#         self.send_email(message)
#
#     # 以文本和附件的形式发送邮件
#     def make_email_by_att(self, content, file_path, subject, from_address, to_address):
#         message = MIMEMultipart()
#         message['Subject'] = subject  # 邮件标题
#         message['From'] = Header(from_address, "utf-8")  # 邮件主体中发送者名称
#         message['To'] = Header(to_address, "utf-8")  # 邮件主体中接收者名称
#         body = MIMEText(content, 'plain', 'utf-8')
#         message.attach(body)
#         att_body = open(file_path, 'rb')  # 以二进制的格式打开附件
#         att = MIMEApplication(att_body.read())  # 导入附件
#         att_body.close()
#         att.add_header('Content-Disposition', 'attachment', filename='allure测试报告.zip')  # 添加附件名称
#         message.attach(att)
#         self.send_email(message)
#
#     # 登录并进行发送
#     def send_email(self, message):
#
#         # 进行登录发送
#         try:
#             smtpobj = smtplib.SMTP()
#             smtpobj.connect(self.mail_host, 25)
#             smtpobj.login(self.mail_user, self.mail_pass)
#             smtpobj.sendmail(self.sender, self.receivers, message.as_string())
#             smtpobj.quit()
#             print('success')
#         except Exception as e:
#             print(f'error: {e}')
#             raise e
#
#
# if __name__ == '__main__':
#     content = "陈强的自动化测试报告"
#     file_path = "邮件主体中发送者名称"
#     subject = "111"
#     from_address = "www"
#     to_address = "333"
#     a = SendEmail(content, file_path, subject, from_address, to_address).make_email_by_att(content, file_path, subject, from_address, to_address)
import json
import os
import subprocess
import requests
import time
import uuid
from Toolbox.log_module import Logger
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
from datetime import datetime

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
    sender = 'chenqiangt@cptgroup.cn'
    receivers = ['chq18870425154@163.com']
    smtp_server = 'smtp.cptgroup.cn'  # 请根据实际情况修改
    smtp_port = 587  # 请根据实际情况修改
    username = 'chenqiangt@cptgroup.cn'
    password = 'your_email_password'  # 请替换为你的邮箱授权码

    # 邮件标题
    current_date = datetime.now().strftime("%Y-%m-%d")
    subject = f"陈强的自动化测试报告{current_date}"

    # 创建邮件对象
    message = MIMEMultipart()
    message['From'] = Header(sender, 'utf-8')
    message['To'] = Header(", ".join(receivers), 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文
    body = "测试allure报告"
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    # 添加附件
    if report_dir:
        zip_command = f'zip -r allure_report.zip {report_dir}'
        subprocess.run(zip_command, shell=True)
        with open('allure_report.zip', 'rb') as f:
            attachment = MIMEApplication(f.read())
            attachment.add_header('Content-Disposition', 'attachment', filename='allure_report.zip')
            message.attach(attachment)

    try:
        # 连接 SMTP 服务器
        smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
        smtp_obj.starttls()
        smtp_obj.login(username, password)
        # 发送邮件
        smtp_obj.sendmail(sender, receivers, message.as_string())
        logger.info("邮件发送成功")
    except smtplib.SMTPException as e:
        logger.error(f"邮件发送失败: {e}")
    finally:
        if 'smtp_obj' in locals():
            smtp_obj.quit()


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