import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class SolveResult:
    text: str
    task_id: str
    latency_ms: int
    status: str


@dataclass
class ExtractResult:
    data: dict
    task_id: str
    latency_ms: int
    status: str


class OcilarError(Exception):
    def __init__(self, status: int, detail: str):
        self.status = status
        self.detail = detail
        super().__init__(f"Ocilar API error {status}: {detail}")


class OcilarClient:
    """Ocilar API client for CAPTCHA solving and document extraction."""

    def __init__(self, api_key: str, base_url: str = "https://api.ocilar.com/api/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({
            "X-API-Key": api_key,
            "Content-Type": "application/json",
        })

    def _post(self, path: str, payload: dict) -> dict:
        url = f"{self.base_url}{path}"
        resp = self._session.post(url, json=payload)
        data = resp.json()
        if not resp.ok:
            raise OcilarError(resp.status_code, data.get("detail", resp.text))
        return data

    # ── CAPTCHA Solving ──

    def solve_sat(self, image_base64: str) -> SolveResult:
        """Solve a SAT Mexico CAPTCHA."""
        data = self._post("/solve/sat", {"image": image_base64})
        return SolveResult(
            text=data.get("text", ""),
            task_id=data.get("task_id", ""),
            latency_ms=data.get("latency_ms", 0),
            status=data.get("status", ""),
        )

    def solve_imss(self, image_base64: str) -> SolveResult:
        """Solve an IMSS Mexico CAPTCHA."""
        data = self._post("/solve/imss", {"image": image_base64})
        return SolveResult(
            text=data.get("text", ""),
            task_id=data.get("task_id", ""),
            latency_ms=data.get("latency_ms", 0),
            status=data.get("status", ""),
        )

    def solve_image(self, image_base64: str) -> SolveResult:
        """Solve a generic image CAPTCHA."""
        data = self._post("/solve/image", {"image": image_base64})
        return SolveResult(
            text=data.get("text", ""),
            task_id=data.get("task_id", ""),
            latency_ms=data.get("latency_ms", 0),
            status=data.get("status", ""),
        )

    def solve_recaptcha_v2(self, site_key: str, site_url: str) -> SolveResult:
        """Solve a reCAPTCHA v2 challenge."""
        data = self._post("/solve/recaptcha-v2", {"site_key": site_key, "site_url": site_url})
        return SolveResult(
            text=data.get("token", data.get("text", "")),
            task_id=data.get("task_id", ""),
            latency_ms=data.get("latency_ms", 0),
            status=data.get("status", ""),
        )

    def solve_recaptcha_v3(self, site_key: str, site_url: str, action: str = "verify") -> SolveResult:
        """Solve a reCAPTCHA v3 challenge."""
        data = self._post("/solve/recaptcha-v3", {"site_key": site_key, "site_url": site_url, "action": action})
        return SolveResult(
            text=data.get("token", data.get("text", "")),
            task_id=data.get("task_id", ""),
            latency_ms=data.get("latency_ms", 0),
            status=data.get("status", ""),
        )

    def solve_hcaptcha(self, site_key: str, site_url: str) -> SolveResult:
        """Solve an hCaptcha challenge."""
        data = self._post("/solve/hcaptcha", {"site_key": site_key, "site_url": site_url})
        return SolveResult(
            text=data.get("token", data.get("text", "")),
            task_id=data.get("task_id", ""),
            latency_ms=data.get("latency_ms", 0),
            status=data.get("status", ""),
        )

    def solve_cloudflare(self, site_url: str) -> SolveResult:
        """Solve a Cloudflare Turnstile challenge."""
        data = self._post("/solve/cloudflare", {"site_url": site_url})
        return SolveResult(
            text=data.get("token", data.get("text", "")),
            task_id=data.get("task_id", ""),
            latency_ms=data.get("latency_ms", 0),
            status=data.get("status", ""),
        )

    def solve_audio(self, audio_base64: str) -> SolveResult:
        """Solve an audio CAPTCHA using Whisper AI."""
        data = self._post("/solve/audio", {"audio": audio_base64})
        return SolveResult(
            text=data.get("text", ""),
            task_id=data.get("task_id", ""),
            latency_ms=data.get("latency_ms", 0),
            status=data.get("status", ""),
        )

    # ── Document AI ──

    def extract_csf(self, document_base64: str) -> ExtractResult:
        """Extract data from a CSF (Constancia de Situacion Fiscal)."""
        data = self._post("/solve/extract_csf", {"document": document_base64})
        return ExtractResult(data=data.get("data", {}), task_id=data.get("task_id", ""), latency_ms=data.get("latency_ms", 0), status=data.get("status", ""))

    def extract_ine(self, document_base64: str) -> ExtractResult:
        """Extract data from an INE (Mexican voter ID)."""
        data = self._post("/solve/extract_ine", {"document": document_base64})
        return ExtractResult(data=data.get("data", {}), task_id=data.get("task_id", ""), latency_ms=data.get("latency_ms", 0), status=data.get("status", ""))

    def extract_cfdi(self, document_base64: str) -> ExtractResult:
        """Extract data from a CFDI (Mexican invoice)."""
        data = self._post("/solve/extract_cfdi", {"document": document_base64})
        return ExtractResult(data=data.get("data", {}), task_id=data.get("task_id", ""), latency_ms=data.get("latency_ms", 0), status=data.get("status", ""))

    def extract_curp(self, document_base64: str) -> ExtractResult:
        """Extract data from a CURP document."""
        data = self._post("/solve/extract_curp", {"document": document_base64})
        return ExtractResult(data=data.get("data", {}), task_id=data.get("task_id", ""), latency_ms=data.get("latency_ms", 0), status=data.get("status", ""))

    def extract_domicilio(self, document_base64: str) -> ExtractResult:
        """Extract data from a proof of address document."""
        data = self._post("/solve/extract_domicilio", {"document": document_base64})
        return ExtractResult(data=data.get("data", {}), task_id=data.get("task_id", ""), latency_ms=data.get("latency_ms", 0), status=data.get("status", ""))

    def extract_nomina(self, document_base64: str) -> ExtractResult:
        """Extract data from a payroll receipt."""
        data = self._post("/solve/extract_nomina", {"document": document_base64})
        return ExtractResult(data=data.get("data", {}), task_id=data.get("task_id", ""), latency_ms=data.get("latency_ms", 0), status=data.get("status", ""))

    def extract_generic(self, document_base64: str) -> ExtractResult:
        """Extract data from a generic document using OCR."""
        data = self._post("/solve/extract_generic", {"document": document_base64})
        return ExtractResult(data=data.get("data", {}), task_id=data.get("task_id", ""), latency_ms=data.get("latency_ms", 0), status=data.get("status", ""))

    # ── Utilities ──

    def hello(self) -> dict:
        """Test your API key connectivity."""
        return self._post("/hello", {})

    def get_balance(self) -> dict:
        """Get account balance and usage info."""
        url = f"{self.base_url}/balance"
        resp = self._session.get(url)
        if not resp.ok:
            raise OcilarError(resp.status_code, resp.text)
        return resp.json()
