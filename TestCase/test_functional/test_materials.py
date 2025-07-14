import pytest
import allure
from Business.mom_admin.factory_modeling.product_materials import ProductMaterials, MaterialsBOM
from Toolbox.log_module import Logger
from Toolbox.random_container import random_characters
from markers import grade_1


@pytest.fixture(scope="class")
def material_fixture():
    product_materials = ProductMaterials()
    bom = MaterialsBOM()
    material_code = random_characters()
    material_name = material_code
    bom_version = random_characters()
    # 新建物料
    response = product_materials.storeMaterialInfoData(MaterialCode=material_code, MaterialName=material_name)
    material_id = None
    if response and response.status_code == 200:
        query_resp = product_materials.getMaterialInfoAutoQueryDatas(MaterialCode=material_code)
        if query_resp and query_resp.status_code == 200:
            query_body = query_resp.json()
            if query_body.get('Attach') and len(query_body['Attach']) > 0:
                material_id = query_body['Attach'][0]['Id']
    # 新建BOM
    response_bom = bom.storeManufactureBomData(bom_version, BOMCode=material_code)
    material_bom_id = None
    if response_bom and response_bom.status_code == 200:
        query_bom = bom.getGetBomMasterViewAutoQueryDatas(MaterialCode=material_code)
        if query_bom and query_bom.status_code == 200:
            query_bom_body = query_bom.json()
            if query_bom_body.get('Attach') and len(query_bom_body['Attach']) > 0:
                material_bom_id = query_bom_body['Attach'][0]['Id']
    yield {
        "product_materials": product_materials,
        "bom": bom,
        "material_code": material_code,
        "material_name": material_name,
        "material_id": material_id,
        "bom_version": bom_version,
        "material_bom_id": material_bom_id
    }
    # 清理BOM
    if material_bom_id:
        bom.removeManufactureBomData(bom_version, material_bom_id, BOMCode=material_code)
    # 清理物料
    if material_id:
        product_materials.removeMaterialInfoData(material_id, MaterialCode=material_code, MaterialName=material_name)

@allure.feature("物料与BOM管理")
class TestMaterials:
    @grade_1
    def test_01_add_material(self, material_fixture):
        assert material_fixture["material_id"] is not None

    @grade_1
    def test_02_query_material(self, material_fixture):
        response = material_fixture["product_materials"].getMaterialInfoAutoQueryDatas(MaterialCode=material_fixture["material_code"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert response_body['Success'] is True

    @grade_1
    def test_03_material_uniqueness(self, material_fixture):
        response = material_fixture["product_materials"].storeMaterialInfoData(MaterialCode=material_fixture["material_code"], MaterialName=material_fixture["material_name"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    # def test_04_add_bom(self, material_fixture):
    #     assert material_fixture["material_bom_id"] is not None

    @grade_1
    def test_05_query_bom(self, material_fixture):
        response = material_fixture["bom"].getGetBomMasterViewAutoQueryDatas(MaterialCode=material_fixture["material_code"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    @grade_1
    def test_06_bom_uniqueness(self, material_fixture):
        response = material_fixture["bom"].storeManufactureBomData(material_fixture["bom_version"], BOMCode=material_fixture["material_code"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    @grade_1
    @allure.title("删除物料BOM")
    def test_07_delete_bom(self, material_fixture):
        with allure.step("调用接口删除物料BOM"):
            response = material_fixture["bom"].removeManufactureBomData(material_fixture["bom_version"], material_fixture["material_bom_id"], BOMCode=material_fixture["material_code"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    @grade_1
    @allure.title("删除物料")
    def test_08_delete_material(self, material_fixture):
        with allure.step("调用接口删除物料"):
            response = material_fixture["product_materials"].removeMaterialInfoData(material_fixture["material_id"], MaterialCode=material_fixture["material_code"], MaterialName=material_fixture["material_name"])
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body 