import json
import os
import subprocess
import requests
import time
import uuid
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
from Toolbox.log_module import Logger
from Toolbox.yaml_util import read_yaml

logger = Logger(name="my_logger").get_logger()  # 实例化日志记录器
config = read_yaml('config.yaml')


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
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        return response.status_code
    except requests.RequestException as e:
        logger.error(f"发送钉钉通知失败: {e}")
        return 500


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
        start_port = 8000
        max_port = 9000
        server_port = None
        for port in range(start_port, max_port):
            try:
                # 检查端口是否可用
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('0.0.0.0', port))
                logger.info(f"端口 {port} 可用，尝试启动服务器...")
                # 启动 Python 简易 HTTP 服务器
                if os.name == 'nt':  # Windows 系统
                    subprocess.Popen(f'python -m http.server {port} --directory {report_dir}', shell=True)
                else:  # Linux 或 macOS 系统
                    subprocess.Popen(f'python3 -m http.server {port} --directory {report_dir}', shell=True)
                server_port = port

                # 增加等待时间
                time.sleep(3)

                # 检查端口是否可连接
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as check_sock:
                    result = check_sock.connect_ex((local_ip, server_port))
                    if result == 0:
                        logger.info(f"端口 {server_port} 可连接，生成报告链接...")
                        report_link = f"http://{local_ip}:{server_port}"
                        break
                    else:
                        logger.error(f"端口 {server_port} 无法连接，可能服务器启动失败，继续尝试下一个端口...")
                        continue
            except OSError:
                # logger.info(f"端口 {port} 已被占用或不可用，继续尝试下一个端口...")
                continue

        if not report_link:
            logger.error("未找到可用且可连接的端口")

    if report_link:
        body = f"尊敬的各位领导.同事:\n  MOM接口自动化测试脚本已运行完成，\n  Allure 报告链接：{report_link}\n   此报告为执行完毕自动发送"
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
# import json
# import os
# import subprocess
# import requests
# import time
# import uuid
# import smtplib
# import socket
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.header import Header
# from datetime import datetime
# from Toolbox.log_module import Logger
# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.metrics import accuracy_score
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
# import allure
#
# logger = Logger(name="my_logger").get_logger()  # 实例化日志记录器
#
# # 默认的测试用例文件格式规则
# DEFAULT_TEST_CASE_FORMAT = {
#     "execution_time": "# execution_time:",
#     "priority": "# priority:"
# }
#
# # 默认的测试日志文件格式规则
# DEFAULT_TEST_LOG_FORMAT = {
#     "execution_time": "Execution Time:",
#     "is_failed": "Test Failed:"
# }
#
#
# # 加载历史测试数据
# def load_history_data():
#     try:
#         with open("history_test_data.json", "r", encoding="utf-8") as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return []
#
#
# # 保存历史测试数据
# def save_history_data(data):
#     with open("history_test_data.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)
#
#
# # 从测试用例文件中提取信息
# def extract_test_case_info(file_path, test_case_format=DEFAULT_TEST_CASE_FORMAT):
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             content = f.read()
#             execution_time = None
#             priority = None
#             for line in content.splitlines():
#                 if line.startswith(test_case_format["execution_time"]):
#                     execution_time = int(line.split(":")[1].strip())
#                 if line.startswith(test_case_format["priority"]):
#                     priority = int(line.split(":")[1].strip())
#             return execution_time, priority
#     except Exception as e:
#         logger.error(f"提取测试用例信息时出错: {e}")
#         return None, None
#
#
# # 测试用例优先级排序
# def prioritize_test_cases():
#     history_data = load_history_data()
#     if not history_data:
#         return None
#
#     df = pd.DataFrame(history_data)
#     X = df[['execution_time', 'failure_rate', 'priority']]
#     y = df['is_failed']
#
#     # 划分训练集和测试集
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
#     # 定义参数网格
#     param_grid = {
#         'n_estimators': [50, 100, 200],
#         'max_depth': [None, 10, 20, 30]
#     }
#
#     # 创建随机森林分类器
#     clf = RandomForestClassifier()
#
#     # 使用网格搜索进行参数调优
#     grid_search = GridSearchCV(clf, param_grid, cv=5)
#     grid_search.fit(X_train, y_train)
#
#     # 获取最佳模型
#     best_clf = grid_search.best_estimator_
#
#     # 从测试用例文件中获取新的测试用例
#     new_test_cases = []
#     test_case_files = os.listdir("TestCase/functional_tests")
#     for file in test_case_files:
#         if file.endswith(".py"):
#             file_path = os.path.join("TestCase/functional_tests", file)
#             execution_time, priority = extract_test_case_info(file_path)
#             if execution_time is not None and priority is not None:
#                 new_test_cases.append({
#                     'execution_time': execution_time,
#                     'failure_rate': 0.1,  # 可以根据实际情况调整
#                     'priority': priority
#                 })
#
#     new_df = pd.DataFrame(new_test_cases)
#     new_predictions = best_clf.predict_proba(new_df)[:, 1]
#
#     # 根据预测结果对测试用例进行排序
#     sorted_indices = new_predictions.argsort()[::-1]
#     sorted_test_cases = [new_test_cases[i] for i in sorted_indices]
#
#     return sorted_test_cases
#
#
# # 构建深度学习模型
# def create_model():
#     model = Sequential([
#         Dense(64, activation='relu', input_shape=(3,)),
#         Dense(1, activation='sigmoid')
#     ])
#     model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#     return model
#
#
# # 缺陷预测
# def predict_defects():
#     history_data = load_history_data()
#     if not history_data:
#         return None
#
#     data = pd.DataFrame(history_data)
#     X = data[['execution_time', 'failure_rate', 'priority']]
#     y = data['is_failed']
#
#     # 划分训练集和测试集
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
#     # 创建 Keras 分类器
#     model = KerasClassifier(build_fn=create_model)
#
#     # 定义参数网格
#     param_grid = {
#         'epochs': [10, 20, 30],
#         'batch_size': [16, 32, 64]
#     }
#
#     # 使用网格搜索进行参数调优
#     grid_search = GridSearchCV(model, param_grid, cv=5)
#     grid_search.fit(X_train, y_train)
#
#     # 获取最佳模型
#     best_model = grid_search.best_estimator_
#
#     # 从测试用例文件中获取新的测试用例
#     new_test_cases = []
#     test_case_files = os.listdir("TestCase/functional_tests")
#     for file in test_case_files:
#         if file.endswith(".py"):
#             file_path = os.path.join("TestCase/functional_tests", file)
#             execution_time, priority = extract_test_case_info(file_path)
#             if execution_time is not None and priority is not None:
#                 new_test_cases.append({
#                     'execution_time': execution_time,
#                     'failure_rate': 0.1,  # 可以根据实际情况调整
#                     'priority': priority
#                 })
#
#     new_df = pd.DataFrame(new_test_cases)
#     new_predictions = best_model.predict(new_df)
#
#     return new_predictions
#
#
# # 从测试日志中提取信息
# def extract_test_log_info(file_path, test_log_format=DEFAULT_TEST_LOG_FORMAT):
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             content = f.read()
#             execution_time = None
#             is_failed = None
#             for line in content.splitlines():
#                 if line.startswith(test_log_format["execution_time"]):
#                     execution_time = int(line.split(":")[1].strip())
#                 if line.startswith(test_log_format["is_failed"]):
#                     is_failed = line.split(":")[1].strip().lower() == "true"
#             return execution_time, is_failed
#     except Exception as e:
#         logger.error(f"提取测试日志信息时出错: {e}")
#         return None, None
#
#
# # 执行 pytest 测试并生成 Allure 数据
# def run_tests():
#     try:
#         # 清理历史数据
#         if os.path.exists("allure-results"):
#             if os.name == 'nt':  # Windows 系统
#                 subprocess.run(["rmdir", "/s", "/q", "allure-results"], check=True, shell=True)
#             else:  # Linux 或 macOS 系统
#                 subprocess.run(["rm", "-rf", "allure-results"], check=True)
#
#         # 对测试用例进行优先级排序
#         sorted_test_cases = prioritize_test_cases()
#         if sorted_test_cases:
#             # 这里可以根据排序结果调整测试用例的执行顺序
#             pass
#
#         # 执行测试命令
#         command = f"pytest D:\\apiAutomationRH\\TestCase --alluredir=./allure-results -v"
#         result = subprocess.run(
#             command,
#             shell=True,
#             capture_output=True,
#             text=True,
#             encoding='utf-8'  # 编码指定
#         )
#         if result.returncode != 0:
#             logger.error(f"测试执行失败，错误信息: {result.stderr}")
#
#         # 记录本次测试结果到历史数据
#         history_data = load_history_data()
#         test_log_files = os.listdir("allure-results")
#         for file in test_log_files:
#             if file.endswith("-attachment.txt"):
#                 file_path = os.path.join("allure-results", file)
#                 execution_time, is_failed = extract_test_log_info(file_path)
#                 if execution_time is not None and is_failed is not None:
#                     # 假设可以从测试用例文件中获取优先级
#                     test_case_name = file.split("-attachment.txt")[0]
#                     test_case_file = os.path.join("TestCase/functional_tests", f"{test_case_name}.py")
#                     _, priority = extract_test_case_info(test_case_file)
#                     if priority is not None:
#                         new_test_case = {
#                             'execution_time': execution_time,
#                             'failure_rate': 0.1 if is_failed else 0,  # 可以根据实际情况调整
#                             'priority': priority,
#                             'is_failed': is_failed
#                         }
#                         history_data.append(new_test_case)
#
#         save_history_data(history_data)
#
#         return result.returncode
#     except subprocess.CalledProcessError as e:
#         logger.error(f"执行测试命令时出错: {e}")
#         return 1
#
#
# # 生成 Allure 测试报告
# def generate_report():
#     try:
#         report_dir = f"allure-report/{uuid.uuid4().hex[:8]}"
#         command = ["allure", "generate", "./allure-results", "-o", report_dir, "--clean"]
#         subprocess.run(command, check=True, shell=True)
#
#         # 在 Allure 报告中添加优先级和缺陷预测结果
#         defects_predictions = predict_defects()
#         if defects_predictions is not None:
#             with open(os.path.join(report_dir, "extra_info.json"), "w", encoding="utf-8") as f:
#                 json.dump(defects_predictions.tolist(), f, ensure_ascii=False, indent=4)
#
#         return report_dir
#     except subprocess.CalledProcessError as e:
#         logger.error(f"生成测试报告时出错: {e}")
#         return None
#
#
# # 发送钉钉通知
# def send_dingtalk(report_path, test_result):
#     try:
#         with open("test_stats.json", "r", encoding="utf-8") as f:
#             test_data = json.load(f)
#     except FileNotFoundError:
#         test_data = {"total": 0, "passed": 0, "failed": 0,
#                      "priority_stats": {"grade_1": 0, "grade_2": 0, "grade_3": 0, "grade_4": 0}}
#     webhook_url = os.getenv("DINGTALK_WEBHOOK")
#     if not webhook_url:
#         logger.error("未配置钉钉 Webhook")
#         return 500
#
#     status_text = "成功" if test_result == 0 else "失败"
#     message = {
#         "msgtype": "markdown",
#         "markdown": {
#             "title": "自动化测试报告详情",
#             "text": f"### 测试执行{status_text}\n"
#                     f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
#                     f"**用例总数**: {test_data['total']}\n"
#                     f"**成功数量**: {test_data['passed']}\n"
#                     f"**优先级统计**: \n"
#                     f" - @grade_1: {test_data['priority_stats']['grade_1']}\n"
#                     f" - @grade_2: {test_data['priority_stats']['grade_2']}\n"
#                     f" - @grade_3: {test_data['priority_stats']['grade_3']}\n"
#                     f" - @grade_4: {test_data['priority_stats']['grade_4']}\n"
#         }
#     }
#     try:
#         response = requests.post(webhook_url, json=message)
#         response.raise_for_status()
#         return response.status_code
#     except requests.RequestException as e:
#         logger.error(f"发送钉钉通知失败: {e}")
#         return 500
#
#
# # 发送邮件
# def send_email(report_dir):
#     # 邮件配置
#     sender = 'chq18870425154@163.com'
#     receivers = ['chenqiangt@cptgroup.cn']
#     smtp_server = 'smtp.163.com'
#     smtp_port = 465
#     username = 'chq18870425154@163.com'
#     password = 'SZgTA33Q25dzp9u7'  # 邮箱授权码
#
#     # 邮件标题
#     current_date = datetime.now().strftime("%Y-%m-%d")
#     subject = f"陈强的自动化测试报告{current_date}"
#
#     # 创建邮件对象
#     message = MIMEMultipart()
#     message['From'] = Header(sender, 'utf-8')
#     message['To'] = Header(", ".join(receivers), 'utf-8')
#     message['Subject'] = Header(subject, 'utf-8')
#
#     # 生成 Allure 报告链接
#     report_link = None
#     if report_dir:
#         start_port = 8000
#         max_port = 9000
#         server_port = None
#         for port in range(start_port, max_port):
#             try:
#                 # 检查端口是否可用
#                 with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                     s.bind(('0.0.0.0', port))
#                 logger.info(f"端口 {port} 可用，尝试启动服务器...")
#                 # 启动 Python 简易 HTTP 服务器
#                 if os.name == 'nt':  # Windows 系统
#                     subprocess.Popen(f'python -m http.server {port} --directory {report_dir}', shell=True)
#                 else:  # Linux 或 macOS 系统
#                     subprocess.Popen(f'python3 -m http.server {port} --directory {report_dir}', shell=True)
#                 server_port = port
#
#                 # 增加等待时间
#                 time.sleep(3)
#
#                 # 检查端口是否可连接
#                 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#                 s.connect(("8.8.8.8", 80))
#                 local_ip = s.getsockname()[0]
#                 s.close()
#                 with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as check_sock:
#                     result = check_sock.connect_ex((local_ip, server_port))
#                     if result == 0:
#                         logger.info(f"端口 {server_port} 可连接，生成报告链接...")
#                         report_link = f"http://{local_ip}:{server_port}"
#                         break
#                     else:
#                         logger.error(f"端口 {server_port} 无法连接，可能服务器启动失败，继续尝试下一个端口...")
#                         continue
#             except OSError:
#                 # logger.info(f"端口 {port} 已被占用或不可用，继续尝试下一个端口...")
#                 continue
#
#         if not report_link:
#             logger.error("未找到可用且可连接的端口")
#
#     if report_link:
#         body = f"测试 Allure 报告链接：{report_link}"
#     else:
#         body = "测试报告生成失败，无报告链接"
#
#     message.attach(MIMEText(body, 'plain', 'utf-8'))
#
#     smtp_obj = None
#     try:
#         # 连接 SMTP 服务器
#         smtp_obj = smtplib.SMTP_SSL(smtp_server, smtp_port)
#         smtp_obj.login(username, password)
#         # 发送邮件
#         smtp_obj.sendmail(sender, receivers, message.as_string())
#         logger.info("邮件发送成功")
#     except smtplib.SMTPException as e:
#         logger.error(f"邮件发送失败: {e}")
#     finally:
#         if smtp_obj:
#             try:
#                 smtp_obj.quit()
#             except smtplib.SMTPServerDisconnected:
#                 pass
#
#
# if __name__ == "__main__":
#     # 执行测试用例
#     test_result = run_tests()
#
#     # 生成测试报告
#     report_dir = generate_report()
#
#     if report_dir:
#         # 发送钉钉通知
#         ding_status = send_dingtalk(report_dir, test_result)
#         logger.info(f"钉钉发送状态码: {ding_status}")
#
#         # 发送邮件
#         send_email(report_dir)
#     else:
#         logger.warning("测试报告生成失败，跳过钉钉通知和邮件发送。")
