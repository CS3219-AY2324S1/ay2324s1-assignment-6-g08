from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
import os
import requests
import utility

QUERY = "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"


def extract_examples(soup):
    if len(soup) == 0:
        return [None, None]

    # test cases usually in a <strong class="example"> tag
    examples = soup.find_all("strong", class_="example")

    inputs = []
    outputs = []
    for e in examples:
        try:
            pre = e.find_next("pre")
            example = pre.find_all("strong")
            tc_input = example[0].next_sibling.strip().replace("null", "None")
            inputs.append(utility.parse_input(tc_input))
            tc_output = example[1].next_sibling.strip()
            outputs.append(utility.parse_output(tc_output))
        except Exception as e:
            return [None, None]
    return [inputs, outputs]


def scrape():
    base_url = "https://leetcode.com/api/problems/algorithms/"
    header = {"Authorization": f"Bearer {os.environ['TOKEN']}"}
    site = os.environ["SITE"]

    try:
        response = requests.get(base_url)
        response.raise_for_status()

        question_list = response.json()["stat_status_pairs"]

        for question in question_list:
            # skip leetcode premium questions
            if question["paid_only"]:
                continue

            # post req to retrieve question data
            data_req = {
                "operationName": "questionData",
                "variables": {
                    "titleSlug": f"{question['stat']['question__title_slug']}"
                },
                "query": QUERY,
            }
            data = requests.post("https://leetcode.com/graphql", json=data_req).json()

            # data processing
            q = data["data"]["question"]
            if len(q["topicTags"]) == 0:
                continue

            # test cases
            soup = bs(q["content"], "html.parser")
            tc_in, tc_out = extract_examples(soup)

            if tc_in == None and tc_out == None:
                continue

            # code templates
            supported = ["Javascript", "Python", "Ruby"]
            code_snippets = q["codeSnippets"]
            code_templates = {}

            for snippet in code_snippets:
                if snippet["lang"] in supported:
                    code_templates.update({snippet["lang"]: snippet["code"]})
                if len(code_templates) == len(supported):
                    break

            question_data = {
                "title": q["title"],
                "categories": [tag["name"] for tag in q["topicTags"]],
                "complexity": q["difficulty"],
                "description": str(bs(q["content"], "html.parser")),
                "codeTemplates": code_templates,
                "inputs": tc_in,
                "outputs": tc_out,
            }

            # post
            post_res = requests.post(site, headers=header, json=question_data)
            print(f"{question_data['title']} - {post_res.content}")
            break

    except requests.RequestException as e:
        print(e)


load_dotenv()
scrape()
