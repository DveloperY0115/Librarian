import pymysql
from pypika import Query, Table, Field

class DatabaseManager:

    def __init__(self, db, user, passwd, host):
        """
        Constructor.

        Establishes connection to the database and binds the DB handle to an instance.

        Args:
            db: Name of database
            user: User-name used during connection
            passwd: Password required to gain access to database
            host: IP address of the server hosting database
        """
        self.db = db
        self.user = user
        self.host = host
        self.conn, self.cursor = self.init_connection(db, user, passwd, host)

    def register_item(self, item, table, overwrite=True):
        field_dict = {'url': '=' + '\'' + item.get('url') + '\''}
        q = Query.into(table).columns('title', 'url', 'content', 'last_updated').insert(
            item.get('title'), item.get('url'), item.get('text'), item.get('last_updated')
        )
        if self.check_exists(table, field_dict):
            # if the page of the same URL already exists in the table
            if overwrite:
                self.cursor.execute(q.get_sql())
                self.conn.commit()
            else:
                # Do nothing.
                pass
        else:
            self.cursor.execute(q.get_sql())
            self.conn.commit()

    def check_exists(self, table, field_dict):
        """
        Checks whether the row satisfying the given condition exists in the table.

        Args:
            field_dict: Python dictionary containing key-value pairs { (Field name, Constraint) ...}
            table: A table on which the search will be performed

        Returns: True if the item satisfying condition exists, False otherwise.
        """
        conditions = [str(field) + str(constraint) for (field, constraint) in field_dict.items()]
        conditions = ' AND '.join(conditions)
        query = 'SELECT * FROM ' + table + ' WHERE ' + conditions
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            # No match found, item doesn't exist
            return False
        return True

    def init_connection(self, db, user, passwd, host):
        """
        Initiates connection to the database

        Args:
            db: Name of database
            user: User-name used during connection
            passwd: Password required to gain access to database
            host: IP address of the server hosting database

        Returns: Database handles
        """
        try:
            conn = pymysql.connect(db=db,
                                   user=user, passwd=passwd,
                                   host=host,
                                   charset='utf8', use_unicode=True)
            cursor = conn.cursor()
        except pymysql.Error as e:
            err_code, msg = e.args
            print("[{0}]: {1}".format(err_code, msg))
            raise SystemExit

        print("Connected to Database: {0}, hosted on: {1}, as user name: {2}".format(db, host, user))
        return conn, cursor

    def close_connection(self):
        """
        Closes connection to the database

        Returns: Nothing
        """
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
