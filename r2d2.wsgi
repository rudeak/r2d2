import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/r2d2/")
from r2d2 import app as application
#application.secret_key = ''
