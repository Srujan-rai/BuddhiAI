from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# Load pre-trained sentence transformer model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load dataset from text file
with open('cleaned_text.txt', 'r') as file:
    documents = file.readlines()

# Create embeddings for documents
document_embeddings = embedder.encode(documents, convert_to_tensor=True)

# Load pre-trained generative QA model
qa_pipeline = pipeline("question-answering")

def get_answer(question):
    # Create embedding for the question
    question_embedding = embedder.encode([question], convert_to_tensor=True)
    
    # Compute similarity scores
    similarities = util.pytorch_cos_sim(question_embedding, document_embeddings)[0]
    
    # Get the index of the most relevant document
    index = similarities.argmax()
    
    # Get the most relevant document
    relevant_document = documents[index].strip()
    
    # Use the QA pipeline to generate an answer from the relevant document
    result = qa_pipeline(question=question, context=relevant_document)
    
    return result['answer']

# Example usage
question = "Prepare SQA plan for the project."
answer = get_answer(question)
print(f"Question: {question}\nAnswer: {answer}")
