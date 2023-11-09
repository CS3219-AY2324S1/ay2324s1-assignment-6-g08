"""
Contains all the utility functions need by the scraper.
"""

import re
from bs4 import BeautifulSoup


def parse_input(input_str):
    """Parse test case inputs based on type

    Test case inputs come in the form {variable_name=value} where value can be
    of types string, integer or array. As eval is used, any None must be
    converted to null for python to be able to call eval.

    Parameters
    ----------
    input_str: str
        unprocessed string containing inputs extracted from the example
    """

    dict = {}

    pattern = r"(\w+)\s*=\s*(.*?)(?=\s*,\s*\w+\s*=\s*|\s*$)"
    input_str = input_str.replace("null", "None")
    matches = re.findall(pattern, input_str)

    for name, value in matches:
        try:
            value = float(value)
        except ValueError:
            if value.startswith("[") and value.endswith("]"):
                value = eval(value)

        dict[name] = value

    return dict


def parse_output(output_str):
    """Parse test case outputs based on type

    Test case outputs come in the form {variable_name=value} where value can be
    of types string, integer or array. As eval is used, any None must be
    converted to null for python to be able to call eval.

    Parameters
    ----------
    output_str: str
        an unprocessed string containing outputs extracted from the example
    """
    output_str = output_str.replace("null", "None")
    value = None

    try:
        value = float(output_str)
        return value
    except ValueError:
        if output_str.startswith("[") and output_str.endswith("]"):
            value = eval(output_str)
            return value

    return output_str


def get_code_templates(code_snippets):
    """
    Get supported code templates from given code snippets

    Parameters
    ----------
    code_snippets: dict
        given code snippets to extract relevant templates
    """

    supported_slugs = ["javascript", "python", "ruby"]
    code_templates = {}

    for snippet in code_snippets:
        if snippet["langSlug"] in supported_slugs:
            code_templates.update(
                {snippet["langSlug"].capitalize(): snippet["code"]})
        if len(code_templates) == len(supported_slugs):
            break

    return code_templates


def extract_test_cases(content):
    """Extracts test cases from the given examples in the question content

    The question bank (aka Leetcode) does not provide any sample test cases.
    However, Leetcode provides examples in the question content.

    Parameters
    ----------
    content: str
        content of the question
    """

    soup = BeautifulSoup(content, "html.parser")
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
            inputs.append(parse_input(tc_input))
            tc_output = example[1].next_sibling.strip()
            outputs.append(parse_output(tc_output))
        except Exception:
            return [None, None]

    return [inputs, outputs]
