# Retrieve TOP 3-5 similar answers

def retrieve_similar_answers(candidate_answer, top_k=3):
    """
    Retrieves top K similar past expert-graded answers using FAISS.
    """
    # Convert candidate's answer to vector
    candidate_embedding = embedding_model.encode(candidate_answer).reshape(1, -1)
    
    # Search for top_k similar expert-graded answers
    distances, indices = faiss_index.search(candidate_embedding, top_k)

    # Retrieve metadata (graded answers, scores, feedback)
    similar_responses = []
    for idx in indices[0]:  # indices is a list of lists
        similar_responses.append(graded_answers_metadata[idx])

    return similar_responses
