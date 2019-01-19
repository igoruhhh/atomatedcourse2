import json

import pymysql.cursors

from value_models.status import Status
from value_models.user import User


def _our_hash(password):
    return {
        "pass": "36525c3f7456ea8b6f228c67039a3ec128612bd40b9469042346664856cbbb8a",
        "test": "62fc22c0da68a727562013a405e45ad29fe67725db24870d8dff48a39b37f5ae",
        "secret": "94d1297b55907d7158b27cd91f0d0b0d212abc0ccd4a3e861b1f4e1f404c67e0"
    }[password]


class DbConnector:
    def __init__(self, config):
        # Connect to the database

        self.connection = pymysql.connect(**config, charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def create_user(self, user):
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = 'INSERT INTO `ow_base_user` (`username`,`email`, `joinIp`,`password`) VALUES ("{}", "{}", "{}", "{}")'
            cursor.execute(sql.format(user.username, user.email, "test@test.org", _our_hash(user.password), "21345215"))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        self.connection.commit()

    def get_users(self):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `ow_base_user`"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
        self.connection.commit()
        return [User(**u) for u in result]

    def delete_user(self, user):
        with self.connection.cursor() as cursor:
            sql = """DELETE FROM `ow_base_user` 
                     WHERE `ow_base_user`.`username` = %s"""
            cursor.execute(sql, (user.username,))
        self.connection.commit()

    def close(self):
        self.connection.close()

    def get_last_text_status(self):
        """ Get status with maximum id that is last added """
        with self.connection.cursor() as cursor:
            sql = """SELECT * FROM `ow_newsfeed_action` 
                     WHERE `id`= (SELECT MAX(`id`) FROM `ow_newsfeed_action`)
                     AND `entityType`="user-status"
                     """
            cursor.execute(sql)
            response = cursor.fetchone()
            data = json.loads(response["data"])
        self.connection.commit()
        return Status(text=data["status"])