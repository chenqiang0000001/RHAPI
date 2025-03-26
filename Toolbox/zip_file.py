import os
import zipfile

from Toolbox.log_module import Logger

logger = Logger(name="my_logger").get_logger()  # 实例化 Logger 类，获取日志记录器


def zip_files(source_dir, output_zip):
    """
    将指定目录下的文件压缩成 ZIP 文件

    :param source_dir: 要压缩的源目录
    :param output_zip: 输出的 ZIP 文件路径
    """
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file) # 获取相对路径，避免将完整路径结构加入 ZIP
                    relative_path = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, relative_path)
        logger.info(f"成功将 {source_dir} 压缩到 {output_zip}")
    except Exception as e:
        logger.error(f"压缩过程出现错误，错误信息：{e}")  # 错误日志记录
