
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/project/cs373-idb/")

from serve import app as application
from serve import init
init("/nba")
application.secret_key = "\xae\xf36S}\xa9\x81\xc8\xa4`\xf0\\F\x19iJ\x19f\xf4\x92VV'\x91\xdf"
