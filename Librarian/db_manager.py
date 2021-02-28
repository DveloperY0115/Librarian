import pymysql


class DatabaseManager:

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.host = host

        def init_connection():
            try:
                conn = pymysql.connect(db=self.db,
                                       user=self.user, passwd=passwd,
                                       host=self.host,
                                       charset='utf8', use_unicode=True)
                cursor = conn.cursor()
            except pymysql.Error as e:
                err_code, msg = e.args
                print("[{0}]: {1}".format(err_code, msg))
                raise SystemExit

            print("Connected to Database: {0}, hosted on: {1}, as user name: {2}".format(db, host, user))
            return conn, cursor

        self.conn, self.cursor = init_connection()

    def register_item(self, item, table, overwrite=True):

        if self.check_exists(item, {'url': item.get('url')}, table):
            # if the page of the same URL already exists in the table
            if overwrite:
                sql = "INSERT INTO " + table + " (title, url, content, last_updated) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(sql,
                                    (
                                        item.get("title"),
                                        item.get("url"),
                                        item.get("text"),
                                        item.get("last_updated")
                                    ))
                self.conn.commit()
            else:
                pass

    def check_exists(self, item, field_dict, table):
        return True

    def close_connection(self):
        try:
            self.cursor.close()
        except pymysql.Error as e:
            err_code, msg = e.args
            print("[{0}]: {1}".format(err_code, msg))
        try:
            self.conn.close()
        except pymysql.Error as e:
            err_code, msg = e.args
            print("[{0}]: {1}".format(err_code, msg))
        print("Successfully closed connection to Database: {0}, hosted on: {1}".format(self.db, self.host))
