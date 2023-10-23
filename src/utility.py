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
