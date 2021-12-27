import logging

from .base import *

logger = logging.getLogger(__package__)

DEBUG = True

try:
    from .local import *
except ImportError:
    logging.warning("No local settings found!")
