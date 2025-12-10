"""
Minimal Azure Blob Storage connector skeleton.

Task: TH1-T309 - Work on adding Microsoft Blob Storage connector

This module defines a minimal interface for Azure Blob operations. The actual
implementation should use the official 'azure-storage-blob' package, but is
intentionally left as NotImplemented for the initial scaffolding.

Usage (future):
    connector = AzureBlobConnector(connection_string="<conn>", container="my-container")
    # connector.upload_bytes(...)
"""
from typing import Iterable, Optional


class AzureBlobConnector:
    """A minimal interface for Azure Blob Storage operations."""

    def __init__(self, connection_string: str, container: str):
        self.connection_string = connection_string
        self.container = container

    def list_blobs(self, prefix: Optional[str] = None) -> Iterable[str]:
        """List blob names in the container, optionally filtered by prefix.

        Not implemented in this skeleton.
        """
        raise NotImplementedError("Implement using azure-storage-blob")

    def upload_bytes(self, name: str, data: bytes, overwrite: bool = True) -> None:
        """Upload bytes to a blob named 'name'.

        Not implemented in this skeleton.
        """
        raise NotImplementedError("Implement using azure-storage-blob")

    def download_bytes(self, name: str) -> bytes:
        """Download blob 'name' and return its content as bytes.

        Not implemented in this skeleton.
        """
        raise NotImplementedError("Implement using azure-storage-blob")

    def delete_blob(self, name: str) -> None:
        """Delete blob 'name'.

        Not implemented in this skeleton.
        """
        raise NotImplementedError("Implement using azure-storage-blob")
