import re


def parse_input(str):
    dict = {}

    # regex to match input patterns
    pattern = r"(\w+)\s*=\s*(.*?)(?=\s*,\s*\w+\s*=\s*|\s*$)"
    str = str.replace("null", "None")
    matches = re.findall(pattern, str)

    for name, value in matches:
        try:
            value = float(value)
        except ValueError:
            if value.startswith("[") and value.endswith("]"):
                value = eval(value)

        dict[name] = value

    return dict


def parse_output(str):
    processed_str = str.replace("null", "None")
    value = None

    try:
        value = float(processed_str)
        return value
    except ValueError:
        if processed_str.startswith("[") and processed_str.endswith("]"):
            value = eval(processed_str)
            return value

    return processed_str


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
            inputs.append(parse_input(tc_input))
            tc_output = example[1].next_sibling.strip()
            outputs.append(parse_output(tc_output))
        except Exception:
            return [None, None]
    return [inputs, outputs]
