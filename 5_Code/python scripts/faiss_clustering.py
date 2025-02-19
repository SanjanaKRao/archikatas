
# FAISS K-Means groups answers based on semantic similarity.
import faiss

def cluster_similar_answers(answers, num_clusters=10):
    """
    Clusters similar answers using FAISS K-Means.
    """
    embeddings = generate_embeddings(answers)
    dimension = embeddings.shape[1]

    # Initialize FAISS K-Means clustering
    kmeans = faiss.Kmeans(dimension, num_clusters, niter=10, verbose=False)
    kmeans.train(embeddings)
    _, cluster_ids = kmeans.index.search(embeddings, 1)

    # Organize answers into clusters
    clustered_answers = {}
    for idx, cluster_id in enumerate(cluster_ids.flatten()):
        if cluster_id not in clustered_answers:
            clustered_answers[cluster_id] = []
        clustered_answers[cluster_id].append(answers[idx])

    return clustered_answers
