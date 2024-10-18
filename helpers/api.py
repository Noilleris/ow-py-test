from requests import RequestException, get

from helpers.constants import CURRENT_PERIOD, REPORT

def current_period():
    try:
        response = get(CURRENT_PERIOD, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Error fetching current period: {e}")
        return None

def report(report_id: str):
    try:
        response = get(REPORT + report_id, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Error fetching report {report_id}: {e}")
        return None