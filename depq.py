# Adapted from https://github.com/KiranBaktha/Double-Ended-Priority-Queue

from dataclasses import dataclass, field
import itertools
import math
from typing import Any


@dataclass(order=True)
class PQItem:
    """Wrapper for priority queue items

    Items should only be compared based on their priority, not data.

    Attributes:
        priority (int):
            The priority of the item
        count (int):
            The unique index of the item
        data (Any):
            The associated data
    """
    priority: int
    count: int#Any=field(compare=False)
    data: Any=field(compare=False)
    def __init__(self, priority, count, data):
        self.priority = priority
        self.count = count
        self.data = data
    def unwrapped(self):
        """Return the underlying (priority, data) tuple"""
        return self.priority, self.count, self.data
    
    @classmethod
    def maximum(cls):
        return cls(math.inf, -1, None)
    
    @classmethod
    def minimum(cls):
        return cls(-math.inf, -1, None)


class DEPQ:
    def __init__(self, maxlen=None, mode='max'):
        self.pq = []  # List of entries arranged in a heap
        self.entry_finder = {}  # Mapping of item to entries
        self.counter = itertools.count()  # unique sequence count
        self.REMOVED = '<removed>'  # Placeholder for removed item
        self.n_items = 0  # Tracks the number of valid elements in the queue
        if maxlen is not None and not isinstance(maxlen, int):
            raise TypeError('expected maxlen to be of type int')
        self.maxlen = maxlen  # Maximum number of valid elements in the queue
        if mode not in ['max', 'min']:
            raise ValueError("mode must be either 'min' or 'max'")
        self.mode = mode  # Which elements to keep after maxlen is reached

    def push(self, item, priority=0):
        'Add a new item or update the priority of an existing item'
        if item in self.entry_finder:
            self.remove(item)
        if self.maxlen is not None and len(self) >= self.maxlen:
            if self.mode == 'max':
                if priority > self._peek_min().priority:
                    self.pop_min()
                else:
                    return  # priority not high enough; drop this item
            else:
                if priority < self._peek_max().priority:
                    self.pop_max()
                else:
                    return  # priority not low enough; drop this item
        count = next(self.counter)
        entry = PQItem(priority, count, item)
        self.entry_finder[item] = entry
        self._heappush(entry)
        self.n_items += 1

    def remove(self, item):
        'Mark an existing item as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(item)
        entry.data = self.REMOVED
        self.n_items -= 1

    def pop_min(self):
        'Remove and return the lowest priority item. Raise KeyError if empty.'
        entry = self._pop_min()
        self.n_items -= 1
        del self.entry_finder[entry.data]
        return entry.data

    def _pop_min(self):
        while self.pq:
            entry = self._heappop_min()
            if entry.data is not self.REMOVED:
                return entry
        raise KeyError('pop from an empty priority queue')

    def pop_max(self):
        'Remove and return the highest priority item. Raise KeyError if empty.'
        entry = self._pop_max()
        self.n_items -= 1
        del self.entry_finder[entry.data]
        return entry.data

    def _pop_max(self):
        while self.pq:
            entry = self._heappop_max()
            if entry.data is not self.REMOVED:
                return entry
        raise KeyError('pop from an empty priority queue')

    def peek_min(self):
        'Take a peek at the lowest priority item. Raise KeyError if empty.'
        return self._peek_min().data

    def _peek_min(self):
        if self.pq:
            min_entry = self._pop_min()
            self._heappush(min_entry)
            return min_entry
        raise KeyError('peek from an empty priority queue')

    def peek_max(self):
        'Take a peek at the highest priority item. Raise KeyError if empty.'
        return self._peek_max().data

    def _peek_max(self):
        if self.pq:
            max_entry = self._pop_max()
            self._heappush(max_entry)
            return max_entry
        raise KeyError('peek from an empty priority queue')

    def _heappush(self, value):
        'Pushes a given value into the heap'
        element_count = len(self.pq)+1
        level = math.floor(math.log2(element_count))  # Find level
        self.pq.append(value)
        if level % 2 == 0:
            self._heappush_minlevel(element_count-1)
        else:
            self._heappush_maxlevel(element_count-1)

    def _heappush_minlevel(self, index):
        'Heapifies a min-leveled element'
        parent = math.ceil(index/2)-1  # Parent index
        if parent >= 0:  # If parent exists
            if self.pq[parent] < self.pq[index]:
                self.pq[parent], self.pq[index] = self.pq[index], self.pq[parent]
                self._maxify_up(parent)
            else:
                self._minify_up(index)

    def _heappush_maxlevel(self, index):
        'Heapifies a max-leveled element'
        parent = math.ceil(index/2)-1
        if parent >= 0:
            if self.pq[parent] > self.pq[index]:
                self.pq[parent], self.pq[index] = self.pq[index], self.pq[parent]
                self._minify_up(parent)
            else:
                self._maxify_up(index)

    def _minify_up(self, index):
        'sift up for an element in the min level'
        parent = math.ceil(index/2)-1
        grand_parent = math.ceil(parent/2)-1  # Next min level is 2 levels up
        while grand_parent >= 0:
            if self.pq[grand_parent] > self.pq[index]:
                self.pq[grand_parent], self.pq[index] = self.pq[index], self.pq[grand_parent]
                parent = math.ceil(grand_parent/2)-1
                grand_parent = math.ceil(parent/2)-1
            else:
                break

    def _maxify_up(self, index):
        'sift up for an element in the max level'
        parent = math.ceil(index/2)-1
        grand_parent = math.ceil(parent/2)-1  # Next max level is 2 levels up
        while grand_parent >= 0:
            if self.pq[grand_parent] < self.pq[index]:
                self.pq[grand_parent], self.pq[index] = self.pq[index], self.pq[grand_parent]
                parent = math.ceil(grand_parent/2)-1
                grand_parent = math.ceil(parent/2)-1
            else:
                break

    def _heappop_min(self):
        'Pop the minimum priority node from the heap'
        self.pq[0], self.pq[len(self.pq)-1] = self.pq[len(self.pq)-1], self.pq[0]
        return_value = self.pq.pop()
        if len(self.pq):
            self._minify_down(0)
        return return_value

    def _minify_down(self, index):
        'sift down an element in the min level'
        left_index = 2*index+1
        right_index = 2*index+2
        if not len(self.pq) > 2*(left_index)+1:  # Last min level
            left_child = self.pq[left_index] if left_index < len(self.pq) else PQItem.maximum()
            right_child = self.pq[right_index] if right_index < len(self.pq) else PQItem.maximum()
            elements = (self.pq[index], left_child, right_child)
            min_index = elements.index(min(elements))
            if min_index != 0:
                self.pq[index], self.pq[min_index-1+left_index] = self.pq[min_index-1+left_index], self.pq[index]
        else:  # Next min level is 2 levels down
            gc = [2*left_index+1, 2*left_index+2, 2*right_index+1, 2*right_index+2]
            left_left_child = self.pq[gc[0]] if gc[0] < len(self.pq) else PQItem.maximum()
            left_right_child = self.pq[gc[1]] if gc[1] < len(self.pq) else PQItem.maximum()
            right_left_child = self.pq[gc[2]] if gc[2] < len(self.pq) else PQItem.maximum()
            right_right_child = self.pq[gc[3]] if gc[3] < len(self.pq) else PQItem.maximum()
            elements = (self.pq[index], left_left_child, left_right_child,
                        right_left_child, right_right_child)
            min_index = elements.index(min(elements))
            if min_index != 0:
                m = gc[min_index-1]
                self.pq[index], self.pq[m] = self.pq[m], self.pq[index]
                parent = m//2
                if self.pq[m] > self.pq[parent]:
                    self.pq[m], self.pq[parent] = self.pq[parent], self.pq[m]
                self._minify_down(m)

    def _heappop_max(self):
        'Pop the maximum priority node from the heap'
        if len(self.pq) == 1:
            return self.pq.pop()
        right = self.pq[2] if 2 < len(self.pq) else PQItem.minimum()
        elements = (PQItem.minimum(), self.pq[1], right)
        max_index = elements.index(max(elements))
        self.pq[max_index], self.pq[len(self.pq)-1] = self.pq[len(self.pq)-1], self.pq[max_index]
        return_value = self.pq.pop()
        if len(self.pq) > 1 and max_index < len(self.pq):
            self._maxify_down(max_index)
        return return_value

    def _maxify_down(self, index):
        'sift down an element in the max level'
        left_index = 2*index+1
        right_index = 2*index+2
        if not len(self.pq) > 2*(left_index)+1:  # Last max level
            left_child = self.pq[left_index] if left_index < len(self.pq) else PQItem.minimum()
            right_child = self.pq[right_index] if right_index < len(self.pq) else PQItem.minimum()
            elements = (self.pq[index], left_child, right_child)
            max_index = elements.index(max(elements))
            if max_index != 0:
                self.pq[index], self.pq[max_index-1+left_index] = self.pq[max_index-1+left_index], self.pq[index]
        else:  # Next max level is 2 levels down
            gc = [2*left_index+1, 2*left_index+2, 2*right_index+1, 2*right_index+2]
            left_left_child = self.pq[gc[0]] if gc[0] < len(self.pq) else PQItem.minimum()
            left_right_child = self.pq[gc[1]] if gc[1] < len(self.pq) else PQItem.minimum()
            right_left_child = self.pq[gc[2]] if gc[2] < len(self.pq) else PQItem.minimum()
            right_right_child = self.pq[gc[3]] if gc[3] < len(self.pq) else PQItem.minimum()
            elements = (self.pq[index], left_left_child, left_right_child,
                        right_left_child, right_right_child)
            max_index = elements.index(max(elements))
            if max_index != 0:
                m = gc[max_index-1]
                self.pq[index], self.pq[m] = self.pq[m], self.pq[index]
                parent = m//2
                if self.pq[m] < self.pq[parent]:
                    self.pq[m], self.pq[parent] = self.pq[parent], self.pq[m]
                self._maxify_down(m)

    def empty(self):
        return self.n_items == 0

    def __len__(self):
        return self.n_items
    
    def items(self):
        """Return the list of (priority, data) tuples in the queue"""
        return [item.unwrapped() for item in sorted(self.entry_finder.values())]

    

def test_basics():
    # Basic types
    queue = DEPQ()
    assert not queue
    queue.push('foo', 10)
    queue.push('bar', 9)
    queue.push('baz', 11)
    assert queue
    assert queue.peek_min() == 'bar'
    assert queue.peek_max() == 'baz'
    assert queue.pop_min() == 'bar'
    assert len(queue) == 2
    assert queue.pop_max() == 'baz'
    assert queue.peek_min() == queue.peek_max() == 'foo'
    del queue
    print('Test passed: basic types')

def test_maxlen():
    queue = DEPQ(maxlen=3, mode='max')
    queue.push('foo', 10)
    queue.push('bar', 7)
    queue.push('baz', 15)
    queue.push('fiz', 9)
    queue.push('buz', 12)
    assert queue.items() == [(10, 0, 'foo'), (12, 4, 'buz'), (15, 2, 'baz')]
    assert len(queue) == 3
    assert queue.pop_min() == 'foo'
    assert queue.pop_max() == 'baz'

    queue = DEPQ(maxlen=3, mode='min')
    queue.push('foo', 10)
    queue.push('bar', 7)
    queue.push('baz', 15)
    queue.push('fiz', 9)
    queue.push('buz', 12)
    assert queue.items() == [(7, 1, 'bar'), (9, 3, 'fiz'), (10, 0, 'foo')]
    assert len(queue) == 3
    assert queue.pop_min() == 'bar'
    assert queue.pop_max() == 'foo'
    print('Test passed: maxlen')

def test_same_priority():
    queue = DEPQ()
    for i in range(20):
        queue.push(i, priority=0)
    for i in range(20):
        item = queue.pop_min()
        assert item == i, '{} != {}'.format(item,i)

    queue = DEPQ()
    for i in range(20):
        queue.push(i, priority=0)
    for i in range(20):
        item = queue.pop_max()
        assert item == 19-i, '{} != {}'.format(item,19-i)

    print('Test passed: same priority')

def test():
    """Test priority queue functionality"""

    test_basics()
    test_maxlen()
    test_same_priority()

    print('All tests passed.')

if __name__ == '__main__':
    test()
