import pytest
import allure
from Business.mom_admin.production_modeling.factory_model import FactoryModel
from Toolbox.log_module import Logger
from Toolbox.random_container import random_characters
from markers import grade_1


@pytest.fixture(scope="class")
def factory_structure_fixture():
    factory_model = FactoryModel()
    workshop_code = random_characters()
    workshop_name = workshop_code
    production_line_code = random_characters()
    production_line_name = production_line_code
    # 新建车间
    response = factory_model.storeOrganizationStructureData(OrganizationStructureCode=workshop_code, OrganizationStructureName=workshop_name)
    workshop_id = None
    if response and response.status_code == 200:
        query_resp = factory_model.GetWorkshopAutoQueryDatas()
        if query_resp and query_resp.status_code == 200:
            query_body = query_resp.json()
            if query_body.get('Attach') and len(query_body['Attach']) > 0:
                workshop_id = query_body['Attach'][0]['Id']
    # 新建产线
    response_line = factory_model.storeOrganizationStructureData_productionline(OrganizationStructureCode2=production_line_code, OrganizationStructureName2=production_line_name)
    production_line_id = None
    if response_line and response_line.status_code == 200:
        query_line = factory_model.GetProductionLineAutoQueryDatas(OrganizationStructureCode=production_line_code)
        if query_line and query_line.status_code == 200:
            query_line_body = query_line.json()
            if query_line_body.get('Attach') and len(query_line_body['Attach']) > 0:
                production_line_id = query_line_body['Attach'][0]['Id']
    yield {
        "factory_model": factory_model,
        "workshop_code": workshop_code,
        "workshop_name": workshop_name,
        "workshop_id": workshop_id,
        "production_line_code": production_line_code,
        "production_line_name": production_line_name,
        "production_line_id": production_line_id
    }
    # 清理产线
    if production_line_id:
        factory_model.removeOrganizationStructureData_productionline(production_line_id)
    # 清理车间
    if workshop_id:
        factory_model.removeOrganizationStructureData(workshop_id, OrganizationStructureCode=workshop_code, OrganizationStructureName=workshop_name)

@allure.feature("工厂结构管理")
class TestFactoryStructure:
    # def test_01_add_workshop(self, factory_structure_fixture):
    #     assert factory_structure_fixture["workshop_id"] is not None

    # def test_02_query_workshop(self, factory_structure_fixture):
    #     response = factory_structure_fixture["factory_model"].GetWorkshopAutoQueryDatas()
    #     assert response is not None
    #     assert response.status_code == 200
    #     response_body = response.json()
    #     assert response_body['Success'] is True

    @grade_1
    def test_03_workshop_uniqueness(self, factory_structure_fixture):
        response = factory_structure_fixture["factory_model"].storeOrganizationStructureData(OrganizationStructureCode=factory_structure_fixture["workshop_code"], OrganizationStructureName=factory_structure_fixture["workshop_name"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    # def test_04_add_production_line(self, factory_structure_fixture):
    #     assert factory_structure_fixture["production_line_id"] is not None

    @grade_1
    def test_05_query_production_line(self, factory_structure_fixture):
        response = factory_structure_fixture["factory_model"].GetProductionLineAutoQueryDatas(OrganizationStructureCode=factory_structure_fixture["production_line_code"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert response_body['Success'] is True

    @grade_1
    def test_06_production_line_uniqueness(self, factory_structure_fixture):
        response = factory_structure_fixture["factory_model"].storeOrganizationStructureData_productionline(OrganizationStructureCode2=factory_structure_fixture["production_line_code"], OrganizationStructureName2=factory_structure_fixture["production_line_name"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    @grade_1
    def test_07_delete_production_line(self, factory_structure_fixture):
        response = factory_structure_fixture["factory_model"].removeOrganizationStructureData_productionline(factory_structure_fixture["production_line_id"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    @grade_1
    def test_08_delete_workshop(self, factory_structure_fixture):
        response = factory_structure_fixture["factory_model"].removeOrganizationStructureData(factory_structure_fixture["workshop_id"], OrganizationStructureCode=factory_structure_fixture["workshop_code"], OrganizationStructureName=factory_structure_fixture["workshop_name"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body 