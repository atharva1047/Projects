import unittest
import student_code as sc
import expand
import sys, signal

time_mapT = {
    'a': {'a': None, 'b': 1, 'c': 1, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None},
    'b': {'a': None, 'b': None, 'c': None, 'd': 1, 'e': 1, 'f': 1, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None},
    'c': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': 1, 'h': 1, 'i': None, 'j': None, 'k': None},
    'd': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None},
    'e': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None},
    'f': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': 1, 'j': 1, 'k': None},
    'g': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None},
    'h': {'a': None, 'b': None, 'c': None, 'd': None, 'e': 1, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': 1},
    'i': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None},
    'j': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None},
    'k': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None}
}

def interrupt(a, b):
    sys.exit(1)

class UnitTests(unittest.TestCase):

    def test3(self):
        # signal.signal(signal.SIGALRM, interrupt)
        # expand.expand_count = 0
        # signal.alarm(5)
        path = sc.depth_first_search(time_mapT, 'a', 'e')
        # Two correct answers for right-to-left or left-to-right child traversal respectively
        self.assertIn(path, [['a', 'c', 'h', 'e'], ['a', 'b', 'e']])


if __name__== "__main__": unittest.main()