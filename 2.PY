from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# Load pre-trained models
embedder = SentenceTransformer('all-MiniLM-L6-v2')
qa_pipeline = pipeline("question-answering")

# Load dataset from text file
with open('cleaned_text.txt', 'r') as file:
    text = file.read()

# Split text into paragraphs or chunks
chunks = text.split('\n\n')  # Assumes paragraphs are separated by double newlines

# Create embeddings for chunks
chunk_embeddings = embedder.encode(chunks, convert_to_tensor=True)

def get_answer(question):
    # Create embedding for the question
    question_embedding = embedder.encode([question], convert_to_tensor=True)
    
    # Compute similarity scores between question and chunks
    similarities = util.pytorch_cos_sim(question_embedding, chunk_embeddings)[0]
    
    # Get the index of the most relevant chunk
    index = similarities.argmax()
    
    # Get the most relevant chunk
    relevant_chunk = chunks[index]
    
    # Use the QA pipeline to generate an answer from the relevant chunk
    result = qa_pipeline(question=question, context=relevant_chunk)
    
    return result['answer']

# Example usage
question = "Can you provide detailed information about the software engineering?"
answer = get_answer(question)
print(f"Question: {question}\nAnswer: {answer}")
