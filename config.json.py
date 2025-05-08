config = {
    "test_case_format": {
        "execution_time": "# execution_time:",
        "priority": "# priority:"
    },
    "test_log_format": {
        "execution_time": "Execution Time:",
        "is_failed": "Test Failed:"
    },
    "pytest_command": "pytest D:\\apiAutomationRH\\TestCase --alluredir=./allure-results -v",
    "email_config": {
        "sender": "chq18870425154@163.com",
        "receivers": ["chenqiangt@cptgroup.cn"],
        "smtp_server": "smtp.163.com",
        "smtp_port": 465,
        "username": "chq18870425154@163.com",
        "password": "SZgTA33Q25dzp9u7"
    },
    "dingtalk_webhook": "YOUR_DINGTALK_WEBHOOK_URL"
}