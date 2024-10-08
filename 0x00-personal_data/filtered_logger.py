#!/usr/bin/env python3
"""
Filter datum module
"""
import os
import re
import logging
import mysql.connector
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str, message: str, separator: str) -> str:
    """
    Parameters
    ----------
    fields(List[str]): a list of strings representing all fields to obfuscate
    redaction(str): a string representing by what the field will be obfuscated
    message(str): a string representing the log line
    separator(str): a string representing by which character is separating all
    fields in the log line (message)
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        parameters
        ----------
        record(logging.LogRecord): Log record to format

        Return the formatted log record
        """
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION,
            original_message, self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """
    An implementation that takes no arguments and returns a
    logging.Logger object
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return connector to the db using credentials from thr env variables
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', '')
    conn = mysql.connector.connect(
        host=host,
        port=3306,
        user=username,
        password=password,
        database=db_name
    )
    return conn


def main() -> None:
    """Obtain a database connection using get_db and retrieve all rows in the
    users table and display each row under a filtered format.
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    column = fields.split(',')
    query = f"SELECT {fields} FROM users;"
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: f'{x[0]}={x[1]}',
                zip(columns, row)
            )
            message = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, message, None, None)
            log_record = logging.LogRecord(*args)
            info_logger = handle(log_record)


if __name__ == '__main__':
    main()
