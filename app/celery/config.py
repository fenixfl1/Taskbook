from __future__ import unicode_literals, absolute_import
import os
import time
import time
from tzlocal import get_localzone
  
local_tz = get_localzone() 
broker_url = 'redis://localhost:6379'
result_backend = 'db+mysql://root:3306/Taskbook'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
include=['tasks.send_mail']
timezone = local_tz
enable_utc = True
result_expires=3600