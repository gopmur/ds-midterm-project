from typing import *

T = TypeVar("T")

class Dnode(Generic[T]):

    def __init__(self, value: T, next: Optional[Self], prev: Optional[Self]) -> None:
        self.value: T = value
        self.next: Optional[Self] = next
        self.prev: Optional[Self] = prev

    def __str__(self) -> str:
        return str(self.value)
        
class DLinkedList(Generic[T]):

    def __init__(self) -> None:
        self.first: Optional[Dnode[T]] = None
        self.last: Optional[Dnode[T]] = None
        self.size: int = 0
        self.current: Optional[Dnode[T]] = None
        self.current_index: int = 0

    def __iter__(self) -> Self:
        self.p = Dnode[T](None, self.first, None)
        return self

    def __next__(self) -> Dnode[T]:
        self.p = self.p.next
        if not self.p:
            raise StopIteration
        return self.p.value

    def __getitem__(self, index: int) -> T:

        if index < 0:
            index += self.size
        if index >= len(self) or index < 0:
            raise Exception("Index out of range")

        # start from first
        if index < self.size//2:
            p = self.first 
            for _ in range(index):
                p = p.next

        # start from last  
        else:
            p = self.last
            for _ in range(self.size - index - 1):
                p = p.prev 

        return p.value
    
    def __setitem__(self, index: int, value: T) -> None:
        
        if index < 0:
            index += self.size
        if index >= len(self) or index < 0:
            raise Exception("Index out of range")

        # start from first
        if index < self.size//2:
            p = self.first 
            for _ in range(index):
                p = p.next

        # start from last  
        else:
            p = self.last
            for _ in range(self.size - index - 1):
                p = p.prev 
        
        p.value = value
    
    def __len__(self) -> int:
        return self.size
    
    def __str__(self) -> str:

        if self.is_empty():
            return "[]"

        p = self.first
        string = "["
        if type(p.value) == str:
            string += "\"" + str(p) + "\""
        else:
            string += str(p)
        p = p.next
        while p:
            if type(p.value) == str:
                string += ", \"" + str(p) + "\""
            else:
                string += ", " + str(p)
            p = p.next
        string += "]"
        return string 

    def move(self, steps: int) -> None:

        if self.current_index + steps < 0 or self.current_index + steps >= self.size:
            raise Exception("Index out of range")

        if steps > 0:
            self.current_index += steps
            for _ in range(steps):
                self.current = self.current.next

        else:
            self.current_index -= steps
            for _ in range(-steps):
                self.current = self.current.prev

    def get_current(self) -> T:
        return self.current.value
                
    def reset_to_first(self) -> None:
        self.current = self.first
        self.current_index = 0

    def reset_to_last(self) -> None:
        self.current = self.last
        self.current_index = self.size - 1

    def is_empty(self) -> bool:
        return self.size == 0

    def push(self, value: T) -> None:
        self.add(value, len(self))

    def pop(self) -> T:
        return self.remove(len(self) - 1)        

    def add(self, value: T, index: int) -> None:

        if index < 0:
            index += self.size
        if index > len(self):
            raise Exception("Index out of range")

        if self.is_empty():
            self.first = Dnode[T](value, None, None)
            self.last = self.first
            self.current = self.first

        elif index == 0:
            self.first = Dnode[T](value, self.first, None)
            self.first.next.prev = self.first 
            self.current = self.current.prev

        elif index == self.size:
            self.last = Dnode[T](value, None, self.last)
            self.last.prev.next = self.last
        
        else:

            # start from first
            if index < self.size//2:
                p = self.first 
                for _ in range(index):
                    p = p.next

            # start from last  
            else:
                p = self.last
                for _ in range(self.size - index - 1):
                    p = p.prev 
            
            q = Dnode[T](value, p, p.prev)
            p.prev.next = q
            p.prev = q

            if index <= self.current_index:
                self.current = q

        self.size += 1
            
    def remove(self, index: int) -> T:

        if self.is_empty():
            raise Exception("Can't remove from an empty list")

        if index < 0:
            index += self.size
        if index >= len(self):
            raise Exception("Index out of range")

        if self.size == 1:
            p = self.first
            self.current = None
            self.first = None
            self.last = None

        elif index == 0:
            p = self.first
            if self.current_index == 0:
                self.current = self.current.next
            self.first = self.first.next
            self.first.prev = None

        elif index == self.size - 1:
            p = self.last
            if self.current_index == index:
                self.current = self.current.prev
            self.last = self.last.prev
            self.last.next = None

        else:

            # start from first
            if index < self.size//2:
                p = self.first 
                for _ in range(index):
                    p = p.next

            # start from last  
            else:
                p = self.last
                for _ in range(self.size - index - 1):
                    p = p.prev
            
            p.next.prev = p.prev
            p.prev.next = p.next

            if index <= self.current_index:
                self.current = self.current.next

        self.size -= 1
        return p.value

if __name__ == "__main__":
    l = DLinkedList[int]()
    l.push(0)
    l.remove(0)