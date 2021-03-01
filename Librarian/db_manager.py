import pymysql
from pypika import Query, Table


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
        """
        Register data contained in Scrapy item to a table in the database bound to this instance.

        Args:
            item: Scrapy item instance
            table: A table to put data in
            overwrite: Whether to overwrite existing data or not, set to true by default

        Returns: Nothing
        """
        q = Query.into(table).columns('url', 'html').insert(
            item.get('url'), item.get('html')
        )
        if self.check_exists(table, item):
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

    def check_exists(self, table, item):
        """
        Checks whether the given  already exists in the table.

        Args:
            item: Scrapy item object to be examined
            table: A table on which the search will be performed

        Returns: True if the item satisfying condition exists, False otherwise.
        """
        table= Table(table)
        q = Query.from_(table).select(table.url).where(
                (table.url == item.get('url'))
        )
        self.cursor.execute(q.get_sql())
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
