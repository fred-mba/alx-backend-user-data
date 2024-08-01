#!/usr/bin/env python3
"""
Filter datum module
"""
import logging
import re
from typing import List


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

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

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
