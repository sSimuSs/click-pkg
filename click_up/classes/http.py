import json
from datetime import datetime

from requests import request


class Http:
    """
    A class for making HTTP requests.
    """
    def __init__(self, requests_logs_file_path=None):
        self.requests_logs_file_path = requests_logs_file_path
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def post(self, url, body, headers, timeout=10):
        """
        Send a POST request to the given URL with
        the provided body and headers.

        Args:
            url (str): The URL to send the request to.
            body (dict): The request body.
            headers (dict): The request headers.
            timeouts (dict, optional): The request timeouts. Defaults to None.

        Returns:
            dict: The response from the server.
        """
        headers = self.headers | headers
        data = json.dumps(body)
        result = request(
            method="POST", url=url,
            headers=headers, data=data, timeout=timeout
        )
        result.raise_for_status()

        f = open(self.requests_logs_file_path, "a")
        f.write(f"\n\n########################  {datetime.now()}\n")
        f.write("--- Request\n")
        f.write(f"{result.request.url}\n")
        f.write(f"{json.dumps(dict(result.request.headers), indent=4)}\n")
        f.write(f"{json.dumps(body, indent=4)}\n")
        try:
            f.write("--- Response\n")
            f.write(f"{json.dumps(result.json(), indent=4)}\n")
        except:
            pass
        f.close()

        return result.json()
