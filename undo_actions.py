class NextPage:
    pass

class PrevousPage:
    pass

class Append:
    pass

class Insert:
    def __init__(self, line_number: int) -> None:
        self.line_number = line_number

class Remove:
    def __init__(self, line_number: int, string: str) -> None:
        self.line_number = line_number
        self.string = string

class Replace:
    def __init__(self, line_number: str, replaced_string: str) -> None:
        self.line_number = line_number
        self.replaced_string = replaced_string

class Swap:
    def __init__(self, line_number_1: str, line_number_2: str) -> None:
        self.line_number_1 = line_number_1
        self.line_number_2 = line_number_2

class FindAndReplace:
    def __init__(self, target: str, replacement: str) -> None:
        self.target = target
        self.replacement = replacement
