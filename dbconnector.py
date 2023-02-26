import psycopg2
from configparser import ConfigParser


class Connector:
    def __init__(self, username='', password='', verifier=False):
        self.__registrationSuccessful = None
        self.__cur = None
        self.__params = None
        self.__conn = None
        self.__result = None
        self.__reachability = None

        if (username == '' and password == '' and verifier is False) or (username != '' and password != '' and verifier is True):
            raise ValueError('Incorrect arguments')

        if not verifier:
            self.__username = username
            self.__password = password

        elif self.__verify():
            self.__reachability = True
        else:
            self.__reachability = False

    def __config(self, filename='database.ini', section='postgresql'):
        # Creates a parser
        self.__parser = ConfigParser()

        # Reads config file
        self.__parser.read(filename)

        # Get section, default to postgresql
        self.__db = {}
        if self.__parser.has_section(section):
            self.__params = self.__parser.items(section)
            for param in self.__params:
                self.__db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return self.__db

    def connect(self):
        """Connects to the PostgreSQL database server"""
        self.__conn = None
        try:
            # Reads connection parameters
            self.__params = self.__config()

            # Connects to the PostgreSQL server
            self.__conn = psycopg2.connect(**self.__params)

            # Creates a cursor
            self.__cur = self.__conn.cursor()

            # Executes a statement
            self.__cur.execute(f'SELECT username FROM users WHERE username = \'{self.__username}\' AND password = crypt(\'{self.__password}\', password)')

            self.__result = self.__cur.fetchone()

            # Closes the communication with the PostgreSQL
            self.__cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.__conn is not None:
                self.__conn.close()
                # Displays the query result
                if not self.__result:
                    return False
                else:
                    return True

    def register(self):
        """Registers a user to the PostgreSQL database server"""
        self.__conn = None
        self.__registrationSuccessful = False
        try:
            # Reads connection parameters
            self.__params = self.__config()

            # Connects to the PostgreSQL server
            self.__conn = psycopg2.connect(**self.__params)

            # Creates a cursor
            self.__cur = self.__conn.cursor()

            # Registers the user
            print(self.__username)
            print(self.__password)
            self.__cur.execute(f'INSERT INTO users (username, password) VALUES (%s, crypt(%s, gen_salt(\'bf\')))', (self.__username, self.__password))

            self.__conn.commit()
            self.__registrationSuccessful = True

            # Closes the communication with the PostgreSQL
            self.__cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.__conn is not None:
                self.__conn.close()
                # Displays the query result
                if not self.__registrationSuccessful:
                    return False
                else:
                    return True

    def __verify(self):
        """Verifies the reachability of the PostgreSQL database server"""
        self.__conn = None
        try:
            # Reads connection parameters
            self.__params = self.__config()

            self.__conn = psycopg2.connect(**self.__params)

            if self.__conn is not None:
                self.__conn.close()
                return True
            else:
                return False

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False

    @property
    def isDatabaseReachable(self):
        if self.__reachability is None:
            self.__verify()

        return self.__reachability
