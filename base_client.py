import requests
from requests import Response

from src.config import BASE_URL, API_KEY


class BaseClient:
    """Shared HTTP client — mirrors the BasePage pattern from the UI framework.

    Every API client inherits from this class. It owns the requests.Session,
    default headers, base URL, and shared response helpers — so individual
    clients only define the endpoint-specific logic.
    """

    DEFAULT_TIMEOUT = 10

    def __init__(self):
        self.base_url = BASE_URL
        self.session  = requests.Session()
        self.session.headers.update({
            "Content-Type":  "application/json",
            "Accept":        "application/json",
            "api_key":       API_KEY,
        })

    # ------------------------------------------------------------------
    # HTTP verbs — thin wrappers that add base_url and timeout
    # ------------------------------------------------------------------

    def get(self, path: str, **kwargs) -> Response:
        return self.session.get(
            f"{self.base_url}{path}",
            timeout=self.DEFAULT_TIMEOUT,
            **kwargs
        )

    def post(self, path: str, **kwargs) -> Response:
        return self.session.post(
            f"{self.base_url}{path}",
            timeout=self.DEFAULT_TIMEOUT,
            **kwargs
        )

    def put(self, path: str, **kwargs) -> Response:
        return self.session.put(
            f"{self.base_url}{path}",
            timeout=self.DEFAULT_TIMEOUT,
            **kwargs
        )

    def delete(self, path: str, **kwargs) -> Response:
        return self.session.delete(
            f"{self.base_url}{path}",
            timeout=self.DEFAULT_TIMEOUT,
            **kwargs
        )

    # ------------------------------------------------------------------
    # Response helpers
    # ------------------------------------------------------------------

    def json(self, response: Response) -> dict | list:
        """Parse and return the response body as JSON.

        Raises ValueError with a clear message if the body is not valid JSON.
        """
        try:
            return response.json()
        except Exception:
            raise ValueError(
                f"Response body is not valid JSON.\n"
                f"Status: {response.status_code}\n"
                f"Body: {response.text[:500]}"
            )

    def is_success(self, response: Response) -> bool:
        """Return True if the response status is in the 2xx range."""
        return 200 <= response.status_code < 300
