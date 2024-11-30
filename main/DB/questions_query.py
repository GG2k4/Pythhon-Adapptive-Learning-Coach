from dotenv import load_dotenv  
import os
import faiss
import numpy as np
import json
# from sentence_transformers import SentenceTransformer

# load_dotenv()
# faiss_index_path = os.getenv("FAISS_INDEX_PATH")
# metadata_path = os.getenv("METADATA_PATH")

faiss_index_path = "main/DB/questions_vector_database4.index"
metadata_path = "main/DB/questions_metadata4.json"

index = faiss.read_index(faiss_index_path)
with open(metadata_path, "r") as meta_file:
    metadata = json.load(meta_file)

embedding_dim = 384
custom_dim = 115
total_dim = embedding_dim + custom_dim

topics_dimensions = {
    "String Manipulation": 0,
    "Vectorization": 1,
    "Attributes": 2,
    "Queues": 3,
    "Comprehension": 4,
    "HTTP": 5,
    "Primes": 6,
    "Loops": 7,
    "Error Handling": 8,
    "String Slicing": 9,
    "String": 10,
    "HTML Parsing": 11,
    "Python Libraries": 12,
    "Type Conversion": 13,
    "Flask": 14,
    "Strings": 15,
    "Formatting": 16,
    "Sets": 17,
    "Syntax": 18,
    "Arrays": 19,
    "Control Flow": 20,
    "Pandas": 21,
    "Linear Algebra": 22,
    "Numbers": 23,
    "Matrix Operations": 24,
    "Computational Complexity": 25,
    "JSON Handling": 26,
    "Python-specific Techniques": 27,
    "Vectors": 28,
    "Command Line Arguments": 29,
    "Trees": 30,
    "Tuple": 31,
    "Linear Regression": 32,
    "Algorithms": 33,
    "Slicing": 34,
    "Scikit-learn": 35,
    "Connection": 36,
    "Operators": 37,
    "Arithmetic": 38,
    "Lambda Expressions": 39,
    "Sorting": 40,
    "Serialization": 41,
    "Databases": 42,
    "NLTK": 43,
    "Boolean Logic": 44,
    "Zip": 45,
    "Dictionaries": 46,
    "Range": 47,
    "Plotting": 48,
    "SSH": 49,
    "Conditionals": 50,
    "Binary": 51,
    "Assignment": 52,
    "Filtering": 53,
    "Text Processing": 54,
    "Counting": 55,
    "Integer": 56,
    "Functions": 57,
    "Input": 58,
    "__str__": 59,
    "Int": 60,
    "Indexing": 61,
    "Profiling": 62,
    "Base64 Encoding/Decoding": 63,
    "Variables": 64,
    "Randomization": 65,
    "Min Function": 66,
    "Lambda": 67,
    "API Interaction": 68,
    "Time/Dates": 69,
    "Regex": 70,
    "Nodes": 71,
    "OOP": 72,
    "Map": 73,
    "Visualization": 74,
    "__init__": 75,
    "Regular Expressions": 76,
    "Tree Traversal": 77,
    "Stacks": 78,
    "Heaps": 79,
    "Data Handling": 80,
    "Machine Learning": 81,
    "Methods": 82,
    "Iteration": 83,
    "Parsing": 84,
    "HTML": 85,
    "Length": 86,
    "Sentiment Analysis": 87,
    "Recursion": 88,
    "Data Structures": 89,
    "Summation": 90,
    "Swapping": 91,
    "Libraries": 92,
    "SQL": 93,
    "Lists": 94,
    "Concurrency": 95,
    "Tuples": 96,
    "Math": 97,
    "Bit Manipulation": 98,
    "NumPy": 99,
    "Validation": 100,
    "Sockets": 101,
    "Import Statements": 102,
    "Python": 103,
    "GroupBy": 104,
    "Printing": 105,
    "Dynamic Programming": 106,
    "Yield": 107,
    "JSON": 108,
    "Dates/Times": 109,
    "Copy": 110,
    "Update": 111,
    "Web Scraping": 112,
    "Input/Output": 113,
    "Lambda Functions": 114
}

def normalize(vec:np.array):
    return vec / np.linalg.norm(vec) if np.linalg.norm(vec) > 0 else vec

def create_topic_vector(topic_weights: dict):
    topic_vector = np.zeros(len(topics_dimensions))
    for topic, weight in topic_weights.items():
        if topic in topics_dimensions:
            topic_vector[topics_dimensions[topic]] = weight
    return topic_vector

def getQuestion(query_weights_vector):
    query_weights_vector = np.array(query_weights_vector)
    zeros = np.zeros(embedding_dim)
    query_weights_vector = np.concatenate((zeros, query_weights_vector)).reshape(1, -1)
    # normalized_query = normalize(query_weights_vector)
    k = 1  # Number of closest neighbors to retrieve
    distances, indices = index.search(query_weights_vector, k)

    retrieved_vector = index.reconstruct(int(indices[0][0]))[384:]
    question = metadata[indices[0][0]]["question"]
    topics = metadata[indices[0][0]]["topics"]
    return retrieved_vector, question, topics

def getQuestionByTopic(topic_weights: dict):
    query_weights_vector = create_topic_vector(topic_weights, topics_dimensions)
    return getQuestion(query_weights_vector)


# def add_question_to_db(question_text, topic_weights, index, topics_dimensions, metadata=None, metadata_path=metadata_path, model=None, embedding_dim=384):
#     """
#     Adds a new question to the FAISS vector database.
    
#     Args:
#         question_text (str): The text of the question.
#         topic_weights (dict): A dictionary of topic weights for the question.
#         index (faiss.IndexFlatL2): The FAISS index to add the embedding to.
#         topics_dimensions (dict): Mapping of topics to their respective dimensions.
#         metadata (list, optional): The metadata list where question info is stored.
#         metadata_path (str, optional): File path to load/save metadata if not provided. Default is "metadata.json".
#         model (SentenceTransformer, optional): Preloaded sentence transformer model for encoding.
#         embedding_dim (int): The base embedding dimension (default is 384 for 'all-MiniLM-L6-v2').
#     """
#     if metadata is None:
#         try:
#             with open(metadata_path, "r") as meta_file:
#                 metadata = json.load(meta_file)
#         except FileNotFoundError:
#             metadata = []

#     if model is None:
#         model = SentenceTransformer("all-MiniLM-L6-v2")
    
#     question_embedding = model.encode(question_text)
    
#     topic_vector = np.zeros(len(topics_dimensions))
#     for topic, weight in topic_weights.items():
#         if topic in topics_dimensions:
#             topic_vector[topics_dimensions[topic]] = weight
    
#     combined_embedding = np.concatenate((question_embedding, topic_vector))
#     combined_embedding = combined_embedding / np.linalg.norm(combined_embedding) if np.linalg.norm(combined_embedding) > 0 else combined_embedding
    
#     index.add(np.array([combined_embedding], dtype=np.float32))
    
#     metadata.append({"question": question_text, "topics": topic_weights})
    
#     with open(metadata_path, "w") as meta_file:
#         json.dump(metadata, meta_file, indent=4)
