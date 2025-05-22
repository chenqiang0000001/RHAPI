# 项目URL
testUrl = "http://192.168.0.135:8282/"  # 测试环境url
formalUrl = "http://192.168.0.143:8282/"  # 正式环境url
urlLogin1 = "http://192.168.0.135:8288/"  # 登录url
url = testUrl
apiLogin = "account/login"  # MOM登录接口后缀

# MES系统
# 工厂建模
apiStoreMaterialInfoData = "MaterialInfoApi/StoreMaterialInfoData"  # 新增物料
apiGetMaterialInfoAutoQueryDatas = "MaterialInfoApi/GetMaterialInfoAutoQueryDatas"  # 查询物料
apiRemoveMaterialInfoData = "MaterialInfoApi/RemoveMaterialInfoData"  # 删除物料
apiStoreManufactureBomData = "ManufactureBomApi/StoreManufactureBomData"  # 新增物料BOM
apiGetBomMasterViewAutoQueryDatas = "ManufactureBomApi/GetBomMasterViewAutoQueryDatas"  # 查询物料BOM
apiRemoveManufactureBomData = "ManufactureBomApi/RemoveManufactureBomData"  # 删除物料BOM

apiStoreProcessInfoData = "ProductRouteApi/StoreProcessInfoData"  # 新增工序
apiRemoveProcessInfoData = "ProductRouteApi/RemoveProcessInfoData"  # 删除工序

apiStoreProcessRoutingData = "ProductRouteApi/StoreProcessRoutingData"  # 新增工艺路线
apiRemoveProcessRoutingData = "ProductRouteApi/RemoveProcessRoutingData"  # 删除工艺路线

apiAdjustProcessRoutingEntry = "ProductRouteApi/AdjustProcessRoutingEntry"  # 工艺路线绑定工序
apiStoreBatchProductProcessRouteDatas = "ProductRouteApi/StoreBatchProductProcessRouteDatas" # 产品绑定工艺路线
apiSelectManufactureBom = "ProductRouteApi/SelectManufactureBom"# 产品工序BOM绑定
apiStoreEquipmentLedgerData = "EquipmentLedgerApi/StoreEquipmentLedgerData"   # 新增设备台账
apiRemoveBatchEquipmentLedger = "EquipmentLedgerApi/RemoveBatchEquipmentLedgerDatas"   # 删除设备台账