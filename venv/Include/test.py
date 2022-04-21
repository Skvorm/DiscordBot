import os
from dotenv import load_dotenv
load_dotenv()
c=os.getenv('DB_HOST')
print(c)
