import os
import subprocess
import requests
import time
import uuid
import smtplib
import socket
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
from Toolbox.log_module import Logger
import logging
import sys

# 日志配置：所有日志写入 run.log，控制台也输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('run.log', encoding='utf-8', mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)

# logger对象
logger = logging.getLogger("run_tests")

import json
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


def run_tests():
    """测试运行器，负责执行测试、生成报告和发送通知"""
    try:
        # 清理历史数据
        if os.path.exists("allure-results"):
            if os.name == 'nt':  # Windows 系统
                subprocess.run(["rmdir", "/s", "/q", "allure-results"], check=True, shell=True)
            else:  # Linux 或 macOS 系统
                subprocess.run(["rm", "-rf", "allure-results"], check=True)

        # 执行测试命令
        command = config["pytest_command"]
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=1000  # 设置超时时间为1小时，对于测试执行来说更合理
            )
        except subprocess.TimeoutExpired as te:
            logger.error(f"测试执行超时: {te}")
            return 2
        except KeyboardInterrupt:
            logger.warning("用户主动中断测试执行")
            return 130
        except Exception as e:
            logger.error(f"未知错误: {e}")
            return 1
        # 记录完整执行日志
        logger.debug('测试命令标准输出:\n{}'.format(getattr(result, 'stdout', None)))
        logger.debug('测试命令标准错误:\n{}'.format(getattr(result, 'stderr', None)))
        if result.returncode != 0:
            error_msg = getattr(result, 'stderr', None) or getattr(result, 'stdout', None)
            logger.error(f"测试执行失败，错误信息: {error_msg}")
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"执行测试命令时出错: {e}")
        return 1


def predict_defects():
    """模拟缺陷预测结果（需根据实际业务逻辑实现）"""
    import numpy as np
    # 生成随机预测数据（示例用）
    return np.random.rand(10) > 0.5  # 返回布尔数组表示是否预测为缺陷


def generate_report():
    """生成 Allure 测试报告"""
    try:
        report_dir = f"allure-report/{uuid.uuid4().hex[:8]}"
        allure_path = config["allure_path"]  # 从配置文件获取allure路径
        command = [allure_path, "generate", "./allure-results", "-o", report_dir, "--clean"]
        subprocess.run(command, check=True, shell=True)

        # 验证报告静态资源文件
        static_files = ['styles.css', 'app.js', 'favicon.ico']
        missing_files = []
        for file in static_files:
            # 检查报告目录下直接的静态文件
            file_path = os.path.join(report_dir, file)
            if not os.path.exists(file_path):
                # 检查可能的static子目录
                plugin_path = os.path.join(report_dir, 'plugins', 'screenDiff', file)
                static_path = os.path.join(report_dir, 'static', file)
                if not os.path.exists(plugin_path) and not os.path.exists(static_path):
                    missing_files.append(file)
        
        if missing_files:
            logger.warning(f"报告目录中缺少以下静态资源文件: {', '.join(missing_files)}")
            # 如果关键文件缺失，返回None表示报告生成失败
            if 'styles.css' in missing_files or 'app.js' in missing_files:
                logger.error("关键静态资源文件缺失，报告生成失败")
                return None

        # 在 Allure 报告中添加优先级和缺陷预测结果
        defects_predictions = predict_defects()
        if defects_predictions is not None:
            with open(os.path.join(report_dir, "extra_info.json"), "w", encoding="utf-8") as f:
                json.dump(defects_predictions.tolist(), f, ensure_ascii=False, indent=4)

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
    webhook_url = config.get("dingtalk_webhook") or os.getenv("DINGTALK_WEBHOOK")
    if not webhook_url:
        logger.error("未配置钉钉 Webhook")
        return 500

    status_text = "成功" if test_result == 0 else "失败"
    # 生成 Allure 报告链接（切换为测试平台/report入口）
    if report_path:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = '127.0.0.1'
        finally:
            s.close()
        report_link = f"http://{local_ip}:5000/report/{os.path.basename(report_path)}/index.html"
        report_text = f"[点击查看Allure测试报告]({report_link})"
    else:
        report_text = "测试报告生成失败，无报告链接"

    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": "自动化测试报告详情",
            "text": f"### 测试执行{status_text}\n"\
                    f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"\
                    f"**用例总数**: {test_data['total']}\n"\
                    f"**成功数量**: {test_data['passed']}\n"\
                    f"**优先级统计**: \n"\
                    f" - @grade_1: {test_data['priority_stats']['grade_1']}\n"\
                    f" - @grade_2: {test_data['priority_stats']['grade_2']}\n"\
                    f" - @grade_3: {test_data['priority_stats']['grade_3']}\n"\
                    f" - @grade_4: {test_data['priority_stats']['grade_4']}\n"\
                    f"{report_text}"
        }
    }
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        return response.status_code
    except requests.RequestException as e:
        logger.error(f"发送钉钉通知失败: {e}")
        return 500


def send_email(report_dir):
    # 邮件配置
    # 从配置文件获取邮件参数
    sender = config["email_config"]["sender"]
    receivers = config["email_config"]["receivers"]
    smtp_server = config["email_config"]["smtp_server"]
    smtp_port = config["email_config"]["smtp_port"]
    username = config["email_config"]["username"]
    password = config["email_config"]["password"]

    # 邮件标题
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"陈强的自动化测试报告{current_date}"

    # 创建邮件对象
    message = MIMEMultipart()
    message['From'] = str(Header(sender, 'utf-8'))
    message['To'] = str(Header(", ".join(receivers), 'utf-8'))
    message['Subject'] = str(Header(subject, 'utf-8'))

    # 生成 Allure 报告链接（切换为测试平台/report入口）
    if report_dir:
        # 获取本机IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = '127.0.0.1'
        finally:
            s.close()
        report_link = f"http://{local_ip}:5000/report/{os.path.basename(report_dir)}/index.html"
        with open('config.yaml', 'r', encoding='utf-8') as f:
            yaml_config = yaml.safe_load(f)
        environment = yaml_config.get('environment', {})
        env_type = environment.get('current', 'test')
        env_url = environment.get('test_url' if env_type == 'test' else 'formal_url', '')
        env_info = f"当前环境：{'测试环境' if env_type == 'test' else '正式环境'}, 环境地址：{env_url}<br>"
        body = env_info + f"尊敬的各位领导.同事:<br>  MOM接口自动化测试脚本已运行完成, <br>  Allure 报告链接：<a href='{report_link}'>{report_link}</a><br>  测试内容:生产主流程 <br>   测试范围:前置条件：自动数据清除，防止残留数据1.产品物料：新增物料，查询物料，新增物料BOM.新增物料BOM明细.查询物料BOM 2.产品工艺：新增工序.查询工序.新增工艺路线.查询工艺路线.工艺路线绑定工序.产品绑定工艺路线.工艺路线绑定产品.查询产品工艺路线.产品工序BOM绑定 3.设备台账：新增设备台账.查询设备台账 4.ESOP:新增ESOP文件.审核ESOP文件.新增工艺路线ESOP文件审核工艺路线.ESOP文件 5.工厂布局：新增车间.查询车间.新增产线.查询产线 6.质量管理：创建检验方案 7.安灯管理：创建安灯规则.查询安灯规则  8.生产管理：创建生产计划.确认生产计划.下达生产计划.创建派工单.查询派工单.派工单下达 9.开工及查看SOP:开始生产.查看SOP 10.质量检验：创建首检单.查询检验单.开始检验.提交检验结果 11.标签拆分：扫描标签.标签拆分 12.安灯呼叫：安灯呼叫.安灯签到.安灯开始处理.安灯结束处理.安灯处理确认 13.上料及完工：上料扫描SN.确认上料.生产报工.生产完工 14.数据清理：删除工序.删除工艺路线.删除设备台账.删除产线.删除车间.删除物料BOM.删除物料.删除安灯规则 <br>   此报告为执行完毕自动发送"
    else:
        body = "测试报告生成失败，无报告链接"

    message.attach(MIMEText(body, 'html', 'utf-8'))

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
    logger.info(f"run_tests 返回码: {test_result}")
    logging.info(f"run_tests 返回码: {test_result}")
    for handler in logging.getLogger().handlers:
        handler.flush()

    # 生成测试报告
    report_dir = generate_report()
    logger.info(f"generate_report 返回: {report_dir}")
    logging.info(f"generate_report 返回: {report_dir}")
    for handler in logging.getLogger().handlers:
        handler.flush()

    if report_dir:
        # 发送钉钉通知
        ding_status = send_dingtalk(report_dir, test_result)
        logger.info(f"钉钉发送状态码: {ding_status}")
        logging.info(f"钉钉发送状态码: {ding_status}")
        for handler in logging.getLogger().handlers:
            handler.flush()

        # 发送邮件
        send_email(report_dir)
        logger.info("邮件发送完成")
        logging.info("邮件发送完成")
        for handler in logging.getLogger().handlers:
            handler.flush()
    else:
        logger.warning("测试报告生成失败，跳过钉钉通知和邮件发送。")
        logging.warning("测试报告生成失败，跳过钉钉通知和邮件发送。")
        for handler in logging.getLogger().handlers:
            handler.flush()

    # 脚本结束标记
    logging.info('===TEST_FINISHED===')
    for handler in logging.getLogger().handlers:
        handler.flush()