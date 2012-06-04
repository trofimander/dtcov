import sys
from dtcov.dt_file_utils import DictContains

DEBUG_TRACE_LEVEL = 2

WARN_ONCE_MAP = {}

def debug(message):
    if DEBUG_TRACE_LEVEL>2:
        sys.stderr.write(message)

def warn(message):
    if DEBUG_TRACE_LEVEL>1:
        sys.stderr.write(message)

def info(message):
    sys.stderr.write(message)

def error(message):
    sys.stderr.write(message)

def error_once(message):
    if not DictContains(WARN_ONCE_MAP, message):
        WARN_ONCE_MAP[message] = True
        error(message)

