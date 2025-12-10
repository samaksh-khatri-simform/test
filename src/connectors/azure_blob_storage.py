"""
Minimal Azure Blob Storage connector skeleton for TH1-T309.

This is a lightweight placeholder that defines the public interface without
introducing external dependencies. Replace the stub implementations with a real
implementation using the Azure SDK (azure-storage-blob) or REST API as needed.

Suggested implementation steps:
- Install dependency: pip install azure-storage-blob
- Wire up client creation via connection string, account_url + credential, or managed identity
- Implement list_blobs, upload_bytes, download_bytes, delete_blob using BlobServiceClient

Example (future):
    from connectors.azure_blob_storage import AzureBlobStorage
    client = AzureBlobStorage(connection_string=os.environ["AZURE_STORAGE_CONNECTION_STRING"])
    client.upload_bytes("my-container", "hello.txt", b"Hello")
    print(list(client.list_blobs("my-container")))
"""
from __future__ import annotations

from typing import Iterable, Optional


class AzureBlobStorage:
    """Minimal Azure Blob Storage connector interface.

    Note: Methods are stubbed. Implementations should use the Azure SDK:
      https://pypi.org/project/azure-storage-blob/
    """

    def __init__(
        self,
        connection_string: Optional[str] = None,
        account_url: Optional[str] = None,
        credential: Optional[str] = None,
    ) -> None:
        self.connection_string = connection_string
        self.account_url = account_url
        self.credential = credential

    def list_blobs(self, container: str, prefix: str = "") -> Iterable[str]:
        """Return an iterable of blob names in the given container.

        Replace with real implementation. Currently returns an empty iterator.
        """
        return iter(())

    def upload_bytes(
        self,
        container: str,
        blob_name: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> None:
        """Upload bytes to the specified blob.

        Replace with real implementation.
        """
        # TODO: Implement using azure.storage.blob.BlobClient
        return None

    def download_bytes(self, container: str, blob_name: str) -> bytes:
        """Download and return blob content as bytes.

        Replace with real implementation. Currently returns empty bytes.
        """
        # TODO: Implement using azure.storage.blob.BlobClient
        return b""

    def delete_blob(self, container: str, blob_name: str) -> None:
        """Delete the specified blob if it exists.

        Replace with real implementation.
        """
        # TODO: Implement using azure.storage.blob.BlobClient
        return None
