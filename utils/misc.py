from utils.imports import *
from .db import db

prefix = db.get("core.main", "prefix", ".")
allowed = db.get("core.main", "allow")
print(db.get("core.main", "allowed"))
system = platform.system()
start_time = time.time()
meta_comments = re.compile(r"^ *# *meta +(\S+) *: *(.*?)\s*$", re.MULTILINE)
req_list = []
modules_help = {}