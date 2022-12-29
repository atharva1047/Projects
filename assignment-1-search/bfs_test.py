import unittest
import student_code as sc
import expand
import sys, signal

time_map1 = {
    'Campus': {'Campus': None, 'Whole_Food': 1, 'Beach': 1, 'Cinema': None, 'Lighthouse': 1, 'Ryan_Field': None, 'YWCA': None},
    'Whole_Food': {'Campus': 1, 'Whole_Food': None, 'Beach': 1, 'Cinema': 1, 'Lighthouse': None, 'Ryan_Field': None, 'YWCA': None},
    'Beach': {'Campus': 1, 'Whole_Food': 1, 'Beach': None, 'Cinema': None, 'Lighthouse': None, 'Ryan_Field': None, 'YWCA': None},
    'Cinema': {'Campus': None, 'Whole_Food': 1, 'Beach': None, 'Cinema': None, 'Lighthouse': None, 'Ryan_Field': None, 'YWCA': 1},
    'Lighthouse': {'Campus': 1, 'Whole_Food': None, 'Beach': None, 'Cinema': None, 'Lighthouse': None, 'Ryan_Field': 1, 'YWCA': None},
    'Ryan_Field': {'Campus': None, 'Whole_Food': None, 'Beach': None, 'Cinema': None, 'Lighthouse': 1, 'Ryan_Field': None, 'YWCA': 1},
    'YWCA': {'Campus': None, 'Whole_Food': None, 'Beach': None, 'Cinema': 1, 'Lighthouse': None, 'Ryan_Field': 1, 'YWCA': None}
}

def interrupt(a, b):
    sys.exit(1)

class UnitTests(unittest.TestCase):

    def test1(self):
        # signal.signal(signal.SIGALRM, interrupt)
        # expand.expand_count = 0
        # signal.alarm(5)
        path = sc.breadth_first_search(time_map1, 'Campus', 'Ryan_Field')
        self.assertEqual(path, ['Campus', 'Lighthouse', 'Ryan_Field'])

if __name__== "__main__": unittest.main()
