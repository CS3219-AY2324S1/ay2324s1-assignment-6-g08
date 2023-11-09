import os
from dotenv import load_dotenv

load_dotenv()

# post request variables
AUTHORIZATION_TOKEN = os.getenv("TOKEN")
POST_REQUEST_HEADER = {"Authorization": f"Bearer {AUTHORIZATION_TOKEN}"}
QUESTION_SERVICE_URI = os.getenv("QUESTION_SERVICE_URI")

# graphql variables
GRAPHQL_ENDPOINT = os.getenv("GRAPHQL_ENDPOINT")
GRAPHQL_QUERY = os.getenv("GRAPHQL_QUERY")
QUESTION_LIST_ENDPOINT = os.getenv("QUESTION_LIST_ENDPOINT")
