import csv


def read_csv(input_path, skip_lines=None):
    with open(input_path, 'r') as csvfile:
        reader = csv.reader(csvfile)

        if skip_lines is None:
            return [line for line in reader]

        for _ in range(skip_lines):
            next(reader)

        return [line for line in reader]


def group_by(ipt_lst: list, group_key: int) -> dict:
    """
    ipt_lst:
        input_list
    group_key:

    """
    result = {}

    for sub_lst in ipt_lst:
        if sub_lst[group_key] not in result:
            result[sub_lst[group_key]] = []

        result[sub_lst[group_key]].append(sub_lst)

    return result


def is_nested(lst: list):
    for item in lst:
        if isinstance(item, list):
            return True
    return False

