CompanyCode ="00000" #宁波瑞辉公司代码
# 工厂建模-产品物料
MaterialCode = "Automation01"  # 物料编码
MaterialName = "自动化测试物料01"  # 物料名称
materialCharacteristic = [{
		"label": "成品",
		"value": "IsProduct",
	}, {
		"label": "半成品",
		"value": "IsSemiFinishedProduct",
	}, {
		"label": "物料",
		"value": "IsMaterial"}] # 物料属性配置
BOMCode = "Automation01" # 物料BOM编码
MaterialName1 = "自动化测试物料BOM01"  # 物料BOM名称
BOMVersion = 520 # BOM版本号

# 工厂建模-工序相关
ProcessCode = "Automation01" # 工序编码
ProcessName = "自动化测试工序01"  #工序名称
ProcessRoutingCode2 = "Automation01"  + "-2" # 工艺路线编码,新建后会自动加序号
ProcessRoutingCode3 = "Automation01" + "-1"
ProcessRoutingCode = "Automation01"   # 工艺路线编码
ProcessRoutingName = "自动化测试工艺路线01" # 工艺路线名称
ProcessRoutingCode1 = "Automation01"  # 工艺路线编码,新建后会自动加序号
#设备管理
EquipmentCode = "Automation01" # 设备编码
EquipmentName = "自动化测试设备"  #设备名称

#工厂布局
OrganizationStructureCode =  "CHEJIAN" #车间编码
OrganizationStructureCode3 =  "CHEJIAN2" #车间编码2

OrganizationStructureName =  "自动化车间2" #车间名称
OrganizationStructureCode2 = "CHANXIANG" #产线编码
OrganizationStructureName2 = "自动化产线2" #产线名称
OrganizationStructureParentCode = "00000.00001.CHEJIAN" #车间编码（拼接后）

PlanQty = 100 # 计划数量