from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(env_path)

import cloudinary
