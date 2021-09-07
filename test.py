import unittest
 
 
class LinkListNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node
 
 
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
 
    def get_at_index(self, index):
        if self.count_list() <= index:
            return None
        current = self.head  # set to the beginning
        count = 0  # starting counter
        while count < index:  # going down list
            current = current.next_node  # moving down list from node to node
            count += 1  # counter
        return current.value  # returning the value that was reached.
 
    def add_at_end(self, value):
        node_to_add = LinkListNode(value)  # creating a node thats not connected
        if self.head == None:
            self.head = (
                self.tail
            ) = node_to_add  # deciding where node goes (first = last) type thing
        else:
            self.tail.next_node = node_to_add  # adding to end of list
            self.tail = node_to_add  # setting it to be the tail
 
    def remove_index(self, index):
        prev = None
        current = self.head
        if(self.count_list() == 0 or index >= self.count_list()):
            return
        if(index == 0):
            self.head = self.head.next_node
            return
        count = 0
        while current is not None:
            if(count == index):
                if(self.count_list() == index - 1):
                    self.tail = prev
                    prev.next_node = None
                    return
                prev.next_node = current.next_node
                return
            count += 1
            prev = current
            current = current.next_node
            
        '''moving_var = self.head

        if moving_var is not index:        << moving var is a node index is a number so it would be if index not 0
            if moving_var.value == index:  << index is not value its number in the list
                self.head = moving_var.next_node <<this is good
                moving_var = None                << not needed
                return
        while moving_var is not None:            << good but needs a count to track index
            if moving_var.value == index:        << value is not index
                break                            << can just do the work and return instead of breaking
            prev = moving_var                    << good
            moving_var = moving_var.next_node    << good
        if moving_var == None:                   << can just return if code below is moved up
            return
        prev.next_node = moving_var.next_node    << move up to break
        moving_var = None                        << not needed '''

    def count_list(self):                    #count works great
        count = 0
        current = self.head
        while current != None:
            current = current.next_node
            count += 1
        return count
