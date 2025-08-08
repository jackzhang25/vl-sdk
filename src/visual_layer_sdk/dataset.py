import json
import uuid
from enum import Enum
from typing import List

import pandas as pd
from typeguard import typechecked

from .logger import get_logger
from .searchable_dataset import Searchable


class SearchOperator(Enum):
    IS = "is"
    IS_NOT = "is_not"
    IS_ONE_OF = "one_of"
    IS_NOT_ONE_OF = "not_one_of"


class IssueType(Enum):
    MISLABELS = "mislabels"
    OUTLIERS = "outliers"
    DUPLICATES = "duplicates"
    BLUR = "blur"
    DARK = "dark"
    BRIGHT = "bright"
    NORMAL = "normal"
    LABEL_OUTLIER = "label_outlier"


class SemanticRelevance(Enum):
    LOW_RELEVANCE = 0.9
    MEDIUM_RELEVANCE = 0.8
    HIGH_RELEVANCE = 0.7


ISSUE_TYPE_MAPPING = {
    0: {"name": "mislabels", "description": "Mislabeled items", "severity": 0},
    1: {"name": "outliers", "description": "Outlier detection", "severity": 0},
    2: {"name": "duplicates", "description": "Duplicate detection", "severity": 0},
    3: {"name": "blur", "description": "Blurry images", "severity": 1},
    4: {"name": "dark", "description": "Dark images", "severity": 1},
    5: {"name": "bright", "description": "Bright images", "severity": 2},
    6: {"name": "normal", "description": "Normal images", "severity": 0},
    7: {"name": "label_outlier", "description": "Label outliers", "severity": 0},
}
ALLOWED_ISSUE_NAMES = {v["name"] for v in ISSUE_TYPE_MAPPING.values()}


class Dataset:
    # TODO: add in details what search capabilities are available for the dataset
    def __init__(self, client, dataset_id: str, poll_interval: int = 10, timeout: int = 300):
        self.client = client
        self.dataset_id = dataset_id
        self.base_url = client.base_url
        self.logger = get_logger()
        self.poll_interval = poll_interval
        self.timeout = timeout

        # Validate that the dataset exists
        self._validate_dataset_exists()

        # Create the single Searchable object for this dataset
        from .searchable_dataset import Searchable

        self.searchable = Searchable(self, [])

    def _validate_dataset_exists(self):
        """Validate that the dataset exists by calling the get_details API"""
        try:
            response = self.client.session.get(
                f"{self.base_url}/dataset/{self.dataset_id}",
                headers=self.client._get_headers(),
            )
            response.raise_for_status()
        except Exception as e:
            if "Not Found" in str(e) or response.status_code == 404:
                raise ValueError(f"Dataset '{self.dataset_id}' does not exist. Please check the dataset ID and try again.")
            else:
                raise RuntimeError(f"Failed to validate dataset '{self.dataset_id}': {str(e)}")

    def __str__(self) -> str:
        """String representation of the dataset with its details"""
        try:
            details = self.get_details()
            status = details.get("status", "Unknown")
            display_name = details.get("display_name", "No name")
            description = details.get("description", "No description")
            created_at = details.get("created_at", "Unknown")
            filename = details.get("filename", "me")

            return f"Dataset(id='{self.dataset_id}', name='{display_name}', status='{status}', filename='{filename}', created_at='{created_at}', description={description})"
        except Exception as e:
            return f"Dataset(id='{self.dataset_id}', error='{str(e)}')"

    def __repr__(self) -> str:
        """String representation of the dataset with its details"""
        return self.__str__()

    @typechecked
    def get_stats(self) -> dict:
        """Get statistics for this dataset"""
        response = self.client.session.get(
            f"{self.base_url}/dataset/{self.dataset_id}/stats",
            headers=self.client._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    @typechecked
    def get_details(self) -> dict:
        """Get details for this dataset"""
        response = self.client.session.get(
            f"{self.base_url}/dataset/{self.dataset_id}",
            headers=self.client._get_headers(),
        )
        response.raise_for_status()
        full_response = response.json()

        # Filter to only include the specified fields
        selected_fields = [
            "id",
            "created_by",
            "source_dataset_id",
            "owned_by",
            "display_name",
            "description",
            "preview_uri",
            "source_type",
            "source_uri",
            "created_at",
            "updated_at",
            "filename",
            "sample",
            "status",
        ]

        # Create filtered dictionary with only the selected fields
        filtered_details = {field: full_response.get(field) for field in selected_fields}

        # Add search capabilities information
        try:
            user_config = self._get_user_config()
            search_capabilities = {
                "labels_search": user_config.get("labels_search", False),
                "captions_search": user_config.get("captions_search", False),
                "semantic_search": user_config.get("semantic_search", False),
            }
            filtered_details["search_capabilities"] = search_capabilities
        except Exception as e:
            # If we can't get user config, set all search capabilities to None
            self.logger.warning(f"Could not retrieve search capabilities: {str(e)}")
            filtered_details["search_capabilities"] = {
                "labels_search": None,
                "captions_search": None,
                "semantic_search": None,
            }

        return filtered_details

    @typechecked
    def explore(self) -> pd.DataFrame:
        """Explore this dataset and return previews as a DataFrame"""
        response = self.client.session.get(
            f"{self.base_url}/explore/{self.dataset_id}",
            headers=self.client._get_headers(),
        )
        response.raise_for_status()
        data = response.json()

        # Extract just the previews from the first cluster
        if data.get("clusters") and len(data["clusters"]) > 0:
            previews = data["clusters"][0].get("previews", [])
            # Convert previews to DataFrame
            df = pd.DataFrame(previews)
            return df
        else:
            return pd.DataFrame()  # Return empty DataFrame if no previews found

    @typechecked
    def delete(self) -> dict:
        """Delete this dataset"""
        response = self.client.session.delete(
            f"{self.base_url}/dataset/{self.dataset_id}",
            headers=self.client._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    @typechecked
    def get_image_info(self, image_id) -> dict:
        response = self.client.session.get(
            f"{self.base_url}/image/{image_id}",
            headers=self.client._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    # include image_uri in export
    @typechecked
    def export(self) -> dict:
        """Export this dataset in JSON format"""
        # Check if dataset is ready before exporting
        status = self.get_status()
        if status not in ["READY", "completed"]:
            raise RuntimeError(f"Cannot export dataset {self.dataset_id}. Current status: {status}. Dataset must be 'ready' or 'completed' to export.")

        url = f"{self.base_url}/dataset/{self.dataset_id}/export"
        params = {"export_format": "json"}
        headers = {**self.client._get_headers()}
        response = self.client.session.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    @typechecked
    def export_to_dataframe(self) -> pd.DataFrame:
        """
        Export this dataset and convert media_items to a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing media_items (excluding metadata_items)
        """
        try:
            # Check if dataset is ready before exporting
            status = self.get_status()
            if status not in ["READY", "completed"]:
                self.logger.dataset_not_ready(self.dataset_id, status)
                return pd.DataFrame()

            # Export the dataset
            export_data = self.export()

            # Extract media_items from the export data
            if "media_items" in export_data:
                media_items = export_data["media_items"]

                # Remove metadata_items from each media item if it exists
                cleaned_media_items = []
                for item in media_items:
                    # Create a copy of the item without metadata_items
                    cleaned_item = {k: v for k, v in item.items() if k != "metadata_items"}
                    cleaned_media_items.append(cleaned_item)

                # Convert to DataFrame
                df = pd.DataFrame(cleaned_media_items)
                self.logger.export_completed(self.dataset_id, len(df))
                return df
            else:
                self.logger.warning("No media_items found in export data")
                return pd.DataFrame()

        except Exception as e:
            self.logger.export_failed(self.dataset_id, str(e))
            return pd.DataFrame()

    @typechecked
    def get_status(self) -> str:
        return self.get_details()["status"]

    @typechecked
    def search(self) -> Searchable:
        """
        Get the Searchable object for this dataset to perform search operations.

        Returns:
            Searchable: The Searchable object that can be used to chain search operations

        Examples:
            searchable = dataset.search()
            results = searchable.search_by_labels(["cat"]).search_by_captions(["sitting"]).get_results()

            # Reset and start a new search
            dataset.search().reset()
            new_results = dataset.search().search_by_issues([IssueType.BLUR]).get_results()
        """
        return self.searchable

    @typechecked
    def search_by_vql(self, vql: List[dict], entity_type: str = "IMAGES") -> pd.DataFrame:
        """
        Search dataset using custom VQL (Visual Query Language) asynchronously, poll until export is ready, download the results, and return as a DataFrame.
        This method is used internally by the Searchable object.

        Args:
            vql (List[dict]): VQL query structure as a list of filter objects
            entity_type (str): Entity type to search ("IMAGES" or "OBJECTS", default: "IMAGES")

        Returns:
            pd.DataFrame: DataFrame containing the search results, or empty if not ready

        Examples:
            vql = [{"id": "label_filter", "labels": {"op": "one_of", "value": ["cat", "dog"]}}]
            df = dataset.search_by_vql(vql)
        """
        if not vql:
            self.logger.warning("No VQL provided for search")
            return pd.DataFrame()

        url = f"{self.base_url}/dataset/{self.dataset_id}/export_context_async"
        params = {"export_format": "json", "include_images": False, "entity_type": entity_type, "vql": json.dumps(vql)}

        try:
            import time

            start_time = time.time()
            self.logger.info(f"Starting VQL search with query: {vql}")
            response = self.client.session.get(url, headers=self.client._get_headers(), params=params)
            response.raise_for_status()
            status_result = response.json()
            self.logger.success("VQL search export task created successfully")
            download_uri = status_result.get("download_uri")
            status = status_result.get("status")
            export_task_id = status_result.get("id")

            # If no download_uri in the first response, return empty DataFrame immediately
            if status == "REJECTED" or status is None:
                self.logger.info("No images matched the VQL search. Returning empty DataFrame.")
                return pd.DataFrame()

            # Poll if not ready
            while (status != "COMPLETED" or not download_uri) and (time.time() - start_time < self.timeout):
                self.logger.info(f"Export not ready (status: {status}). Waiting {self.poll_interval}s before polling again...")
                time.sleep(self.poll_interval)
                # Poll status endpoint
                poll_status = self.client.session.get(
                    f"{self.client.base_url}/dataset/{self.dataset_id}/export_status",
                    headers=self.client._get_headers(),
                    params={"export_task_id": export_task_id, "dataset_id": self.dataset_id},
                )
                poll_status.raise_for_status()
                status_result = poll_status.json()
                download_uri = status_result.get("download_uri")
                status = status_result.get("status")

                # Check if export was rejected during polling
                if status == "REJECTED":
                    result_message = status_result.get("result_message", "No reason provided")
                    self.logger.error(f"Export request rejected during polling: {result_message}")
                    print(f"❌ Export request rejected during polling: {result_message}")
                    return pd.DataFrame()

            if status != "COMPLETED" or not download_uri:
                self.logger.warning(f"Export not completed or no download_uri after waiting. Final status: {status}")
                return pd.DataFrame()

            # Step 2: Use the general processor
            return self._process_export_download_to_dataframe(download_uri)
        except Exception as e:
            self.logger.error(f"VQL search failed: {str(e)}")
            raise

    def _search_by_image_file(self, image_path: str, allow_deleted: bool = False) -> dict:
        """
        Upload an image file and get the anchor media ID for similarity search.
        This method is used internally by the Searchable object.

        Args:
            image_path (str): Path to the image file (JPEG, PNG, etc.)
            allow_deleted (bool): Whether to include deleted images in search (default: False)

        Returns:
            dict: Dictionary with anchor_media_id and anchor_type

        Examples:
            result = dataset._search_by_image_file("/path/to/image.jpg")
        """
        import os
        from pathlib import Path

        # Validate file exists
        if not os.path.exists(image_path):
            raise ValueError(f"Image file not found: {image_path}")

        # Get file info
        file_path = Path(image_path)
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {image_path}")

        # Determine content type
        content_type = "image/jpeg"  # Default
        if file_path.suffix.lower() in [".png"]:
            content_type = "image/png"
        elif file_path.suffix.lower() in [".jpg", ".jpeg"]:
            content_type = "image/jpeg"

        url = f"{self.base_url}/dataset/{self.dataset_id}/search-image-similarity"
        params = {"allow_deleted": allow_deleted}

        try:
            self.logger.info(f"Uploading image file for similarity search: {image_path}")

            # Prepare multipart form data
            with open(image_path, "rb") as file:
                files = {"file": (file_path.name, file, content_type)}

                # Remove Content-Type header to let requests set it for multipart
                headers = self.client._get_headers()
                headers.pop("Content-Type", None)

                self.logger.debug(f"URL: {url}")
                self.logger.debug(f"Params: {params}")
                self.logger.debug(f"Headers: {headers}")
                self.logger.debug(f"File: {file_path.name}, Content-Type: {content_type}")

                response = self.client.session.post(url, headers=headers, params=params, files=files)

                self.logger.debug(f"Response status: {response.status_code}")
                self.logger.debug(f"Response headers: {dict(response.headers)}")

                if response.status_code != 200:
                    self.logger.debug(f"Response text: {response.text}")

                response.raise_for_status()
                result = response.json()

                self.logger.success("Image similarity search completed successfully")
                return result

        except Exception as e:
            self.logger.error(f"Image similarity search failed: {str(e)}")
            raise

    def _get_user_config(self) -> dict:
        """
        Get the user config for this dataset from the /user_config endpoint.
        This method is used internally by the Searchable object.

        Returns:
            dict: {"labels_search": bool or None, "captions_search": bool or None, "semantic_search": bool or None}
        """
        url = f"{self.base_url}/user_config"
        params = {"dataset_id": self.dataset_id}
        headers = self.client._get_headers()
        response = self.client.session.get(url, params=params, headers=headers)
        response.raise_for_status()
        full_response = response.json()

        labels_search = None
        captions_search = None
        semantic_search = None
        features = full_response.get("features", [])
        for feature in features:
            if feature.get("feature_key") == "TEXTUAL_SEARCH_IMAGE":
                options = feature.get("feature_options", {})
                labels_search = options.get("labels_search")
                captions_search = options.get("captions_search")
                semantic_search = options.get("semantic_search")
                break

        return {
            "labels_search": labels_search,
            "captions_search": captions_search,
            "semantic_search": semantic_search,
        }

    def _download_export_results(self, download_uri: str) -> dict:
        """
        Download the export results from the provided URI.
        Handles both ZIP (with JSON inside) and direct JSON responses.
        This method is used internally by the Searchable object.

        Args:
            download_uri (str): The download URI from the export status response

        Returns:
            dict: The downloaded export data (parsed from JSON inside ZIP if needed)
        """
        import io
        import zipfile

        try:
            self.logger.info(f"Downloading export results from: {download_uri}")
            response = self.client.session.get(download_uri)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            self.logger.debug(f"Response content type: {content_type}")
            self.logger.debug(f"Response status code: {response.status_code}")
            self.logger.debug(f"Response size: {len(response.content)} bytes")

            # Try ZIP extraction first (since we know it works)
            self.logger.info("Attempting ZIP extraction...")
            try:
                with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
                    self.logger.debug(f"ZIP contents: {zf.namelist()}")

                    # Look specifically for metadata.json
                    if "metadata.json" in zf.namelist():
                        self.logger.info("Found metadata.json")
                        with zf.open("metadata.json") as json_file:
                            json_bytes = json_file.read()
                            json_str = json_bytes.decode("utf-8")
                            result = json.loads(json_str)
                            self.logger.info("Successfully extracted and parsed JSON")
                            self.logger.debug(f"JSON keys: {list(result.keys())}")
                            if "media_items" in result:
                                self.logger.info(f"Number of media items: {len(result['media_items'])}")
                            self.logger.success("Export results downloaded and extracted from ZIP successfully")
                            return result
                    else:
                        self.logger.warning("metadata.json not found")
                        self.logger.debug(f"Available files: {zf.namelist()}")
                        raise ValueError("metadata.json not found in ZIP archive.")

            except Exception as zip_error:
                self.logger.warning(f"ZIP extraction failed: {str(zip_error)}")
                # Fall through to try JSON parsing

            # If ZIP extraction failed, try JSON parsing
            if "application/json" in content_type:
                result = response.json()
                self.logger.debug("Parsed as JSON")
                self.logger.debug(f"Response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                self.logger.success("Export results downloaded successfully")
                return result
            else:
                # Handle non-JSON responses (like text)
                self.logger.debug(f"Content type: {content_type}")
                self.logger.debug(f"Response size: {len(response.content)} bytes")
                # Try to parse as JSON anyway (in case content-type is wrong)
                try:
                    result = response.json()
                    self.logger.info("Successfully parsed as JSON")
                    self.logger.debug(f"Response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                except Exception as json_error:
                    self.logger.warning(f"Failed to parse as JSON: {str(json_error)}")
                    result = {"content_type": content_type, "size_bytes": len(response.content), "raw_text": response.text[:1000], "error": "Response is not valid JSON"}
                self.logger.success("Export results downloaded (non-JSON fallback)")
                return result

        except Exception as e:
            self.logger.error(f"Export download failed: {str(e)}")
            raise

    def _process_export_download_to_dataframe(self, download_uri: str) -> pd.DataFrame:
        """
        Download the export results from the provided URI and flatten to a DataFrame.
        Can be used by any async search function that returns a download_uri.
        This method is used internally by the Searchable object.

        Args:
            download_uri (str): The download URI from the export status response

        Returns:
            pd.DataFrame: DataFrame containing the search results, or empty if not valid
        """
        # Download and process the export results
        export_data = self._download_export_results(download_uri)
        if not export_data or "media_items" not in export_data:
            self.logger.warning("No media_items found in downloaded export data")
            return pd.DataFrame()

        # Flatten to DataFrame (reuse export_to_dataframe logic)
        processed_items = []
        for item in export_data["media_items"]:
            processed_item = item.copy()
            metadata_items = item.get("metadata_items", [])
            processed_item["captions"] = []
            processed_item["image_labels"] = []
            processed_item["object_labels"] = []
            processed_item["issues"] = []
            for metadata in metadata_items:
                metadata_type = metadata.get("type")
                properties = metadata.get("properties", {})
                if metadata_type == "caption":
                    caption = properties.get("caption", "")
                    if caption:
                        processed_item["captions"].append(caption)
                elif metadata_type == "image_label":
                    category = properties.get("category_name", "")
                    source = properties.get("source", "")
                    if category:
                        processed_item["image_labels"].append(f"{category}({source})")
                elif metadata_type == "object_label":
                    category = properties.get("category_name", "")
                    bbox = properties.get("bbox", [])
                    if category:
                        processed_item["object_labels"].append(f"{category}{bbox}")
                elif metadata_type == "issue":
                    issue_type = properties.get("issue_type", "")
                    description = properties.get("issues_description", "")
                    confidence = properties.get("confidence", 0.0)
                    if issue_type:
                        processed_item["issues"].append(f"{issue_type}:{description}({confidence:.3f})")
            processed_item["captions"] = "; ".join(processed_item["captions"])
            processed_item["image_labels"] = "; ".join(processed_item["image_labels"])
            processed_item["object_labels"] = "; ".join(processed_item["object_labels"])
            processed_item["issues"] = "; ".join(processed_item["issues"])
            processed_item.pop("metadata_items", None)
            processed_items.append(processed_item)

        df = pd.DataFrame(processed_items)
        self.logger.export_completed(self.dataset_id, len(df))
        return df

    @typechecked
    def get_available_models(self) -> list:
        """
        Get available models for enrichment for this dataset.

        Returns:
            list: List containing available models for enrichment

        Examples:
            models = dataset.get_available_models()
            print(f"Available models: {models}")
        """
        url = f"{self.base_url}/enrichment/{self.dataset_id}/list_models"
        headers = self.client._get_headers()

        try:
            self.logger.info(f"Fetching available models for dataset {self.dataset_id}")
            response = self.client.session.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            self.logger.success("Successfully retrieved available models")
            return result
        except Exception as e:
            self.logger.error(f"Failed to get available models: {str(e)}")
            raise

    @typechecked
    def enrich_dataset(self, enrichment_models: dict) -> dict:
        """
        Enrich the dataset with specified models.

        Args:
            enrichment_models (dict): Dictionary mapping enrichment types to model names.
                                    Example: {
                                        "CAPTION_IMAGES": "vl_image_captioner_v00",
                                        "OBJECT_DETECTION": "vl_object_detector_v00"
                                    }

        Returns:
            dict: Response from the enrichment API

        Examples:
            # Enrich with caption and object detection
            result = dataset.enrich_dataset({
                "CAPTION_IMAGES": "vl_image_captioner_v00",
                "OBJECT_DETECTION": "vl_object_detector_v00"
            })
            print(f"Enrichment result: {result}")
        """
        if not enrichment_models or not isinstance(enrichment_models, dict):
            raise ValueError("enrichment_models must be a non-empty dictionary")

        url = f"{self.base_url}/dataset/{self.dataset_id}/enrich_dataset"
        headers = self.client._get_headers()
        headers["Content-Type"] = "application/json"

        enrichment_config = {"enrichment_models": enrichment_models}

        try:
            self.logger.info(f"Starting enrichment for dataset {self.dataset_id}")
            self.logger.debug(f"Enrichment config: {enrichment_config}")

            response = self.client.session.post(url, headers=headers, json=enrichment_config)
            response.raise_for_status()
            result = response.json()

            self.logger.success("Dataset enrichment started successfully")
            return result
        except Exception as e:
            self.logger.error(f"Failed to enrich dataset: {str(e)}")
            raise

    @typechecked
    def check_enrichment_progress(self, enrichment_context_id: str) -> dict:
        """
        Check enrichment progress with percentage.

        Args:
            enrichment_context_id (str): The enrichment context ID from get_enrichment_context

        Returns:
            dict: Dictionary containing enrichment status and progress information

        Examples:
            context = dataset.get_enrichment_context()
            progress = dataset.check_enrichment_progress(context['context_id'])
            print(f"Progress: {progress['progress']}%")
        """
        url = f"{self.base_url}/enrichment/{self.dataset_id}/{enrichment_context_id}/status"
        headers = self.client._get_headers()

        try:
            self.logger.info(f"Checking enrichment progress for dataset {self.dataset_id}, context {enrichment_context_id}")
            response = self.client.session.get(url, headers=headers)
            response.raise_for_status()
            status = response.json()

            progress = status.get("progress", 0)
            self.logger.info(f"Enrichment status: {status.get('status', 'unknown')}, Progress: {progress}%")

            print(f"Status: {status.get('status', 'unknown')}")
            print(f"Progress: {progress}%")

            return status
        except Exception as e:
            self.logger.error(f"Failed to check enrichment progress: {str(e)}")
            raise
