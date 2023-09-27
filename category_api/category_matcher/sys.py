import difflib
import spacy
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class CategoryMatcher:
    def __init__(self, data_path, nlp_model):
        self.data = self._load_data(data_path)
        self.nlp = spacy.load(nlp_model)
        self.category_vectors = self._compute_category_vectors()

    def _load_data(self, path):
        df = pd.read_csv(path)
        data = {}
        for _, row in df.iterrows():
            data[row['Category']] = row['Keywords'].split(", ")
        return data

    def _compute_category_vectors(self):
        category_vectors = {}
        for category, keywords in self.data.items():
            vectors = [self.nlp(keyword).vector for keyword in keywords]
            avg_vector = np.mean(vectors, axis=0)
            category_vectors[category] = avg_vector
        return category_vectors

    def get_category_by_keyword(self, keyword):
        for category, keywords in self.data.items():
            if keyword in keywords:
                return category
            close_matches = difflib.get_close_matches(keyword, keywords, n=1, cutoff=0.8)
            if close_matches:
                return category
        return None

    def get_semantic_category(self, search_term):
        search_vector = self.nlp(search_term).vector.reshape(1, -1)
        similarities = {}
        for category, avg_vector in self.category_vectors.items():
            sim = cosine_similarity(search_vector, avg_vector.reshape(1, -1))
            similarities[category] = sim[0][0]
        return max(similarities, key=similarities.get)

    def get_category_for_search_query(self, query):
        category = self.get_category_by_keyword(query)
        if category:
            return category
        return self.get_semantic_category(query) or "Not Found"


if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    matcher = CategoryMatcher(data_path='data.csv', nlp_model="en_core_web_md")
    result_category = matcher.get_category_for_search_query(search_query)
    print(f"Category: {result_category}")



