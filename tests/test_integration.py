import os

import pandas as pd
import pytest
from dotenv import load_dotenv

from src.visual_layer_sdk.client import VisualLayerClient
from src.visual_layer_sdk.dataset import Dataset, IssueType, SearchOperator

load_dotenv()

API_KEY = os.getenv("VISUAL_LAYER_API_KEY")
API_SECRET = os.getenv("VISUAL_LAYER_API_SECRET")
DATASET_ID = "bc41491e-78ae-11ef-ba4b-8a774758b536"


@pytest.mark.skipif(not API_KEY or not API_SECRET, reason="API credentials not set in .env")
class TestIntegration:
    @classmethod
    def setup_class(cls):
        cls.client = VisualLayerClient(API_KEY, API_SECRET)
        cls.dataset = Dataset(cls.client, DATASET_ID)

    def test_get_stats(self):
        stats = self.dataset.get_stats()
        print("Stats:", stats)
        assert isinstance(stats, dict)

    def test_get_details(self):
        details = self.dataset.get_details()
        print("Details:", details)
        assert details["id"] == DATASET_ID

    def test_explore(self):
        df = self.dataset.explore()
        print("Explore DataFrame shape:", df.shape)
        assert isinstance(df, pd.DataFrame)

    def test_export_to_dataframe(self):
        df = self.dataset.export_to_dataframe()
        print("Exported DataFrame shape:", df.shape)
        assert isinstance(df, pd.DataFrame)

    def test_search_by_labels(self):
        df = self.dataset.search_by_labels(["leaf", "spot"], "IMAGES", search_operator=SearchOperator.IS_ONE_OF)
        print("Label search DataFrame shape:", df.shape)
        assert isinstance(df, pd.DataFrame)

    def test_search_by_captions(self):
        df = self.dataset.search_by_captions(["leaf", "spot"], "IMAGES", search_operator=SearchOperator.IS)
        print("Caption search DataFrame shape:", df.shape)
        assert isinstance(df, pd.DataFrame)

    def test_search_by_issues(self):
        df = self.dataset.search_by_issues(issue_type=IssueType.BLUR, entity_type="IMAGES", search_operator=SearchOperator.IS_ONE_OF)
        print("Issue search DataFrame shape:", df.shape)
        assert isinstance(df, pd.DataFrame)

    def test_get_user_config(self):
        config = self.dataset._get_user_config()
        print("User config:", config)
        assert isinstance(config, dict)

    def test_client_get_all_datasets(self):
        df = self.client.get_all_datasets()
        print("All datasets DataFrame shape:", df.shape)
        assert isinstance(df, pd.DataFrame)

    def test_client_get_dataset(self):
        df = self.client.get_dataset(DATASET_ID)
        print("Get dataset DataFrame shape:", df.shape)
        assert isinstance(df, pd.DataFrame)

    def test_client_get_dataset_object(self):
        ds = self.client.get_dataset_object(DATASET_ID)
        print("Dataset object:", ds)
        assert isinstance(ds, Dataset)
