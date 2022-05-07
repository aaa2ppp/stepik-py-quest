import base64
import os

print(base64.b64encode(os.urandom(32)))
