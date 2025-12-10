import builtins
import types
from unittest import mock
import pytest

from connectors.azure_blob_connector import AzureBlobConnector


class DummyBlob:
    def __init__(self):
        self._data = b""

    def upload_blob(self, data, overwrite=True):
        self._data = data

    def download_blob(self):
        return types.SimpleNamespace(readall=lambda: self._data)

    def delete_blob(self):
        self._data = b""


class DummyContainer:
    def __init__(self):
        self._blobs = {"a.txt": DummyBlob(), "b/c.txt": DummyBlob()}

    def list_blobs(self, name_starts_with=None):
        for name in list(self._blobs.keys()):
            if name_starts_with is None or name.startswith(name_starts_with):
                yield types.SimpleNamespace(name=name)

    def get_blob_client(self, name):
        if name not in self._blobs:
            self._blobs[name] = DummyBlob()
        return self._blobs[name]


class DummyService:
    def __init__(self, container: DummyContainer):
        self._container = container

    def get_container_client(self, name):
        return self._container

    @classmethod
    def from_connection_string(cls, conn):
        return cls(DummyContainer())


@mock.patch("connectors.azure_blob_connector.AzureBlobConnector._ensure_sdk")
@mock.patch("connectors.azure_blob_connector.AzureBlobConnector._get_container_client")
def test_list_and_upload_and_download(mock_get_container, mock_ensure):
    # Arrange dummy SDK
    mock_ensure.return_value = (DummyService, object)
    dummy_container = DummyContainer()
    mock_get_container.return_value = dummy_container

    c = AzureBlobConnector(container="test", connection_string="UseDevelopmentStorage=true")

    # List first two
    names = c.list_blobs(max_results=2)
    assert len(names) == 2

    # Upload and download
    c.upload_bytes("hello.txt", b"hello")
    assert c.download_bytes("hello.txt") == b"hello"

    # Delete
    c.delete_blob("hello.txt")
    assert c.download_bytes("hello.txt") == b""  # since DummyBlob returns empty after delete
