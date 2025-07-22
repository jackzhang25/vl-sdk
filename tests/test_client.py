"""Tests for the VisualLayerClient."""

from unittest.mock import MagicMock, patch

import pandas as pd

from src.visual_layer_sdk.client import VisualLayerClient
from src.visual_layer_sdk.dataset import Dataset


class TestVisualLayerClient:
    """Test cases for VisualLayerClient."""

    def test_client_initialization(self):
        """Test that the client initializes correctly."""
        api_key = "test_key"
        api_secret = "test_secret"

        client = VisualLayerClient(api_key, api_secret)

        assert client.api_key == api_key
        assert client.api_secret == api_secret
        assert client.base_url == "https://app.visual-layer.com/api/v1"

    def test_generate_jwt(self):
        """Test JWT token generation."""
        api_key = "test_key"
        api_secret = "test_secret"

        client = VisualLayerClient(api_key, api_secret)
        jwt_token = client._generate_jwt()

        assert jwt_token is not None
        assert isinstance(jwt_token, str)

    def test_get_headers(self):
        """Test header generation."""
        api_key = "test_key"
        api_secret = "test_secret"

        client = VisualLayerClient(api_key, api_secret)
        headers = client._get_headers()

        assert "Authorization" in headers
        assert headers["accept"] == "application/json"
        assert headers["Content-Type"] == "application/json"
        assert headers["Authorization"].startswith("Bearer ")

    def test_get_headers_no_jwt(self):
        """Test header generation without JWT."""
        api_key = "test_key"
        api_secret = "test_secret"

        client = VisualLayerClient(api_key, api_secret)
        headers = client._get_headers_no_jwt()

        assert "Authorization" not in headers
        assert headers["accept"] == "application/json"
        assert headers["Content-Type"] == "application/json"


class TestDatasetSearch:
    def test_search_by_visual_similarity(self):
        # Mock client and session
        mock_client = MagicMock()
        mock_client.base_url = "https://app.visual-layer.com/api/v1"
        mock_client._get_headers.return_value = {"Authorization": "Bearer test", "accept": "application/json", "Content-Type": "application/json"}
        mock_client.session.get.return_value.json.return_value = {"status": "READY"}
        mock_client.session.get.return_value.raise_for_status = MagicMock()
        mock_client.session.post.return_value.json.return_value = {"anchor_media_id": "test_media_id"}
        mock_client.session.post.return_value.raise_for_status = MagicMock()

        # Patch Dataset._validate_dataset_exists to do nothing
        with patch.object(Dataset, "_validate_dataset_exists", return_value=None):
            # Patch search_by_image_file to return a fake anchor_media_id
            with patch.object(Dataset, "search_by_image_file", return_value={"anchor_media_id": "test_media_id"}):
                # Patch search_by_vql to return a dummy DataFrame
                with patch.object(Dataset, "search_by_vql", return_value=pd.DataFrame({"id": [1], "score": [0.99]})) as mock_search_by_vql:
                    dataset = Dataset(mock_client, "test-dataset-id")
                    df = dataset.search_by_visual_similarity("/path/to/image.jpg", threshold=10)
                    assert isinstance(df, pd.DataFrame)
                    assert not df.empty
                    mock_search_by_vql.assert_called()


class TestDatasetRegression:
    def setup_method(self):
        mock_client = MagicMock()
        mock_client.base_url = "https://app.visual-layer.com/api/v1"
        mock_client._get_headers.return_value = {"Authorization": "Bearer test", "accept": "application/json", "Content-Type": "application/json"}
        mock_client.session.get.return_value.raise_for_status = MagicMock()
        mock_client.session.post.return_value.raise_for_status = MagicMock()
        with patch.object(Dataset, "_validate_dataset_exists", return_value=None):
            self.dataset = Dataset(mock_client, "test-dataset-id")

    def test_get_stats(self):
        with patch.object(self.dataset.client.session, "get") as mock_get:
            mock_get.return_value.json.return_value = {"stat": 1}
            mock_get.return_value.raise_for_status = MagicMock()
            stats = self.dataset.get_stats()
            assert stats == {"stat": 1}

    def test_get_details(self):
        with patch.object(self.dataset.client.session, "get") as mock_get:
            mock_get.return_value.json.return_value = {"id": "test", "status": "READY"}
            mock_get.return_value.raise_for_status = MagicMock()
            details = self.dataset.get_details()
            assert details["id"] == "test"

    def test_explore(self):
        with patch.object(self.dataset.client.session, "get") as mock_get:
            mock_get.return_value.json.return_value = {"clusters": [{"previews": [{"id": 1}]}]}
            mock_get.return_value.raise_for_status = MagicMock()
            df = self.dataset.explore()
            assert not df.empty
            assert "id" in df.columns

    def test_delete(self):
        with patch.object(self.dataset.client.session, "delete") as mock_delete:
            mock_delete.return_value.json.return_value = {"deleted": True}
            mock_delete.return_value.raise_for_status = MagicMock()
            result = self.dataset.delete()
            assert result["deleted"] is True

    def test_get_image_info(self):
        with patch.object(self.dataset.client.session, "get") as mock_get:
            mock_get.return_value.json.return_value = [1, 2, 3]
            mock_get.return_value.raise_for_status = MagicMock()
            info = self.dataset.get_image_info("imgid")
            assert info == [1, 2, 3]

    def test_export(self):
        with patch.object(self.dataset, "get_status", return_value="READY"):
            with patch.object(self.dataset.client.session, "get") as mock_get:
                mock_get.return_value.json.return_value = {"media_items": []}
                mock_get.return_value.raise_for_status = MagicMock()
                result = self.dataset.export()
                assert "media_items" in result

    def test_export_to_dataframe(self):
        with patch.object(self.dataset, "get_status", return_value="READY"):
            with patch.object(self.dataset, "export", return_value={"media_items": [{"id": 1, "metadata_items": []}]}):
                df = self.dataset.export_to_dataframe()
                assert not df.empty
                assert "id" in df.columns

    def test_get_status(self):
        with patch.object(self.dataset, "get_details", return_value={"status": "READY"}):
            status = self.dataset.get_status()
            assert status == "READY"

    def test_process_export_download_to_dataframe(self):
        with patch.object(self.dataset, "download_export_results", return_value={"media_items": [{"id": 1, "metadata_items": []}]}):
            df = self.dataset.process_export_download_to_dataframe("dummy_uri")
            assert not df.empty
            assert "id" in df.columns

    def test_search_by_captions(self):
        with patch.object(self.dataset, "search_by_vql", return_value=pd.DataFrame({"id": [1]})) as mock_vql:
            df = self.dataset.search_by_captions(["cat", "dog"])
            assert not df.empty
            mock_vql.assert_called()

    def test_search_by_labels(self):
        with patch.object(self.dataset, "search_by_vql", return_value=pd.DataFrame({"id": [1]})) as mock_vql:
            df = self.dataset.search_by_labels(["cat", "dog"])
            assert not df.empty
            mock_vql.assert_called()

    def test_search_by_issues(self):
        with patch.object(self.dataset, "search_by_vql", return_value=pd.DataFrame({"id": [1]})) as mock_vql:
            from src.visual_layer_sdk.dataset import IssueType

            df = self.dataset.search_by_issues(issue_type=IssueType.BLUR)
            assert not df.empty
            mock_vql.assert_called()

    def test_search_by_vql(self):
        with patch.object(self.dataset, "process_export_download_to_dataframe", return_value=pd.DataFrame({"id": [1]})):
            with patch.object(self.dataset.client.session, "get") as mock_get:
                mock_get.return_value.json.return_value = {"download_uri": "uri", "status": "COMPLETED", "id": "taskid"}
                mock_get.return_value.raise_for_status = MagicMock()
                df = self.dataset.search_by_vql([{"id": "label_filter"}], "IMAGES")
                assert not df.empty

    def test_download_export_results(self):
        with patch.object(self.dataset.client.session, "get") as mock_get:
            mock_get.return_value.headers = {"content-type": "application/json"}
            mock_get.return_value.json.return_value = {"media_items": []}
            mock_get.return_value.raise_for_status = MagicMock()
            result = self.dataset.download_export_results("dummy_uri")
            assert "media_items" in result

    def test_search_by_image_file(self):
        with patch("builtins.open", create=True):
            with patch.object(self.dataset.client.session, "post") as mock_post:
                mock_post.return_value.json.return_value = {"anchor_media_id": "mid"}
                mock_post.return_value.raise_for_status = MagicMock()
                with patch("os.path.exists", return_value=True):
                    from pathlib import Path

                    with patch.object(Path, "is_file", return_value=True):
                        result = self.dataset.search_by_image_file("/tmp/img.jpg")
                        assert result["anchor_media_id"] == "mid"
