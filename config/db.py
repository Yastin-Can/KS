import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        try:
            self.connection = pymysql.connect(
                host='database-1.cfjebmevkzwv.us-east-1.rds.amazonaws.com',
                user='admin',
                password='A1s2d3f4g5h6',
                db=db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.connection = None

    def query_db(self, query, data=None):
        if self.connection is None:
            print("No hay conexión a la base de datos.")
            return False

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
        except Exception as e:
            print("Something went wrong:", e)
            return False

    def close(self):
        if self.connection:
            self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
