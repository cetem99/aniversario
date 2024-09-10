import mysql.connector


cnx = mysql.connector.connect(
    user="root",
    password="password",
    host="127.0.0.1",
    database="SchemaName",
)


def create(valor):
    cursor = cnx.cursor()
    query = (f"INSERT INTO TableName (ColumName) VALUES ('{valor}')")
    cursor.execute(query)
    cnx.commit()
    cursor.close()