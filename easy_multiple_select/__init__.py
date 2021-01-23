def is_multiple_select(string: str, max_length: int) -> bool:
    """
    Checks if input string confirms to the rules of my multiple select input.
    You can read about what the the multiple select input is useful for in docstring of function do_multiple_select.
    :Rules:
    - An operant must be a integer bigger than -1 and the last operant, it must be smaller than max length
    - An operator is either an "," or an "-" and adjacent (<- in german: nebenstehende) of operators must be numbers
    - there can't be two "-" in a row (with a number in between of course) e.g: 2-5-7 is not allowed, 2-7 does the same

    """
    operators = (",", "-")

    # checks first operant and operator
    if len(string) < 3 or not string[0].isdecimal() or not 0 < int(string[0]) or string[1] not in operators:
        return False

    for index in range(2, len(string), 2):
        item = string[index]

        if not item.isdecimal() or not int(string[index - 2]) < int(item) < max_length:
            return False

    for index in range(3, len(string) - 1, 2):
        item = string[index]
        if item not in operators or "-" == item == string[index - 2]:
            return False

    return True


def is_multiple_select_1(string: str, max_length: int) -> bool:
    """
    Same but different, check which has better performance
    """
    operators = (",", "-")

    # checks first operant and operator
    if len(string) < 3 or not string[0].isdecimal() or not -1 < int(string[0]) or string[1] not in operators:
        return False

    for index in range(2, len(string) + 1, 2):
        item = string[index]

        # checks operands
        if index % 2 == 0:
            if not item.isdecimal() or not int(string[index - 2]) < int(item) <= max_length:
                return False

        # checks operators
        else:
            print(item, string[index - 2])
            if item not in operators or "-" == item == string[index - 2]:
                return False

    return True


def run_multiple_select(string: str) -> tuple:
    numbers = set()

    for index in range(1, len(string), 2):

        if string[index] == ',':
            numbers.add(int(string[index - 1]))
            numbers.add(int(string[index + 1]))

        else:
            for number in range(int(string[index - 1]), int(string[index + 2])):
                numbers.add(number)

    return tuple(numbers)


if __name__ == '__main__':

    nums = "2,4-6,8"

    max = 9

    if is_multiple_select("nums", max):
        print(run_multiple_select(nums))
