from dotenv import load_dotenv
from pathlib import Path  # python3 only
import elasticroute
import os

"""
env_path = Path('tests') / '.env'
load_dotenv(dotenv_path=env_path)

elasticroute.defaults.API_KEY = os.getenv("ELASTICROUTE_API_KEY")
elasticroute.defaults.BASE_URL = os.getenv("ELASTICROUTE_PATH")

print("Default API Key registered as: {}".format(elasticroute.defaults.API_KEY))
print("BASE URL registered as: {}".format(elasticroute.defaults.BASE_URL))
"""
