import os

from dotenv import load_dotenv
from us_visa.constants import MONGODB_URL_KEY

load_dotenv()

print(os.getenv(MONGODB_URL_KEY))