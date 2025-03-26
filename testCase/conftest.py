import pytest
import json

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