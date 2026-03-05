import os
from dotenv import load_dotenv

# 1. Get the directory of the current file (core/)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to the root directory (ai-coding-agent/)
root_dir = os.path.dirname(current_dir)

# 3. Build the exact path to .env
env_path = os.path.join(root_dir, '.env')

# 4. Force load from that exact path
load_dotenv(dotenv_path=env_path)

class Settings:
    def __init__(self):
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

        if not self.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in .env file")

settings = Settings()