import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
db_config = {
    'user': 'bakhtiyar',
    'password': 'BuX6nEpA',
    'host': '10.0.3.63',
    'database': 'data_for_arcgis_import',
    'raise_on_warnings': True
}


def connect_db():
    try:
        my_db = mysql.connector.connect(**db_config)
        return my_db
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        my_db.close()

