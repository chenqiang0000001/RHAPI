import pytest
import json
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from Toolbox.random_container import random_characters
except ImportError as e:
    print(f"Warning: Could not import random_characters from Toolbox: {e}")
    # 提供一个简单的替代函数
    def random_characters():
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

test_data = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "priority_stats": {"grade_1": 0, "grade_2": 0, "grade_3": 0, "grade_4": 0}
}

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    # 仅在测试用例执行阶段（call）统计总数
    if rep.when == "call":
        test_data["total"] += 1
        for priority in ["grade_1", "grade_2", "grade_3", "grade_4"]:
            if item.get_closest_marker(priority):
                test_data["priority_stats"][priority] += 1
        if rep.outcome == "passed":
            test_data["passed"] += 1
        elif rep.outcome == "failed":
            test_data["failed"] += 1

# 测试结束后，将数据写入文件
def pytest_sessionfinish(session, exitstatus):
    with open("test_stats.json", "w", encoding="utf-8") as f:
        json.dump(test_data, f)

@pytest.fixture(scope="class")
def material_params():
    code = "AutoMat" + random_characters()
    name = "自动化物料" + random_characters()
    return {"MaterialCode": code, "MaterialName": name}

@pytest.fixture(scope="class")
def bom_params(material_params):
    version = random_characters()
    return {"BOMVersion": version, "MaterialCode": material_params["MaterialCode"]}

@pytest.fixture(scope="class")
def process_params():
    code = "AutoGX" + random_characters()
    name = "自动化工序" + random_characters()
    return {"ProcessCode": code, "ProcessName": name}

@pytest.fixture(scope="class")
def route_params():
    code = "AutoRoute" + random_characters()
    name = "自动化工艺路线" + random_characters()
    return {"ProcessRoutingCode": code, "ProcessRoutingName": name}

@pytest.fixture(scope="class")
def equipment_params():
    code = "AutoEQ" + random_characters()
    name = "自动化设备" + random_characters()
    return {"EquipmentCode": code, "EquipmentName": name}

@pytest.fixture(scope="class")
def workshop_params():
    code = "AutoWS" + random_characters()
    name = "自动化车间" + random_characters()
    return {"OrganizationStructureCode": code, "OrganizationStructureName": name}

@pytest.fixture(scope="class")
def production_line_params():
    code = "AutoPL" + random_characters()
    name = "自动化产线" + random_characters()
    return {"OrganizationStructureCode2": code, "OrganizationStructureName2": name}

@pytest.fixture(scope="class")
def plan_params(material_params, route_params, bom_params):
    return {
        "ProductCode": material_params["MaterialCode"],
        "ProductName": material_params["MaterialName"],
        "ProcessRoutingCode": route_params["ProcessRoutingCode"],
        "BOMCode": bom_params["MaterialCode"],
        "BOMVersion": bom_params["BOMVersion"]
    }