from django.test import TestCase
import os
from dotenv import load_dotenv

load_dotenv()

print(os.environ.get("DATABASE_URL"))
