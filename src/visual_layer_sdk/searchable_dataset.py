from typing import List, Optional, Union
import uuid
import pandas as pd


class Searchable:
    """
    A wrapper around Dataset that provides fluent search interface.
    Allows chaining multiple search criteria together.
    """

    def __init__(self, dataset: "Dataset", vql_query: Optional[List[dict]] = None):
        """
        Initialize Searchable.

        Args:
            dataset: The original Dataset object
            vql_query: Optional initial VQL query to start with
        """
        self.original_dataset = dataset
        self.vql_query = vql_query or []
        self.dataset_id = dataset.dataset_id
        self.client = dataset.client
        # Generate a unique ID for this Searchable object
        self.searchable_id = str(uuid.uuid4())
        # Cache for storing results after first evaluation
        self._cached_results = None

        # Add this searchable to the client's storage
        if hasattr(self.client, "add_searchable"):
            self.client.add_searchable(self.searchable_id, self)

    def get_dataset(self) -> "Dataset":
        """
        Get the original Dataset object associated with this Searchable.

        Returns:
            Dataset: The original Dataset object
        """
        return self.original_dataset

    def get_searchable_id(self) -> str:
        """
        Get the unique ID of this Searchable object.

        Returns:
            str: The unique ID of this Searchable object
        """
        return self.searchable_id

    @classmethod
    def from_id(cls, searchable_id: str, dataset: "Dataset", vql_query: Optional[List[dict]] = None) -> "Searchable":
        """
        Create a Searchable object from an ID.

        Args:
            searchable_id: The ID to assign to the Searchable object
            dataset: The original Dataset object
            vql_query: Optional initial VQL query to start with

        Returns:
            Searchable: A new Searchable object with the specified ID
        """
        searchable = cls(dataset, vql_query)
        searchable.searchable_id = searchable_id

        # Add this searchable to the client's storage with the specified ID
        if hasattr(searchable.client, "add_searchable"):
            searchable.client.add_searchable(searchable_id, searchable)

        return searchable

    def chain_filters(self, *filters: "Searchable") -> "Searchable":
        """
        Chain multiple filters together to create a complex query.
        This method combines multiple Searchable objects into one with all their filters.

        Args:
            *filters: Variable number of Searchable objects to chain together

        Returns:
            New Searchable with all filters combined
        """
        if not filters:
            return self

        # Collect all VQL filters from all Searchable objects
        all_vql_filters = self.vql_query.copy()

        for filter_searchable in filters:
            if filter_searchable.vql_query:
                all_vql_filters.extend(filter_searchable.vql_query)

        # Create new Searchable with all filters
        new_searchable = Searchable(self.original_dataset, all_vql_filters)
        # Preserve the searchable_id
        new_searchable.searchable_id = self.searchable_id
        # Clear cached results for new query
        new_searchable._cached_results = None
        return new_searchable

    def search_by_labels(self, labels: Union[List[str], str], search_operator: "SearchOperator" = None) -> "Searchable":
        """
        Add label search criteria to the current query.

        Args:
            labels: Label(s) to search for
            search_operator: Search operator to use

        Returns:
            New Searchable with updated query
        """
        # Check if labels search is enabled in user config
        user_config = self.original_dataset._get_user_config()
        if not user_config.get("labels_search", False):
            self.original_dataset.logger.warning("Label search is not enabled for this dataset.")
            return self

        if isinstance(labels, str):
            labels = [labels]

        # Import here to avoid circular import
        from .dataset import SearchOperator

        if search_operator is None:
            search_operator = SearchOperator.IS_ONE_OF

        # Build the correct VQL structure for labels
        label_filter = {"labels": {"op": search_operator.value, "value": labels}}

        # Create new Searchable with accumulated filters
        new_vql_query = self.vql_query.copy()
        new_vql_query.append(label_filter)
        new_searchable = Searchable(self.original_dataset, new_vql_query)
        # Preserve the searchable_id
        new_searchable.searchable_id = self.searchable_id
        # Clear cached results for new query
        new_searchable._cached_results = None
        return new_searchable

    def search_by_captions(self, captions: Union[List[str], str], search_operator: "SearchOperator" = None) -> "Searchable":
        """
        Add caption search criteria to the current query.

        Args:
            captions: Caption(s) to search for
            search_operator: Search operator to use

        Returns:
            New Searchable with updated query
        """
        # Check if captions search is enabled in user config
        user_config = self.original_dataset._get_user_config()
        if not user_config.get("captions_search", False):
            self.original_dataset.logger.warning("Caption search is not enabled for this dataset.")
            return self

        if isinstance(captions, str):
            captions = [captions]

        # Import here to avoid circular import
        from .dataset import SearchOperator

        if search_operator is None:
            search_operator = SearchOperator.IS

        # Build the correct VQL structure for captions
        if search_operator == SearchOperator.IS_ONE_OF and len(captions) > 1:
            # For IS_ONE_OF with multiple captions, keep them as a list
            caption_filter = {"captions": {"op": search_operator.value, "value": captions}}
        else:
            # For other operators or single caption, combine into one search string
            combined_text = " ".join(captions)
            caption_filter = {"captions": {"op": search_operator.value, "value": combined_text}}

        # Create new Searchable with accumulated filters
        new_vql_query = self.vql_query.copy()
        new_vql_query.append(caption_filter)
        new_searchable = Searchable(self.original_dataset, new_vql_query)
        # Preserve the searchable_id
        new_searchable.searchable_id = self.searchable_id
        # Clear cached results for new query
        new_searchable._cached_results = None
        return new_searchable

    def search_by_issues(self, issue_type: Union["IssueType", List["IssueType"]], search_operator: "SearchOperator" = None, confidence_min: float = 0.8, confidence_max: float = 1.0) -> "Searchable":
        """
        Add issue search criteria to the current query.

        Args:
            issue_type: Issue type(s) to search for
            search_operator: Search operator to use
            confidence_min: Minimum confidence threshold
            confidence_max: Maximum confidence threshold

        Returns:
            New Searchable with updated query
        """
        if not issue_type:
            raise ValueError("issue_type must be provided")

        if not isinstance(issue_type, list):
            issue_type = [issue_type]

        # Import here to avoid circular import
        from .dataset import SearchOperator, ALLOWED_ISSUE_NAMES

        if search_operator is None:
            search_operator = SearchOperator.IS

        if isinstance(search_operator, str):
            try:
                search_operator = SearchOperator(search_operator)
            except ValueError:
                self.original_dataset.logger.warning(f"Invalid search_operator for issues: {search_operator}")
                return self

        # Validate issue types
        for it in issue_type:
            issue_type_str = it.value
            if issue_type_str not in ALLOWED_ISSUE_NAMES:
                self.original_dataset.logger.warning(f"Invalid issue type '{issue_type_str}'. Allowed types: {list(ALLOWED_ISSUE_NAMES)}")
                return self

        # Build the correct VQL structure for issues
        if len(issue_type) == 1:
            # Single issue type
            issue_filter = {"issues": {"op": search_operator.value, "value": issue_type[0].value, "confidence_min": confidence_min, "confidence_max": confidence_max, "mode": "in"}}
        else:
            # Multiple issue types - use single filter with array of values
            issue_values = [it.value for it in issue_type]
            issue_filter = {"issues": {"op": search_operator.value, "value": issue_values, "confidence_min": confidence_min, "confidence_max": confidence_max, "mode": "in"}}

        # Create new Searchable with accumulated filters
        new_vql_query = self.vql_query.copy()
        new_vql_query.append(issue_filter)
        new_searchable = Searchable(self.original_dataset, new_vql_query)
        # Preserve the searchable_id
        new_searchable.searchable_id = self.searchable_id
        # Clear cached results for new query
        new_searchable._cached_results = None
        return new_searchable

    def search_by_semantic(self, text: str, relevance: "SemanticRelevance" = None) -> "Searchable":
        """
        Add semantic search criteria to the current query.

        Args:
            text: Text to search for semantically
            relevance: Relevance level for semantic search

        Returns:
            New Searchable with updated query
        """
        # Check if semantic search is enabled in user config
        user_config = self.original_dataset._get_user_config()
        if not user_config.get("semantic_search", False):
            self.original_dataset.logger.warning("Semantic search is not enabled for this dataset.")
            return self

        if not text or not isinstance(text, str):
            raise ValueError("text must be a non-empty string")

        # Import here to avoid circular import
        from .dataset import SemanticRelevance

        if relevance is None:
            relevance = SemanticRelevance.MEDIUM_RELEVANCE

        # Build the correct VQL structure for semantic search
        semantic_filter = {"semantic": {"op": "semantic", "value": text, "relevance": relevance.value}}
        print(f"Semantic filter: {semantic_filter}")
        # Create new Searchable with accumulated filters
        new_vql_query = self.vql_query.copy()
        new_vql_query.append(semantic_filter)
        new_searchable = Searchable(self.original_dataset, new_vql_query)
        # Preserve the searchable_id
        new_searchable.searchable_id = self.searchable_id
        # Clear cached results for new query
        new_searchable._cached_results = None
        return new_searchable

    def search_by_visual_similarity(self, image_path: str, threshold: float = 0.8, search_operator: "SearchOperator" = None) -> "Searchable":
        """
        Add visual similarity search criteria to the current query.

        Args:
            image_path: Path to the reference image
            threshold: Similarity threshold between 0.0 and 1.0 (default: 0.8)
                      Lower values = more restrictive (fewer results)
                      Higher values = less restrictive (more results)
                      Recommended range: 0.2-0.8
            search_operator: Search operator to use

        Returns:
            New Searchable with updated query
        """
        # Validate threshold range
        if not isinstance(threshold, (int, float)) or threshold < 0.0 or threshold > 1.0:
            raise ValueError(f"threshold must be a float between 0.0 and 1.0, got {threshold}")

        # Warn for very restrictive thresholds that might return no results
        if threshold < 0.2:
            self.original_dataset.logger.warning(f"Very low threshold ({threshold}) may return no results. Consider using 0.2-0.8 for better results.")

        # Warn for very permissive thresholds that might cause performance issues
        if threshold > 0.9:
            self.original_dataset.logger.warning(f"Very high threshold ({threshold}) may cause connection timeouts. Consider using 0.2-0.8 for better performance.")

        # Import here to avoid circular import
        from .dataset import SearchOperator

        if search_operator is None:
            search_operator = SearchOperator.IS_ONE_OF

        if isinstance(search_operator, str):
            try:
                search_operator = SearchOperator(search_operator)
            except ValueError:
                self.original_dataset.logger.warning(f"Invalid search_operator for visual similarity: {search_operator}")
                return self

        if search_operator != SearchOperator.IS_ONE_OF:
            self.original_dataset.logger.warning(f"Search operator {search_operator} is not implemented for visual similarity.")
            return self

        # First upload the image to get media_id
        upload_result = self.original_dataset._search_by_image_file(image_path=image_path)
        media_id = upload_result.get("anchor_media_id")

        if not media_id:
            raise ValueError("Failed to get anchor_media_id from image upload")

        # Build the correct VQL structure for visual similarity
        # Visual similarity always uses "upload" operation, but we store the search operator for consistency
        similarity_filter = {"similarity": {"op": "upload", "value": media_id, "threshold": threshold, "search_operator": search_operator.value}}

        # Create new Searchable with accumulated filters
        new_vql_query = self.vql_query.copy()
        new_vql_query.append(similarity_filter)
        new_searchable = Searchable(self.original_dataset, new_vql_query)
        # Preserve the searchable_id
        new_searchable.searchable_id = self.searchable_id
        # Clear cached results for new query
        new_searchable._cached_results = None
        return new_searchable

    def count(self, entity_type: str = "IMAGES") -> int:
        """
        Get the count of results that satisfy the current query without constructing a DataFrame.
        This is more efficient than get_results().shape[0] for count-only queries.
        Count is cached after the first call for better performance.

        Args:
            entity_type: Entity type to search ("IMAGES" or "OBJECTS")

        Returns:
            int: Number of results that satisfy the query criteria
        """
        # If results are already cached, just return the length
        if self._cached_results is not None:
            return len(self._cached_results)

        # If no results cached, call get_results to cache them and return length
        results = self.get_results(entity_type)
        return len(results)

    def get_results(self, entity_type: str = "IMAGES") -> pd.DataFrame:
        """
        Execute the accumulated VQL query and return results.
        Results are cached after the first call for better performance.

        Args:
            entity_type: Entity type to search ("IMAGES" or "OBJECTS")

        Returns:
            DataFrame containing the search results
        """
        # Return cached results if available
        if self._cached_results is not None:
            return self._cached_results

        # Execute the query and cache results
        if not self.vql_query:
            # If no query has been built, return all images
            raw_results = self.original_dataset.export_to_dataframe()
        else:
            # Execute the VQL query using the new processing method
            raw_results = self.original_dataset._process_searchable_vql(self.vql_query, entity_type)

        # Cache the results
        self._cached_results = raw_results
        return raw_results

    # reset the results of eval. store datasframe after first call
    def reset(self) -> None:
        """
        Reset the query to empty (return to original dataset).
        This also clears any cached results.
        Modifies the current Searchable object in place.

        Returns:
            None
        """
        self.vql_query = []
        # Clear cached results
        self._cached_results = None

    def get_query(self) -> List[dict]:
        """
        Get the current VQL query.

        Returns:
            List of VQL query filters
        """
        return self.vql_query.copy()

    def __str__(self) -> str:
        """String representation showing the current query"""
        query_str = " + ".join([str(filter_obj) for filter_obj in self.vql_query]) if self.vql_query else "No filters"
        return f"Searchable(id='{self.searchable_id}', dataset_id='{self.dataset_id}', query=[{query_str}])"

    def __repr__(self) -> str:
        return self.__str__()


# Example usage and demonstration
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from .client import VisualLayerClient

    load_dotenv()

    # Initialize client
    API_KEY = os.getenv("VISUAL_LAYER_API_KEY")
    API_SECRET = os.getenv("VISUAL_LAYER_API_SECRET")

    if not API_KEY or not API_SECRET:
        print("❌ Error: VISUAL_LAYER_API_KEY and VISUAL_LAYER_API_SECRET must be set in environment variables")
        exit(1)

    client = VisualLayerClient(API_KEY, API_SECRET)

    # Get dataset
    dataset_id = "bc41491e-78ae-11ef-ba4b-8a774758b536"
    print(f"🔍 Testing search functionality with dataset: {dataset_id}")

    try:
        original_dataset = client.get_dataset_object(dataset_id)
        print(f"✅ Successfully connected to dataset: {original_dataset}")
    except Exception as e:
        print(f"❌ Error connecting to dataset: {e}")
        exit(1)

    print("\n" + "=" * 60)
    print("🧪 TESTING SEARCH FUNCTIONALITY")
    print("=" * 60)

    # Test 1: Basic label search
    print("\n1️⃣ Testing basic label search...")
    try:
        searchable = original_dataset.search_by_labels(["healthy"])
        results = searchable.get_results()
        print(f"✅ Label search (healthy): Found {len(results)} images")
        if len(results) > 0:
            print(f"   Sample labels: {results['image_labels'].iloc[0] if 'image_labels' in results.columns else 'N/A'}")
    except Exception as e:
        print(f"❌ Label search failed: {e}")

    # Test 2: Label search with multiple labels
    print("\n2️⃣ Testing label search with multiple labels...")
    try:
        searchable = original_dataset.search_by_labels(["healthy", "bean_rust", "angular_leaf_spot"])
        results = searchable.get_results()
        print(f"✅ Multi-label search: Found {len(results)} images")
    except Exception as e:
        print(f"❌ Multi-label search failed: {e}")

    # Test 3: Issue search
    print("\n3️⃣ Testing issue search...")
    try:
        searchable = original_dataset.search_by_issues([IssueType.OUTLIERS])
        results = searchable.get_results()
        print(f"✅ Issue search (outliers): Found {len(results)} images")
        if len(results) > 0:
            print(f"   Sample issues: {results['issues'].iloc[0] if 'issues' in results.columns else 'N/A'}")
    except Exception as e:
        print(f"❌ Issue search failed: {e}")

    # Test 4: Issue search with multiple issues
    print("\n4️⃣ Testing issue search with multiple issues...")
    try:
        searchable = original_dataset.search_by_issues([IssueType.OUTLIERS, IssueType.MISLABELS])
        results = searchable.get_results()
        print(f"✅ Multi-issue search: Found {len(results)} images")
    except Exception as e:
        print(f"❌ Multi-issue search failed: {e}")

    # Test 5: Caption search
    print("\n5️⃣ Testing caption search...")
    try:
        searchable = original_dataset.search_by_captions(["leaf", "plant"])
        results = searchable.get_results()
        print(f"✅ Caption search: Found {len(results)} images")
        if len(results) > 0:
            print(f"   Sample captions: {results['captions'].iloc[0] if 'captions' in results.columns else 'N/A'}")
    except Exception as e:
        print(f"❌ Caption search failed: {e}")

    # Test 6: Semantic search
    print("\n6️⃣ Testing semantic search...")
    try:
        searchable = original_dataset.search_by_semantic("healthy plant leaves")
        results = searchable.get_results()
        print(f"✅ Semantic search: Found {len(results)} images")
    except Exception as e:
        print(f"❌ Semantic search failed: {e}")

    # Test 7: Chaining - Labels + Issues
    print("\n7️⃣ Testing chaining: Labels + Issues...")
    try:
        searchable = original_dataset.search_by_labels(["healthy"])
        results = searchable.search_by_issues([IssueType.OUTLIERS]).get_results()
        print(f"✅ Chained search (healthy + outliers): Found {len(results)} images")
    except Exception as e:
        print(f"❌ Chained search failed: {e}")

    # Test 8: Chaining - Issues + Labels
    print("\n8️⃣ Testing chaining: Issues + Labels...")
    try:
        searchable = original_dataset.search_by_issues([IssueType.MISLABELS])
        results = searchable.search_by_labels(["bean_rust"]).get_results()
        print(f"✅ Chained search (mislabels + bean_rust): Found {len(results)} images")
    except Exception as e:
        print(f"❌ Chained search failed: {e}")

    # Test 9: Complex chaining
    print("\n9️⃣ Testing complex chaining...")
    try:
        searchable = original_dataset.search_by_labels(["healthy", "bean_rust"])
        results = searchable.search_by_issues([IssueType.OUTLIERS, IssueType.MISLABELS]).get_results()
        print(f"✅ Complex chained search: Found {len(results)} images")
    except Exception as e:
        print(f"❌ Complex chained search failed: {e}")

    # Test 10: Using Searchable constructor
    print("\n🔟 Testing Searchable constructor...")
    try:
        searchable = Searchable(original_dataset)
        results = searchable.search_by_labels(["angular_leaf_spot"]).search_by_issues([IssueType.OUTLIERS]).get_results()
        print(f"✅ Searchable constructor + chaining: Found {len(results)} images")
    except Exception as e:
        print(f"❌ Searchable constructor test failed: {e}")

    # Test 11: Reset functionality
    print("\n1️⃣1️⃣ Testing reset functionality...")
    try:
        searchable = Searchable(original_dataset)
        # Add some filters
        searchable = searchable.search_by_labels(["healthy"])
        # Reset
        searchable.reset()
        results = searchable.get_results()
        print(f"✅ Reset functionality: Found {len(results)} images (should be all images)")
    except Exception as e:
        print(f"❌ Reset functionality failed: {e}")

    # Test 12: Get query functionality
    print("\n1️⃣2️⃣ Testing get_query functionality...")
    try:
        searchable = original_dataset.search_by_labels(["healthy"])
        query = searchable.get_query()
        print(f"✅ Get query: {query}")
    except Exception as e:
        print(f"❌ Get query failed: {e}")

    # Test 13: String representation
    print("\n1️⃣3️⃣ Testing string representation...")
    try:
        searchable = original_dataset.search_by_labels(["healthy"])
        print(f"✅ String representation: {searchable}")
    except Exception as e:
        print(f"❌ String representation failed: {e}")

    # Test 14: Visual similarity (if image exists)
    print("\n1️⃣4️⃣ Testing visual similarity...")
    image_path = "./sample/dog.jpeg"
    if os.path.exists(image_path):
        try:
            searchable = original_dataset.search_by_visual_similarity(image_path, threshold=0.7)
            results = searchable.get_results()
            print(f"✅ Visual similarity search: Found {len(results)} images")
        except Exception as e:
            print(f"❌ Visual similarity search failed: {e}")
    else:
        print(f"⚠️  Skipping visual similarity test - image not found at {image_path}")

    # Test 15: Semantic + Issues chaining
    print("\n1️⃣5️⃣ Testing semantic + issues chaining...")
    try:
        searchable = original_dataset.search_by_semantic("diseased plant leaves")
        results = searchable.search_by_issues([IssueType.OUTLIERS]).get_results()
        print(f"✅ Semantic + issues chaining: Found {len(results)} images")
    except Exception as e:
        print(f"❌ Semantic + issues chaining failed: {e}")

    # Test 16: Caption + Issues chaining
    print("\n1️⃣6️⃣ Testing caption + issues chaining...")
    try:
        searchable = original_dataset.search_by_captions(["leaf", "green"])
        results = searchable.search_by_issues([IssueType.BLUR]).get_results()
        print(f"✅ Caption + issues chaining: Found {len(results)} images")
    except Exception as e:
        print(f"❌ Caption + issues chaining failed: {e}")

    # Test 17: Multiple chaining operations
    print("\n1️⃣7️⃣ Testing multiple chaining operations...")
    try:
        searchable = Searchable(original_dataset)
        results = searchable.search_by_labels(["healthy", "bean_rust"]).search_by_captions(["leaf"]).search_by_issues([IssueType.OUTLIERS]).get_results()
        print(f"✅ Multiple chaining: Found {len(results)} images")
    except Exception as e:
        print(f"❌ Multiple chaining failed: {e}")

    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)
