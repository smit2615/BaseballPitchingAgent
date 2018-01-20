import unittest
from agents import SimpleReflexAgent, Environment


class MyTestCase(unittest.TestCase):
    def test_MapStateToSction_returns_number_in_proper_range(self):
        agent = SimpleReflexAgent()
        agent.state = [30, 'right']

        agent.mapStateToAction()

        self.assertIn(abs(agent.horizontalOffset), range(0, 19))

if __name__ == '__main__':
    unittest.main()