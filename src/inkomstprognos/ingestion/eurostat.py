"""Thin wrapper over the Eurostat REST API with local caching."""

from __future__ import annotations

import hashlib
import pathlib

import httpx
import pandas as pd

_CACHE_DIR = pathlib.Path.home() / ".cache" / "inkomstprognos" / "eurostat"
_BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"


class EurostatClient:
    """Client for the Eurostat REST API with Parquet caching.

    Args:
        cache_dir: Directory for cached responses.
        timeout: HTTP request timeout in seconds.

    Examples:
        >>> client = EurostatClient()
    """

    def __init__(
        self,
        cache_dir: pathlib.Path | None = None,
        timeout: float = 30.0,
    ) -> None:
        self._cache_dir = cache_dir or _CACHE_DIR
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._client = httpx.Client(timeout=timeout)

    def _cache_key(self, code: str, filters: dict[str, str] | None) -> str:
        raw = f"{code}:{filters}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def _cache_path(self, key: str) -> pathlib.Path:
        return self._cache_dir / f"{key}.parquet"

    def get_dataset(
        self,
        code: str,
        *,
        filters: dict[str, str] | None = None,
    ) -> pd.DataFrame:
        """Fetch a dataset from Eurostat, using cache if available.

        Args:
            code: Eurostat dataset code (e.g. 'nama_10_gdp').
            filters: Optional dictionary of query filters.

        Returns:
            pandas DataFrame with the requested dataset.

        Raises:
            httpx.HTTPStatusError: If the API request fails.

        Examples:
            >>> client = EurostatClient()
            >>> # client.get_dataset("nama_10_gdp")  # requires network
        """
        key = self._cache_key(code, filters)
        cache_file = self._cache_path(key)

        if cache_file.exists():
            return pd.read_parquet(cache_file)

        url = f"{_BASE_URL}/{code}"
        params: dict[str, str] = {"format": "TSV"}
        if filters:
            params.update(filters)

        response = self._client.get(url, params=params)
        response.raise_for_status()

        lines = response.text.strip().split("\n")
        if len(lines) < 2:
            return pd.DataFrame()

        header = lines[0].split("\t")
        data = [line.split("\t") for line in lines[1:]]
        df = pd.DataFrame(data, columns=header)

        df.to_parquet(cache_file, index=False)
        return df

    def close(self) -> None:
        """Close the underlying HTTP client.

        Examples:
            >>> client = EurostatClient()
            >>> client.close()
        """
        self._client.close()

    def __enter__(self) -> EurostatClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
