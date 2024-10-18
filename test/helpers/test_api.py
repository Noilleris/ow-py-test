import unittest
import requests_mock
from src.helpers.constants import CURRENT_PERIOD, REPORT
from src.helpers.api import current_period, report

class TestAPIRequests(unittest.TestCase):

    @requests_mock.Mocker()
    def test_current_period_success(self, m):
        m.get(CURRENT_PERIOD, json={"messages":[]})
        res = current_period()

        self.assertEqual(res, {"messages":[]})

    @requests_mock.Mocker()
    def test_current_period_404(self, m):
        m.get(CURRENT_PERIOD, status_code=404)
        res = current_period()

        self.assertIsNone(res)

    @requests_mock.Mocker()
    def test_current_period_500(self, m):
        m.get(CURRENT_PERIOD, status_code=500)
        res = current_period()

        self.assertIsNone(res)

    @requests_mock.Mocker()
    def test_report_404(self, m):
        m.get(REPORT + "SOME_ID", status_code=404)
        res = report("SOME_ID")

        self.assertIsNone(res)

    @requests_mock.Mocker()
    def test_report_success(self, m):
        m.get(REPORT + "SOME_ID", status_code=200, json={'id': 3952, 'name': 'Retail Lease Report', 'credit_cost': 52})
        res = report("SOME_ID")

        self.assertEqual(res, {'id': 3952, 'name': 'Retail Lease Report', 'credit_cost': 52})

if __name__ == '__main__':
    unittest.main()
