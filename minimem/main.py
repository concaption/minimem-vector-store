"""
path: minimem/main.py

A minimal in memory vector store for storing and retrieving vectors.
"""

import numpy as np


class MiniMemStore:
    """
    MinMemStore
    A minimal in memory vector store for storing and retrieving vectors.

    Attributes:
    ----------
    vector_data: dict
        a dictionary to store vectors
    vector_index: dict
        an indexing stucture for retrieval

    Methods:
    -------
    add_vector(vector_id, vector)
        add a vector to the store
    get_vector(vector_id)
        get a vector from the store
    get_most_similar(vector_id, num_results=1)
        get the most similar vectors to a vector in the store
    """

    def __init__(self):
        self.vector_data = {}  # a dictionary to store vectors
        self.vector_index = {}  # an indexing stucture for retrieval

    def add_vector(self, vector_id, vector):
        """
        Add a vector to the store.

        Parameters:
        ----------
        vector_id: str
            a unique identifier for the vector
        vector: numpy.ndarray
            a vector to be stored

        Returns:
        -------
        None
        """
        self.vector_data[vector_id] = vector
        self._update_index(vector_id, vector)

    def get_vector(self, vector_id):
        """
        Get a vector from the store.

        Parameters:
        ----------
        vector_id: str
            a unique identifier for the vector

        Returns:
        -------
        numpy.ndarray
            the vector corresponding to vector_id
        """
        return self.vector_data.get(vector_id)

    def _update_index(self, vector_id, vector):
        """
        Update the index with a new vector.

        Parameters:
        ----------
        vector_id: str
            a unique identifier for the vector
        vector: numpy.ndarray
            a vector to be stored

        Returns:
        -------
        None

        Notes:
        -----
        The index is a dictionary of dictionaries. The outer dictionary
        is keyed by vector_id and the inner dictionary is keyed by
        similar_vector_id. The value of the inner dictionary is the
        similarity between the two vectors.
        """
        for existing_id, existing_vector in self.vector_data.items():
            similarity = np.dot(vector, existing_vector) / (
                np.linalg.norm(vector) * np.linalg.norm(existing_vector)
            )
            if existing_id not in self.vector_index:
                self.vector_index[existing_id] = {}
            self.vector_index[existing_id][vector_id] = similarity

    def get_most_similar(self, query_vector, num_results=1):
        """
        Get the most similar vectors to a vector in the store.

        Parameters:
        ----------
        query_vector: numpy.ndarray
            the vector to compare against
        num_results: int
            the number of results to return

        Returns:
        -------
        list
            a list of tuples of the form (similar_vector_id, similarity)

        Notes:
        -----
        The list is sorted by similarity in descending order.
        """
        results = []
        for vector_id, vector in self.vector_data.items():
            similarity = np.dot(query_vector, vector) / (
                np.linalg.norm(query_vector) * np.linalg.norm(vector)
            )
            results.append((vector_id, similarity))

        # Sort by similarity in descending order
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:num_results]


# Query: apple is best for health
# Similar sentences:
#         fruit is good for health: Similarity: 0.6708
#         apple is my favorite fruit: Similarity: 0.4472
#         I eat an apple: Similarity: 0.2500
