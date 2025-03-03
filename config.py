import os

DATABASE_URL = os.getenv("DATABASE_URL", "your_cloud_postgres_url_here")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
