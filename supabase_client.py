import os
from dotenv import load_dotenv
from supabase import create_client, client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: client = create_client(url, key)
