from cgi import test
import unittest
import read, copy
from logical_classes import *
from student_code import KnowledgeBase


class KBTest(unittest.TestCase):

    def setUp(self):
        # Assert starter facts
        file = 'statements_kb4.txt'
        self.data = read.read_tokenize(file)
        data = read.read_tokenize(file)
        self.KB = KnowledgeBase([], [])
        for item in data:
            if isinstance(item, Fact) or isinstance(item, Rule):
                self.KB.kb_assert(item)

    def test1(self):
            ask1 = read.parse_input("fact: (motherof ada ?X)")
            if unittest.main.verbosity > 1:
                print(' Asking if', ask1)
            answer = self.KB.kb_ask(ask1)
            print(answer)

if __name__ == '__main__':
    unittest.main()