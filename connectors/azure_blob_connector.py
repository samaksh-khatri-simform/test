"""
Minimal Azure Blob Storage connector (Python)

This is a lightweight skeleton to interact with Azure Blob Storage with minimal
setup and no hard dependency at import time. The azure-storage-blob package is
imported only when methods are invoked.

Install dependency (if needed):
    pip install azure-storage-blob

Example:
    from connectors.azure_blob_connector import AzureBlobConnector
    import os

    connector = AzureBlobConnector(
        container="my-container",
        connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
    )

    # List a few blobs
    print(connector.list_blobs(prefix=None, max_results=10))

    # Upload bytes
    connector.upload_bytes("hello.txt", b"hello world", overwrite=True)

    # Download
    data = connector.download_bytes("hello.txt")
    print(data)

    # Delete
    connector.delete_blob("hello.txt")
"""
from __future__ import annotations
from typing import List, Optional


class AzureBlobConnector:
    def __init__(
        self,
        *,
        container: str,
        connection_string: Optional[str] = None,
        account_url: Optional[str] = None,
        credential: Optional[object] = None,
    ) -> None:
        """
        Initialize the connector.

        Provide either:
          - connection_string, or
          - account_url + credential (SAS token/DefaultAzureCredential/etc.)
        """
        self._container = container
        self._connection_string = connection_string
        self._account_url = account_url
        self._credential = credential

    def _ensure_sdk(self):
        try:
            from azure.storage.blob import BlobServiceClient, ContainerClient  # type: ignore
        except Exception as exc:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "azure-storage-blob is required. Install via: pip install azure-storage-blob"
            ) from exc
        return BlobServiceClient, ContainerClient

    def _get_container_client(self):
        BlobServiceClient, ContainerClient = self._ensure_sdk()
        if self._connection_string:
            service = BlobServiceClient.from_connection_string(self._connection_string)
            return service.get_container_client(self._container)
        if self._account_url and self._credential is not None:
            service = BlobServiceClient(account_url=self._account_url, credential=self._credential)
            return service.get_container_client(self._container)
        raise ValueError(
            "Provide either connection_string or (account_url and credential)."
        )

    def list_blobs(self, prefix: Optional[str] = None, max_results: int = 100) -> List[str]:
        """Return up to max_results blob names in the container (optionally filtered by prefix)."""
        client = self._get_container_client()
        names: List[str] = []
        for b in client.list_blobs(name_starts_with=prefix):
            names.append(b.name)
            if len(names) >= max_results:
                break
        return names

    def upload_bytes(self, name: str, data: bytes, *, overwrite: bool = True) -> None:
        """Upload in-memory bytes to a blob."""
        client = self._get_container_client()
        blob = client.get_blob_client(name)
        blob.upload_blob(data, overwrite=overwrite)

    def download_bytes(self, name: str) -> bytes:
        """Download a blob and return its data as bytes."""
        client = self._get_container_client()
        blob = client.get_blob_client(name)
        stream = blob.download_blob()
        return stream.readall()

    def delete_blob(self, name: str) -> None:
        """Delete a blob by name (no error if missing)."""
        client = self._get_container_client()
        blob = client.get_blob_client(name)
        try:
            blob.delete_blob()
        except Exception:
            # Best-effort delete; ignore if already deleted or missing.
            pass


__all__ = ["AzureBlobConnector"]
