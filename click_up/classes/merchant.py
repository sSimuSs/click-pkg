import time
import hashlib

from click_up.classes.http import Http


class MerchantApi:
    """
    A class for interacting with the CLICK Merchant API.
    """

    def __init__(self, service_id, merchant_user_id, secret_key, requests_logs_file_path=None):
        """
        Initialize the MerchantApi instance.
        :param service_id: Service ID provided by CLICK.
        :param merchant_user_id: Merchant User ID provided by CLICK.
        :param secret_key: Secret key for authentication.
        """
        self.http = Http(requests_logs_file_path)
        self.secret_key = secret_key
        self.service_id = int(service_id)
        self.merchant_user_id = merchant_user_id
        self.url = "https://api.click.uz/v2/merchant"

    def create_invoice(
        self,
        amount: float,
        phone_number: str,
        merchant_trans_id: str
    ) -> dict:
        """
        Create an invoice using the CLICK API.
        :param amount: Requested amount.
        :param phone_number: Invoice receiver.
        :param merchant_trans_id:
            Order ID (for online shopping) / personal account / login
            in the billing of the supplier.
        :returns dict: A dictionary containing the response from the API.
        """
        data = {
            "service_id": self.service_id,
            "amount": amount,
            "phone_number": phone_number,
            "merchant_trans_id": merchant_trans_id
        }

        url = f"{self.url}/invoice/create"
        return self._send_post_request(url, data)


    def submit_fiscal_check(
        self,
        payment_id: int,
        fiscal_check_url: str
    ) -> dict:
        """
        Sends already generated fiscal check data to CLICK for linking it to the invoice
        :param payment_id: payment ID from the CLICK side.
        :param fiscal_check_url: URL of the fiscal check from the ofd.uz.
        """

        data = {
            "service_id": self.service_id,
            "payment_id": payment_id,
            "qrcode": fiscal_check_url,
        }

        url = f"{self.url}/payment/ofd_data/submit_qrcode"
        return self._send_post_request(url, data)

    def reverse_invoice(self, payment_id: int):
        url = f"{self.url}/payment/reversal/{self.service_id}/{payment_id}"
        return self._send_delete_request(url)

    def _send_post_request(self, url: str, data: dict) -> dict:
        return self.http.post(url, data, self._get_request_headers(), 10)

    def _send_delete_request(self, url: str) -> dict:
        return self.http.delete(url, self._get_request_headers(), 10)

    def _get_request_headers(self) -> dict:
        timestamp = int(time.time())
        digest_input = f"{timestamp}{self.secret_key}"
        digest = hashlib.sha1(digest_input.encode()).hexdigest()
        headers = {
            "Auth": f"{self.merchant_user_id}:{digest}:{timestamp}",
        }
        return headers
