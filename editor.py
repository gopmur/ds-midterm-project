from typing import *
from linked_list import *
import undo_actions
import redo_actions

class Editor:

    page_seprator = "$"

    def __init__(self) -> None:
        self.doc = DLinkedList[DLinkedList[str]]()
        self.undo_stack = DLinkedList[Any]()
        self.redo_stack = DLinkedList[Any]()

    def parse(self, address: str) -> None:
        self.undo_stack = DLinkedList[Any]()
        self.redo_stack = DLinkedList[Any]()
        self.doc = DLinkedList[DLinkedList[str]]()

        text = open(address).read()

        self.doc.push(DLinkedList[str]())
        self.doc[0].push("")
        
        i = 0
        while i < len(text):
            if text[i] == "\n":
                self.doc[-1].push("")
            elif text[i] == Editor.page_seprator:
                self.doc.push(DLinkedList[str]())
                self.doc[-1].push("")
                i += 1
            else:
                self.doc[-1][-1] += text[i]
            i += 1

    def save(self, address: str):
        file = open(address, "w")
        first_line = True
        first_page = True
        for page in self.doc:
            if first_page:
                first_page = False
            else:
                file.write(Editor.page_seprator)
            for line in page:
                if first_line:
                    first_line = False
                    file.write(line)    
                else:
                    file.write("\n" + line)

    def where(self) -> int:
        return self.doc.current_index
    
    def next_page(self) -> None:
        self.redo_stack = DLinkedList[Any]()
        self.undo_stack.push(undo_actions.NextPage())
        self.doc.move(1)

    def prevous_page(self) -> None:
        self.redo_stack = DLinkedList[Any]()
        self.undo_stack.push(undo_actions.PrevousPage())
        self.doc.move(-1)

    def lines(self) -> int:
        return self.doc.current.value.size
    
    def show(self, amogus: int) -> None:
        if amogus > self.doc.current.value.size:
            for i in range(self.doc.current.value.size):
                print(self.doc.current.value[i])
            return 
        for i in range(amogus):
            print(self.doc.current.value[i])

    def append(self, string: str) -> None:
        self.redo_stack = DLinkedList[Any]()
        self.undo_stack.push(undo_actions.Append())
        self.insert(string, self.doc.current.value.size)

    def insert(self, string: str, line_number: int) -> None:
        self.redo_stack = DLinkedList[Any]()
        self.undo_stack.push(undo_actions.Insert(line_number))
        line = ""
        for char in string:
            if char != "\n":
                line += char
            else:
                self.doc.current.value.add(line, line_number)
                line_number += 1
                line = ""
        self.doc.current.value.add(line, line_number)

    def remove(self, line_number: int) -> None:
        self.redo_stack = DLinkedList[Any]()
        self.undo_stack.push(undo_actions.Remove(
                line_number, 
                self.doc.current.value.remove(line_number))
        )

    def replace(self, line_number: int, string: str) -> None:
        self.redo_stack = DLinkedList[Any]()
        self.undo_stack.push(undo_actions.Replace(line_number, self.doc.current.value[line_number]))
        self.doc.current.value[line_number] = string

    def swap(self, line_number_1: int, line_number_2: int) -> None:
        self.redo_stack = DLinkedList[Any]()
        self.undo_stack.push(undo_actions.Swap(line_number_1, line_number_2))
        temp = self.doc.current.value[line_number_1]
        self.doc.current.value[line_number_1] = self.doc.current.value[line_number_2]
        self.doc.current.value[line_number_2] = temp

    def find(self, string: str) -> None:
        for (page_number, page) in enumerate(self.doc):
            for (line_number, line) in enumerate(page):
                if string in line:
                    print(f"Page: {page_number + 1}, Line: {line_number + 1}, {line}")

    def find_and_replace(self, target: str, replacement: str) -> None:
        self.redo_stack = DLinkedList[Any]()
        self.undo_stack.push(undo_actions.FindAndReplace(target, replacement))

        for page in self.doc:
            for line_index in range(len(page)):
                i = 0
                while i < len(page[line_index]):
                    
                    if page[line_index][i] == target[0]:

                        found = True
                        j = 1
                        while j + i < len(page[line_index]) and j < len(target):
                            if page[line_index][i + j] != target[j]:
                                found = False
                            j += 1

                        if found:
                            temp = page[line_index]
                            page[line_index] = temp[:i]
                            page[line_index] += replacement
                            page[line_index] += temp[i + j:]
                            i += len(replacement) - 1

                    i += 1 

    def undo(self) -> None:

        if self.undo_stack.is_empty():
            return
        
        action = self.undo_stack.pop()

        match action:

            case undo_actions.NextPage():
                self.prevous_page()
                self.redo_stack.push(redo_actions.NextPage)

            case undo_actions.PrevousPage():
                self.next_page()
                self.redo_stack.push(redo_actions.PrevousPage)

            case undo_actions.Append():
                self.redo_stack.push(redo_actions.Append(self.doc.current.value.pop()))

            case undo_actions.Insert():
                self.redo_stack.push(redo_actions.Insert(
                        action.line_number,
                        self.doc.current.value.remove(action.line_number) 
                    ))
            
            case undo_actions.Remove():
                self.redo_stack.push(redo_actions.Remove(action.line_number))
                self.insert(action.string, action.line_number)

            case undo_actions.Replace():
                self.redo_stack.push(redo_actions.Replace(action.line_number, action.replaced_string))
                self.replace(action.line_number, action.replaced_string)

            case undo_actions.Swap():
                self.redo_stack.push(redo_actions.Swap(action.line_number_1, action.line_number_2))
                self.swap(action.line_number_1, action.line_number_2)

            case undo_actions.FindAndReplace():
                self.redo_stack.push(redo_actions.FindAndReplace(action.target, action.replacement))
                self.find_and_replace(action.replacement, action.target)

    def redo(self) -> None:

        if self.redo_stack.is_empty():
            return

        action = self.redo_stack.pop()

        match action:

            case redo_actions.NextPage():
                self.next_page()

            case redo_actions.PrevousPage():
                self.prevous_page()

            case redo_actions.Append():
                self.append(action.string)

            case redo_actions.Insert():
                self.insert(action.string, action.line_number)

            case redo_actions.Remove():
                self.remove(action.line_number) 

            case redo_actions.Replace():
                self.replace(action.line_number, action.replacement)

            case redo_actions.Swap():
                self.swap(action.line_number_1, action.line_number_2)

            case redo_actions.FindAndReplace():
                self.find_and_replace(action.target, action.replacement)


if __name__ == "__main__":

    editor = Editor()
    editor.parse("text.txt")
    print(editor.doc)
    editor.save("target.txt")
    editor.parse("target.txt")
    print(editor.doc)
    
    editor.find_and_replace("target", "replacement")
    print(editor.doc)
    editor.undo()
    print(editor.doc)