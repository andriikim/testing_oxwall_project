import json
import pymysql

from models import User


def _our_hash(password):
    d = {
        "pass": "bf6116af8e4b3e83a7646640590b9d5f5c95b06bf7eebf6c424487ff39293833",
        "test": "62fc22c0da68a727562013a405e45ad29fe67725db24870d8dff48a39b37f5ae",
        "secret": "94d1297b55907d7158b27cd91f0d0b0d212abc0ccd4a3e861b1f4e1f404c67e0"
    }
    return d[password]


class OxwallDB:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                             user='root',
                             password='mysql',
                             db='oxwa166',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def close(self):
        self.connection.close()

    def create_user(self, user):
        with self.connection.cursor() as cursor:
            # Create a new user
            sql = f"""INSERT `ow_base_user` (`username`, `email`, `password`, `joinIp`)
                      VALUES ("{user.username}", "{user.email}", "{_our_hash(user.password)}", "21423532")"""
            cursor.execute(sql)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        self.connection.commit()

    def delete_user(self, user):
        with self.connection.cursor() as cursor:
            sql = f'''DELETE FROM `ow_base_user`
                      WHERE `ow_base_user`.`username` = "{user.username}"'''
            cursor.execute(sql)
        self.connection.commit()

    def get_users(self):
        """
        :return: User objects with user data from DB
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `ow_base_user`"
            cursor.execute(sql)
            result = cursor.fetchall()
        self.connection.commit()
        return [User(**u) for u in result]  # TODO explain!

    def get_last_text_status(self):
        """ Get status with maximum id that is last added """
        with self.connection.cursor() as cursor:
            sql = """SELECT * FROM `ow_newsfeed_action`
                     WHERE `id`= (SELECT MAX(`id`) FROM `ow_newsfeed_action` WHERE `entityType`="user-status")
                     AND `entityType`="user-status"
                     """
            cursor.execute(sql)
            response = cursor.fetchone()
            data = json.loads(response["data"])["status"]
        self.connection.commit()
        return data
