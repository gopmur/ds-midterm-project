class NextPage:
    pass

class PrevousPage:
    pass

class Append:
    def __init__(self, string: str) -> None:
        self.string = string
    
class Insert:
    def __init__(self, line_number: int, string: str) -> None:
        self.line_number = line_number
        self.string = string

class Remove:
    def __init__(self, line_number):
        self.line_number = line_number

class Replace:
    def __init__(self, line_number: str, replacement: str) -> None:
        self.line_number = line_number
        self.replacement = replacement

class Swap:
    def __init__(self, line_number_1: str, line_number_2: str) -> None:
        self.line_number_1 = line_number_1
        self.line_number_2 = line_number_2

class FindAndReplace:
    def __init__(self, target: str, replacement: str):
        self.target = target 
        self.replacement = replacement