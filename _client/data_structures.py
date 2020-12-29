import threading,time
class node:
    def __init__(self,x,next_node = None):
        self.x = x
        self.next = next_node


class queue:
    def __init__(self):
        self.first = None
        self.last = None
        self.not_empty = threading.Event()

    def __str__(self):
        if (self.first == None):
            return "->[]->"
        s = "->["
        temp = self.first

        while (temp != self.last):
            s += str(temp.x) + ", "
            temp = temp.next

        if (temp == self.last):
            s += str(temp.x) + "]->"
        
        return s

    def Head(self):
        if self.first == None:
            return ""
        return self.first.x
    def insert(self,x):
        temp = node(x)
        if self.last == None:
            self.first = temp
        else:
            self.last.next = temp
        self.last = temp
        self.not_empty.set()

    def wait_for_item(self):
        self.not_empty.wait()

    
    def is_empty(self):
        return not self.not_empty.is_set()

    def remove(self):
        if (self.first == None):
            return None
            
        x = self.first.x

        self.first = self.first.next

        if (self.first == None):
            self.last = None
            self.not_empty.clear()
        return x
