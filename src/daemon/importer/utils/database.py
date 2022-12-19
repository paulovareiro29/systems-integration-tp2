import psycopg2


class Database:
    def __init__(self, host="db-xml"):
        self.conn = None
        self.cursor = None
        self.user = "is"
        self.password = "is"
        self.host = host
        self.port = "5432"
        self.database = "is"

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(user=self.user,
                                             password=self.password,
                                             host=self.host,
                                             port=self.port,
                                             database=self.database)
            except psycopg2.DatabaseError as e:
                raise Exception("Error connecting to database")

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def insert(self, sql, values):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query=sql, vars=values)
                self.conn.commit()
                cursor.close()
                return True
        except psycopg2.Error as ex:
            raise ex

    def selectAll(self, query):
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query)

            for row in cursor:
                yield row

            cursor.close()

    def selectOne(self, query):
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result

    def softdelete(self, table, options):
        self.connect()
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"UPDATE {table} SET deleted_on = now() WHERE {options}")
            result = cursor.rowcount
            self.conn.commit()
            cursor.close()
            return result
