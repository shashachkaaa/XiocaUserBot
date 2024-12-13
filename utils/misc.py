from utils.imports import *
from .db import db

prefix = db.get("core.main", "prefix", ".")
system = platform.system()
start_time = time.time()
META_COMMENTS = re.compile(r"^ *# *meta +(\S+) *: *(.*?)\s*$", re.MULTILINE)
req_list = []
modules_help = {}