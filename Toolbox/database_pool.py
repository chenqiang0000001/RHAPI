import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from Toolbox.config_manager import config_manager
from Toolbox.log_module import Logger


class DatabasePool:
    """数据库连接池管理器"""
    
    def __init__(self, pool_size: int = 5):
        self.pool_size = pool_size
        self.logger = Logger(name="database_pool").get_logger()
        self.config = config_manager.get_database_config()
        self._connections = []
        self._init_pool()
    
    def _init_pool(self):
        """初始化连接池"""
        try:
            for _ in range(self.pool_size):
                conn = pymysql.connect(
                    host=self.config['host'],
                    user=self.config['user'],
                    password=self.config['password'],
                    database=self.config['database'],
                    charset=self.config['charset'],
                    cursorclass=DictCursor,
                    autocommit=False
                )
                self._connections.append(conn)
            self.logger.info(f"数据库连接池初始化成功，连接数: {self.pool_size}")
        except Exception as e:
            self.logger.error(f"数据库连接池初始化失败: {e}")
            raise
    
    def _get_connection(self) -> pymysql.Connection:
        """获取数据库连接"""
        if not self._connections:
            self.logger.warning("连接池为空，创建新连接")
            return pymysql.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset=self.config['charset'],
                cursorclass=DictCursor,
                autocommit=False
            )
        return self._connections.pop()
    
    def _return_connection(self, conn: pymysql.Connection):
        """归还数据库连接"""
        try:
            if conn.open:
                self._connections.append(conn)
        except Exception as e:
            self.logger.error(f"归还连接失败: {e}")
            self._close_connection(conn)
    
    def _close_connection(self, conn: pymysql.Connection):
        """关闭数据库连接"""
        try:
            if conn.open:
                conn.close()
        except Exception as e:
            self.logger.error(f"关闭连接失败: {e}")
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = None
        try:
            conn = self._get_connection()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            if conn:
                self._return_connection(conn)
    
    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """执行查询语句"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
    
    def execute_update(self, sql: str, params: Optional[tuple] = None) -> int:
        """执行更新语句"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, params)
                conn.commit()
                return affected_rows
    
    def execute_many(self, sql: str, params_list: List[tuple]) -> int:
        """批量执行语句"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                affected_rows = cursor.executemany(sql, params_list)
                conn.commit()
                return affected_rows
    
    def close_pool(self):
        """关闭连接池"""
        for conn in self._connections:
            self._close_connection(conn)
        self._connections.clear()
        self.logger.info("数据库连接池已关闭")


# 全局数据库连接池实例
db_pool = DatabasePool() 