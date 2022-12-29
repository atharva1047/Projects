import sys, json
import unittest
from urllib import parse, request

def get_problem_result(problem_file_name):
    with open('domain.pddl', 'r') as domain_file:
        with open(problem_file_name, 'r') as problem_file:
            data = {'domain': domain_file.read(), 'problem': problem_file.read()}
    response = {}
    while not response or response['result'] == 'Server busy...':
        try:
            response = json.loads(request.urlopen(request.Request('http://solver.planning.domains/solve', data=parse.urlencode(data).encode('utf-8'))).read())
        except:
            pass

    print(response['status'])
    if response['status'] != 'ok':
        if 'error' in response['result']:
            print(response['result']['error'])
    return response['status'], response['result']['output'].strip() if 'output' in response['result'] else None

class PlanningTest(unittest.TestCase):

    def test0(self):
        print('Solving Problem 0')
        result, status = get_problem_result('problem0.pddl')
        self.assertEqual(result, 'ok')

    def test1(self):
        print('Solving Problem 1')
        result, status = get_problem_result('problem1.pddl')
        self.assertEqual(result, 'ok')

if __name__ == '__main__':
    unittest.main()