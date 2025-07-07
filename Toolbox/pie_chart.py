import matplotlib.pyplot as plt

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建2x2子图画布
fig, axs = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle('缺陷统计信息全景图', fontsize=16)

# 1. 缺陷状态分布（左上）
status_labels = ['已关闭', '遗留']
status_sizes = [30, 2]
axs[0, 0].pie(status_sizes,
              labels=[f'{label}({size})' for label, size in zip(status_labels, status_sizes)],
              autopct='%1.1f%%',
              startangle=90,
              colors=['#66b3ff', '#ff9999'])
axs[0, 0].set_title('缺陷状态分布')

# 2. 缺陷类型分布（右上）
type_labels = ['逻辑缺陷', '页面缺陷', '需求缺陷']
type_sizes = [12,13,5]
axs[0, 1].pie(type_sizes,
              labels=[f'{label}\n({size})' for label, size in zip(type_labels, type_sizes)],
              autopct='%1.1f%%',
              colors=['#99ff99', '#ffcc99', '#ccccff'])
axs[0, 1].set_title('缺陷类型分布')

# 3. 优先级分布（左下）
priority_data = {
    '最高': {'count': 7, 'color': '#ff6666', 'percent': 23.3},
    '较高': {'count': 10, 'color': '#ff9966', 'percent': 33.3},
    '中等': {'count': 8, 'color': '#ffcc00', 'percent': 26.7},
    '较低': {'count': 5, 'color': '#99ff99', 'percent': 16.7},
    '最低': {'count': 0, 'color': '#ccccff', 'percent': 0}
}

# 绘制柱状图
axs[1, 0].bar(priority_data.keys(),
              [v['count'] for v in priority_data.values()],
              color=[v['color'] for v in priority_data.values()])

# 添加数值标签
for i, (k, v) in enumerate(priority_data.items()):
    axs[1, 0].text(i, v['count'] + 0.2,
                   f"{v['count']}({v['percent']:.1f}%)",
                   ha='center')
axs[1, 0].set_ylim(0, 11)  # 调整Y轴范围以更好显示标签
axs[1, 0].set_title('优先级分布')
axs[1, 0].set_ylabel('缺陷数量')

# 4. 处理人分布（右下）
owners_data = {
    '黄成祥': 10,
    '刘佳炜': 16,
    '共同处理': 4,
    '挂起':2
}
colors = ['#66b3ff', '#ffcc99', '#c2f0c2','#ffcc99']
axs[1, 1].bar(owners_data.keys(),
              owners_data.values(),
              color=colors)
for i, (k, v) in enumerate(owners_data.items()):
    axs[1, 1].text(i, v + 0.2, str(v), ha='center')
axs[1, 1].set_title('处理人分布')
axs[1, 1].set_ylabel('处理数量')

# 调整布局并保存
plt.tight_layout()
plt.savefig('defect_analysis.png', dpi=300, bbox_inches='tight')
plt.show()