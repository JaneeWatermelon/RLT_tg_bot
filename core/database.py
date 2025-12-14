import contextlib
import os
import psycopg2
import psycopg2.extras as ps_extras


class Database:
    def __init__(self, **kwargs):
        super().__init__()
        self.connection_params = kwargs
        print(self.connection_params)

        SQL_ROOT = os.getenv("SQL_ROOT")

        queries_list = []
        # sql_files = ["clear.sql", "videos.sql", "video_snapshots.sql"]
        sql_files = ["videos.sql", "video_snapshots.sql"]

        for file in sql_files:
            with open(os.path.join(SQL_ROOT, file), "r", encoding="UTF-8") as f:
                queries_list.append((f.read(), None))

        self.execute_many(queries_list)
    
    @contextlib.contextmanager
    def get_connection(self):
        """
        Получение соединения к базе данных

        Пример:
            >>> with self.get_connection() as conn:
                    conn.execute(...)
        """
        conn = psycopg2.connect(**self.connection_params)
        
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute(self, query: str, params: list=None):
        """
        Отправка 1 запроса в базу данных.

        Аргументы:
            query (str): запрос (составлен BaseQueries, TableQueries или вручную)
            params (list): параметры для заполнения

        Возвращает:
            Cursor: курсор базы данных
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=ps_extras.RealDictCursor)
            cursor.execute(query, params or [])
            return cursor
        
    def execute_many(self, data: list):
        """
        Отправка нескольких запросов в базу данных.

        Аргументы:
            data (list): список кортежей вида:
                (query (str): запрос, params (list): параметры для заполнения)
        Возвращает:
            Cursor: курсор базы данных
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=ps_extras.RealDictCursor)
            for query, params in data:
                cursor.execute(query, params or [])
            return cursor
    
    def fetch_one(self, query, params=None):
        """
        Получение первой записи из выполненного запроса.

        Аргументы:
            query (str): запрос (составлен BaseQueries, TableQueries или вручную)
            params (list): параметры для заполнения
        Возвращает:
            RealDictRow: словарь (атрибут: значение) полученной записи
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=ps_extras.RealDictCursor)
            cursor.execute(query, params or [])
            return cursor.fetchone()
    
    def fetch_all(self, query, params=None):
        """
        Получение первой записи из выполненного запроса.

        Аргументы:
            query (str): запрос (составлен BaseQueries, TableQueries или вручную)
            params (list): параметры для заполнения
        Возвращает:
            list[RealDictRow]: список словарей (атрибут: значение) полученных записей
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=ps_extras.RealDictCursor)
            cursor.execute(query, params or [])
            return cursor.fetchall()
        
    def __str__(self):
        return f"Database(connection_params={self.connection_params})"

    def __repr__(self):
        return f"Database(connection_params={self.connection_params})"

    def to_dict(self):
        return {
            "connection_params": self.connection_params,
        }