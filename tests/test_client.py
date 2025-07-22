"""Tests for the VisualLayerClient."""

from src.visual_layer_sdk.client import VisualLayerClient
from src.visual_layer_sdk.dataset import Dataset
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch


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
