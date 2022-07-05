import logging
import secrets

from .base import *

logger = logging.getLogger(__package__)

DEBUG = True
SECRET_KEY = secrets.token_urlsafe()

try:
    from .local import *
except ImportError:
    logging.warning("No local settings found!")
