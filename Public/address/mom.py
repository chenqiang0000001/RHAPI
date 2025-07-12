# 项目URL
testUrl = "http://192.168.0.135:8282/"  # 测试环境url
formalUrl = "http://192.168.0.143:8282/"  # 正式环境url
urlLogin1 = "http://192.168.0.135:8288/"  # 登录url
url = testUrl
# 新增PDA服务base url
pdaUrl = "http://192.168.0.135:8283/"  # PDA相关接口url（如标签扫描、拆分等）
apiLogin = "account/login"  # MOM登录接口后缀

# MES系统
# 工厂建模
apiStoreMaterialInfoData = "MaterialInfoApi/StoreMaterialInfoData"  # 新增物料
apiGetMaterialInfoAutoQueryDatas = "MaterialInfoApi/GetMaterialInfoAutoQueryDatas"  # 查询物料
apiRemoveMaterialInfoData = "MaterialInfoApi/RemoveMaterialInfoData"  # 删除物料
apiStoreManufactureBomData = "ManufactureBomApi/StoreManufactureBomData"  # 新增物料BOM
apiGetBomMasterViewAutoQueryDatas = "ManufactureBomApi/GetBomMasterViewAutoQueryDatas"  # 查询物料BOM
apiStoreBatchManufactureBomDetailDatas = "ManufactureBomApi/StoreBatchManufactureBomDetailDatas" # 新增物料BOM明细(绑定物料)
apiRemoveManufactureBomData = "ManufactureBomApi/RemoveManufactureBomData"  # 删除物料BOM

apiStoreProcessInfoData = "ProductRouteApi/StoreProcessInfoData"  # 新增工序
apiRemoveProcessInfoData = "ProductRouteApi/RemoveProcessInfoData"  # 删除工序
apiGetProcessInfoAutoQueryDatas = "ProductRouteApi/GetProcessInfoAutoQueryDatas" # 查询工序

apiUpLoadESopFileMaterialCollection = "ESopApi/UpLoadESopFileMaterialCollection"  # 上传物料ESOP文件
apiAuditESopMaterialDatas = "ESopApi/AuditESopMaterialDatas"  # 审核物料ESOP文件
apiUpLoadESopFileProcessCollection = "ESopApi/UpLoadESopFileMaterialProcessRoutingCollection"  # 上传工艺路线ESOP文件

apiStoreProcessRoutingData = "ProductRouteApi/StoreProcessRoutingData"  # 新增工艺路线
apiRemoveProcessRoutingData = "ProductRouteApi/RemoveProcessRoutingData"  # 删除工艺路线
apiGetProcessRoutingAutoQueryDatas = "ProductRouteApi/GetProcessRoutingAutoQueryDatas" # 查询工艺路线
apiGetProductProcessRouteAutoQueryDatas = "ProductRouteApi/GetProductProcessRouteAutoQueryDatas" # 查询产品工艺路线
apiRemoveBatchProductProcessRouteDatas = "ProductRouteApi/RemoveBatchProductProcessRouteDatas" # 删除产品工艺路线

apiStoreWorkShopInfoData = "WorkShopInfoApi/StoreWorkShopInfoData"  # 新增车间信息
apiStoreProductionLineData = "ProductionLineApi/StoreProductionLineData"  # 新增产线
apiRemoveWorkShopInfoData = "WorkShopInfoApi/RemoveWorkShopInfoData"  # 删除车间
apiRemoveProductionLineData = "ProductionLineApi/RemoveProductionLineData"  # 删除产线
apiGetAllProductionLineAutoQueryDatas = "ProductionLineApi/GetAllProductionLineAutoQueryDatas" # 查询产线
apiGetAllWorkShopInfoAutoQueryDatas = "WorkShopInfoApi/GetAllWorkShopInfoAutoQueryDatas" # 查询车间

apiAdjustProcessRoutingEntry = "ProductRouteApi/AdjustProcessRoutingEntry"  # 工艺路线绑定工序
apiStoreProductProcessRouteData = "ProductRouteApi/StoreProductProcessRouteData" # 工艺路线绑定产品
apiStoreBatchProductProcessRouteDatas = "ProductRouteApi/StoreBatchProductProcessRouteDatas" # 产品绑定工艺路线
apiSelectManufactureBom = "ProductRouteApi/SelectManufactureBom"# 产品工序BOM绑定

apiStoreEquipmentLedgerData = "EquipmentLedgerApi/StoreEquipmentLedgerData"   # 新增设备台账
apiGetEquipmentLedgerAutoQueryDatas = "EquipmentLedgerApi/GetEquipmentLedgerAutoQueryDatas" # 查询设备台账
apiRemoveBatchEquipmentLedger = "EquipmentLedgerApi/RemoveBatchEquipmentLedgerDatas"   # 删除设备台账

apiCreateProductInspectSchemaData = "IpqcProductInspectApi/CreateProductInspectSchemaData" # 新增产品检验方案
apiGetIpqcProductInspectSchemaDatas = "IpqcProductInspectApi/GetIpqcProductInspectSchemaDatas" # 查询产品检验方案
apiGetIpqcProductInspectOrderDatas = "IpqcProductInspectApi/GetIpqcProductInspectOrderDatas" # 查询产品检验单
apiStartInspectProcessInspectOrder = "IpqcProductInspectApi/StartInspectProcessInspectOrder" # 启动产品检验
apiSubmitProcessInspectOrderData = "IpqcProductInspectApi/SubmitProcessInspectOrderData" # 提交产品检验单

apiStoreProductionPlanOrderData = "ProductionPlanApi/StoreProductionPlanOrderData" # 新增生产计划单
apiGetProductionPlanOrderAutoQueryDatas = "ProductionPlanApi/GetProductionPlanOrderAutoQueryDatas" # 查询生产计划单
apiConfirmBatchProductionPlanOrderDatas = "ProductionPlanApi/ConfirmBatchProductionPlanOrderDatas" # 生产计划单确认
apiIssuedBatchProductionPlanOrderDatas = "ProductionPlanApi/IssuedBatchProductionPlanOrderDatas" # 生产计划单下达

apiCreateBatchProductionDispatchOrderData = "ProductionDispatchApi/CreateBatchProductionDispatchOrder" # 生产快捷派工
apiIssuedBatchProductionDispatchOrderDatas = "ProductionDispatchApi/IssuedBatchProductionDispatchOrderDatas" # 生产派工下达

#工控端
apiGetCanProductionDispatchOrderDatas = "SingleMachineExecuteApi/GetCanProductionDispatchOrderDatas"  #查询选择派工单
apiGetProductionDispatchOrderDataByCode = "SingleMachineExecuteApi/GetProductionDispatchOrderDataByCode"  #查询派工单详情

apiGetESopMaterialProcessRoutingAutoQueryDatas = "ESopApi/GetESopMaterialProcessRoutingAutoQueryDatas"  # 查看ESOP文件

apiStartProduction = "SingleMachineExecuteApi/StartProduction"   # 启动生产
apiScanFeedingMaterialLabelData = "IndustrialMaterialApi/ScanFeedingMaterialLabelData"  # 扫描投料物料标签
apiStoreFeedingMaterialLabelDatas = "IndustrialMaterialApi/StoreFeedingMaterialLabelDatas"  # 确认上料
apiProductionReport = "SingleMachineExecuteApi/ProductionReport"  # 生产报工
apiCreateFirstInspectOrder = "IpqcProductInspectApi/CreateFirstInspectOrder"  # 发起首检
apiCompletedProduction = "SingleMachineExecuteApi/CompletedProduction"  # 完成生产

apiStoreAndonCallHandleRulesData = "AndonCallHandleRulesApi/StoreAndonCallHandleRulesData"  # 新增andon规则
apiGetAndonCallHandleRulesAutoQueryDatas = "AndonCallHandleRulesApi/GetAndonCallHandleRulesAutoQueryDatas"  # 查询andon规则
apiRemoveBatchAndonCallHandleRulesDatas = "AndonCallHandleRulesApi/RemoveBatchAndonCallHandleRulesDatas"  # 删除andon规则
apiUpdateAndonCallCategoryParametersData = "AndonCallCategoryParametersApi/UpdateAndonCallCategoryParametersData" # 更新andon二级类别参数

apiStoreAndonCallDataRecordsData = "AndonCallDataRecordsApi/StoreAndonCallDataRecordsData" # 安灯呼叫
apiResponseAndonCallDataRecordsData = "AndonCallDataRecordsApi/ResponseAndonCallDataRecordsData" # 安灯签到
apiStartProcessAndonCallDataRecordsData = "AndonCallDataRecordsApi/StartProcessAndonCallDataRecordsData" # 安灯开始处理
apiEndProcessAndonCallDataRecordsData = "AndonCallDataRecordsApi/EndProcessAndonCallDataRecordsData" # 安灯结束处理
apiConfirmAndonCallDataRecordsData = "AndonCallDataRecordsApi/ConfirmAndonCallDataRecordsData" # 安灯确认