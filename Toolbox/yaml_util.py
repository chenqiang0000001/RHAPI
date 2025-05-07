import yaml
from pathlib import Path


def read_yaml(file_path: str) -> dict:
    """
    通用 YAML 读取方法
    :param file_path: YAML 文件路径（相对项目根目录）
    :return: YAML 解析后的字典数据
    """
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"YAML 文件 {file_path_obj} 不存在")
    with open(file_path_obj, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
