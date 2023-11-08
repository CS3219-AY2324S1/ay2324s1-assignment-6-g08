from dotenv import load_dotenv
import os

load_dotenv()

AUTHORIZATION_TOKEN = os.getenv("TOKEN")

GRAPHQL_ENDPOINT = "https://leetcode.com/graphql"
GRAPHQL_QUERY = """
    query questionData($titleSlug: String!)
    {
        question(titleSlug: $titleSlug) 
        {
            title    
            titleSlug
            content
            isPaidOnly
            difficulty
            topicTags 
            {
                name
            }
            codeSnippets
            {
                lang
                langSlug
                code
            }
            hints
        }
    }

"""
QUESTIONS_ENDPOINT = "https://leetcode.com/api/problems/algorithms/"

POST_REQUEST_HEADER = {"Authorization": f"Bearer {AUTHORIZATION_TOKEN}"}
QUESTION_SERVICE_URI = os.getenv("QUESTION_SERVICE_URI")
