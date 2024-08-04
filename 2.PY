import torch
from transformers import BertTokenizer, BertForQuestionAnswering
from datasets import load_dataset

# Load the tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

def split_text(text, max_length=512):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        new_chunk = current_chunk + sentence + '. '
        if len(tokenizer.encode(new_chunk, truncation=False)) <= max_length:
            current_chunk = new_chunk
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def answer_question(question, context):
    # Split context if it's too long
    chunks = split_text(context)
    answers = []

    for chunk in chunks:
        inputs = tokenizer.encode_plus(question, chunk, return_tensors='pt', truncation=True, max_length=512)
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']

        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits

        start_index = torch.argmax(start_logits)
        end_index = torch.argmax(end_logits) + 1

        answer_tokens = input_ids[0][start_index:end_index]
        answer = tokenizer.decode(answer_tokens)

        answers.append(answer)

    # Optionally, you can implement a more sophisticated merging strategy for answers
    return answers

def main():
    # Example question and context
    question = "What is the capital of France?"
    context = "Paris is the capital of France. It is known for its art, fashion, and culture. The city is situated on the Seine River."

    # Get the answer
    answers = answer_question(question, context)
    print("Answers:", answers)

if __name__ == "__main__":
    main()
