import psycopg2
from Config import host, user, password, port, db_name


class MyDataBase:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(MyDataBase, cls).__new__(cls)
        return cls.__instance

    connection = None

    def __init__(self):
        try:
            self.connection = psycopg2.connect(host=host, user=user, password=password, port=port, database=db_name)
            self.connection.autocommit = True

            # create table
            with self.connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE users(
                id varchar(20) NOT NULL,
                msg_id varchar(20) NOT NULL);
                """)

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)

    def add_in_table(self, tg_id: int, msg_id: int) -> None:
        if self.get_msg_id_from_bd(tg_id) is None:
            tg_id, msg_id = str(tg_id), str(msg_id)
            with self.connection.cursor() as cursor:
                cursor.execute(f"""
                INSERT INTO users (id, msg_id) VALUES
                ('{tg_id}', '{msg_id}');""")
        else:
            with self.connection.cursor() as cursor:
                cursor.execute(f"""
                UPDATE users SET msg_id = '{str(msg_id)}' WHERE id = '{tg_id}';
                """)

    def get_msg_id_from_bd(self, tg_id: int):
        tg_id = str(tg_id)
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT msg_id FROM users WHERE id = '{tg_id}';
            """)

            return cursor.fetchone()

    def drop_row_with_id(self, tg_id: int) -> None:
        tg_id = str(tg_id)
        with self.connection.cursor() as cursor:
            cursor.execute(f"""
            DELETE FROM users WHERE id='{tg_id}'; 
            """)

    def drop_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            DROP TABLE users;
            """)

    def __del__(self):
        if self.connection is not None:
            self.connection.close()
