# -*- coding: utf-8 -*-
# Code written in co-authorship with Claude Sonnet 4

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')

class ArticleDuplicateDetector:
    def __init__(self, similarity_threshold: float = 0.8):
        """
        Initialize the duplicate detector.
        
        Args:
            similarity_threshold: Threshold above which articles are considered duplicates
        """
        self.similarity_threshold = similarity_threshold
        self.vectorizer = None
        self.tfidf_matrix = None
        self.processed_data = None
        
    def preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess text for better similarity calculation.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Cleaned text
        """
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common stop words manually (basic set)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        words = text.split()
        text = ' '.join([word for word in words if word not in stop_words and len(word) > 2])
        
        return text.strip()
    
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare the dataset by combining title and abstract and preprocessing.
        
        Args:
            df: DataFrame with 'Covidence #', 'Title', and 'Abstract' columns
            
        Returns:
            DataFrame with processed text
        """
        # Create a copy to avoid modifying original data
        processed_df = df.copy()
        
        # Handle missing values
        processed_df['Title'] = processed_df['Title'].fillna('')
        processed_df['Abstract'] = processed_df['Abstract'].fillna('')
        
        # Combine title and abstract
        processed_df['combined_text'] = processed_df['Title'] + ' ' + processed_df['Abstract']
        
        # Preprocess the combined text
        processed_df['processed_text'] = processed_df['combined_text'].apply(self.preprocess_text)
        
        # Remove rows with empty processed text
        processed_df = processed_df[processed_df['processed_text'].str.len() > 0]
        
        self.processed_data = processed_df
        return processed_df
    
    def calculate_similarities(self, df: pd.DataFrame) -> np.ndarray:
        """
        Calculate cosine similarities between all articles.
        
        Args:
            df: Processed DataFrame
            
        Returns:
            Cosine similarity matrix
        """
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),  # Use unigrams and bigrams
            min_df=2,  # Ignore terms that appear in less than 2 documents
            max_df=0.95  # Ignore terms that appear in more than 95% of documents
        )
        
        # Fit and transform the text data
        self.tfidf_matrix = self.vectorizer.fit_transform(df['processed_text'])
        
        # Calculate cosine similarities
        similarity_matrix = cosine_similarity(self.tfidf_matrix)
        
        return similarity_matrix
    
    def find_duplicates(self, similarity_matrix: np.ndarray) -> List[Tuple]:
        """
        Find potential duplicate pairs based on similarity threshold.
        
        Args:
            similarity_matrix: Cosine similarity matrix
            
        Returns:
            List of tuples containing duplicate pairs and their similarity scores
        """
        duplicates = []
        n = similarity_matrix.shape[0]
        
        # Check upper triangle of similarity matrix (avoid duplicates)
        for i in range(n):
            for j in range(i + 1, n):
                if similarity_matrix[i, j] >= self.similarity_threshold:
                    duplicates.append((i, j, similarity_matrix[i, j]))
        
        return duplicates
    
    def generate_duplicate_report(self, duplicates: List[Tuple]) -> pd.DataFrame:
        """
        Generate a detailed report of duplicate pairs.
        
        Args:
            duplicates: List of duplicate pairs with similarity scores
            
        Returns:
            DataFrame with duplicate pair details
        """
        if not duplicates:
            return pd.DataFrame(columns=['Covidence_1', 'Title_1', 'Covidence_2', 'Title_2', 'Similarity_Score'])
        
        report_data = []
        for i, j, score in duplicates:
            row1 = self.processed_data.iloc[i]
            row2 = self.processed_data.iloc[j]
            
            report_data.append({
                'Covidence_1': row1['Covidence #'],
                'Title_1': row1['Title'],
                'Covidence_2': row2['Covidence #'],
                'Title_2': row2['Title'],
                'Similarity_Score': round(score, 4)
            })
        
        return pd.DataFrame(report_data)
    
    def detect_duplicates(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Main method to detect duplicates in the dataset.
        
        Args:
            df: Input DataFrame with 'Covidence #', 'Title', and 'Abstract' columns
            
        Returns:
            Tuple of (duplicate_report_df, similarity_matrix)
        """
        print("Preprocessing data...")
        processed_df = self.prepare_data(df)
        print(f"Processed {len(processed_df)} articles")
        
        print("Calculating cosine similarities...")
        similarity_matrix = self.calculate_similarities(processed_df)
        
        print("Finding duplicates...")
        duplicates = self.find_duplicates(similarity_matrix)
        
        print(f"Found {len(duplicates)} potential duplicate pairs")
        
        duplicate_report = self.generate_duplicate_report(duplicates)
        
        return duplicate_report, similarity_matrix


# Load your dataset
df = pd.read_csv('review_581959_screen_csv_20250718174203.csv')
df = df[['Title', 'Abstract', 'Covidence #']]
 
# Initialize detector with similarity threshold
detector = ArticleDuplicateDetector(similarity_threshold=0.7)
    
# Detect duplicates
duplicate_report, similarity_matrix = detector.detect_duplicates(df)
    
# Save results
duplicate_report.to_csv('duplicate_report.csv', index=False)
