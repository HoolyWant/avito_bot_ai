import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
dot_env = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dot_env)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

KEYS = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}



# HEADERS = {
#     'Authorization': 'Bearer ' + CLIENT_SECRET
# }