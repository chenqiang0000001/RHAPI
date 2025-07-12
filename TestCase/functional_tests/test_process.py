import pytest
import allure
from Business.mom_admin.factory_modeling.production_process import ProcessRelated
from Toolbox.log_module import Logger
from Toolbox.random_container import random_characters
from markers import grade_1


@pytest.fixture(scope="class")
def process_fixture():
    process_related = ProcessRelated()
    process_code = random_characters()
    routing_code = random_characters()
    # 新建工序
    response = process_related.storeProcessInfoData(ProcessCode=process_code)
    process_id = None
    if response and response.status_code == 200:
        query_resp = process_related.GetProcessInfoAutoQueryDatas(ProcessCode=process_code)
        if query_resp and query_resp.status_code == 200:
            query_body = query_resp.json()
            if query_body.get('Attach') and len(query_body['Attach']) > 0:
                process_id = query_body['Attach'][0]['Id']
    # 新建工艺路线
    response_route = process_related.storeProcessRoutingData(ProcessRoutingName="测试工艺路线", ProcessRoutingBasisCode=routing_code)
    routing_id = None
    if response_route and response_route.status_code == 200:
        query_route = process_related.getProcessRoutingAutoQueryDatas(ProcessRoutingCode=routing_code)
        if query_route and query_route.status_code == 200:
            query_route_body = query_route.json()
            if query_route_body.get('Attach') and len(query_route_body['Attach']) > 0:
                routing_id = query_route_body['Attach'][0]['Id']
    yield {
        "process_related": process_related,
        "process_code": process_code,
        "process_id": process_id,
        "routing_code": routing_code,
        "routing_id": routing_id
    }
    # 清理工艺路线
    if routing_id:
        process_related.removeProcessRoutingData(routing_id)
    # 清理工序
    if process_id:
        process_related.removeProcessInfoData(process_id)

@allure.feature("工序与工艺路线管理")
class TestProcess:
    @grade_1
    def test_01_add_process(self, process_fixture):
        assert process_fixture["process_id"] is not None

    @grade_1
    def test_02_query_process(self, process_fixture):
        response = process_fixture["process_related"].GetProcessInfoAutoQueryDatas(ProcessCode=process_fixture["process_code"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert response_body['Success'] is True

    @grade_1
    def test_03_process_uniqueness(self, process_fixture):
        response = process_fixture["process_related"].storeProcessInfoData(ProcessCode=process_fixture["process_code"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    @grade_1
    def test_04_add_route(self, process_fixture):
        assert process_fixture["routing_id"] is not None

    @grade_1
    def test_05_query_route(self, process_fixture):
        response = process_fixture["process_related"].getProcessRoutingAutoQueryDatas(ProcessRoutingCode=process_fixture["routing_code"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    @grade_1
    def test_06_route_uniqueness(self, process_fixture):
        response = process_fixture["process_related"].storeProcessRoutingData(ProcessRoutingName="测试工艺路线", ProcessRoutingBasisCode=process_fixture["routing_code"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    @grade_1
    @allure.title("删除工艺路线")
    def test_07_delete_route(self, process_fixture):
        with allure.step("调用接口删除工艺路线"):
            response = process_fixture["process_related"].removeProcessRoutingData(process_fixture["routing_id"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    @grade_1
    @allure.title("删除工序")
    def test_08_delete_process(self, process_fixture):
        with allure.step("调用接口删除工序"):
            response = process_fixture["process_related"].removeProcessInfoData(process_fixture["process_id"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body 