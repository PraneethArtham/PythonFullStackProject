import os
from supabase import create_client, Client  # pip install supabase
from dotenv import load_dotenv  # pip install python-dotenv
from datetime import datetime, timedelta

load_dotenv()

# Get environment variables
url = os.getenv("url")
key = os.getenv("key")

# Create Supabase client
sb: Client = create_client(url, key)