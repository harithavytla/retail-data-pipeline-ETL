import mysql.connector as mc
from mysql.connector import errorcode as ec


def get_connection(source_db):
    try:
        connection = mc.connect(user=source_db['DB_USER'],
                                password=source_db['DB_PASS'],
                                host=source_db['DB_HOST'],
                                db=source_db['DB_NAME']
                                )

    except mc.Error as error:
        if error.errno == ec.ER_ACCESS_DENIED_ERROR:
            print("Invalid Credentials")
        else:
            print(error)

    return connection
