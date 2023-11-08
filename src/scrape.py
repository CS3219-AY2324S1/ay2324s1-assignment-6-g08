from bs4 import BeautifulSoup
import requests
from src.utility import extract_examples
from src.constants import GRAPHQL_ENDPOINT, GRAPHQL_QUERY, POST_REQUEST_HEADER, QUESTIONS_ENDPOINT, QUESTION_SERVICE_URI


def _fetch_title_slugs():
    for _ in range(5):
        try:
            response = requests.get(QUESTIONS_ENDPOINT)
            response.raise_for_status()

            data = response.json()["stat_status_pairs"]
            question_title_list = [
                q["stat"]["question__title_slug"] for q in data
                if not q["paid_only"]
            ]

            return question_title_list
        except requests.exceptions.Timeout:
            print("Timeout when getting all question titles. Retrying...")


def _get_question_data(title_slug):
    try:
        data_req = {
            "operationName": "questionData",
            "variables": {
                "titleSlug": title_slug
            },
            "query": GRAPHQL_QUERY,
        }
        data = requests.post(GRAPHQL_ENDPOINT, json=data_req).json()
        return data

    except requests.exceptions.Timeout:
        print(f"Timeout getting data of {title_slug}. Skipping...")


def fetch_questions():
    try:
        titles = _fetch_title_slugs()
        for slug in titles:
            q = _get_question_data(slug)["data"]["question"]
            if len(q["topicTags"]) == 0:
                continue

            # test cases
            soup = BeautifulSoup(q["content"], "html.parser")
            tc_in, tc_out = extract_examples(soup)

            if tc_in is None and tc_out is None:
                continue

            # code templates
            supported_slugs = ["javascript", "python", "ruby"]
            code_snippets = q["codeSnippets"]
            code_templates = {}

            for snippet in code_snippets:
                if snippet["langSlug"] in supported_slugs:
                    code_templates.update(
                        {snippet["langSlug"].capitalize(): snippet["code"]})
                if len(code_templates) == len(supported_slugs):
                    break

            question_data = {
                "title": q["title"],
                "categories": [tag["name"] for tag in q["topicTags"]],
                "complexity": q["difficulty"],
                "description": str(BeautifulSoup(q["content"], "html.parser")),
                "codeTemplates": code_templates,
                "inputs": tc_in,
                "outputs": tc_out,
            }

            requests.post(QUESTION_SERVICE_URI,
                          headers=POST_REQUEST_HEADER,
                          json=question_data)

            print(f"Done - {q['title']}")

    except requests.RequestException:
        print("Test")
