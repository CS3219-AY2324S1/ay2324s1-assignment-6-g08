import requests
from src.constants import (GRAPHQL_ENDPOINT, GRAPHQL_QUERY,
                           POST_REQUEST_HEADER, QUESTION_LIST_ENDPOINT,
                           QUESTION_SERVICE_URI)
from src.utility import extract_test_cases, get_code_templates


def _fetch_title_slugs():
    for _ in range(5):
        try:
            response = requests.get(QUESTION_LIST_ENDPOINT)
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
            tc_in, tc_out = extract_test_cases(q["content"])
            if tc_in is None and tc_out is None:
                continue

            question_data = {
                "title": q["title"],
                "categories": [tag["name"] for tag in q["topicTags"]],
                "complexity": q["difficulty"],
                "description": q["content"],
                "codeTemplates": get_code_templates(q["codeSnippets"]),
                "inputs": tc_in,
                "outputs": tc_out,
            }

            requests.post(QUESTION_SERVICE_URI,
                          headers=POST_REQUEST_HEADER,
                          json=question_data)

    except requests.RequestException as e:
        print(f"Error - {str(e)}")


def update_question_database(event, context):
    try:
        fetch_questions()
    except Exception as e:
        print(f"Error - {str(e)}")
