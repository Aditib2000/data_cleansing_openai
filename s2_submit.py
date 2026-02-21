from openai import OpenAI
import os

def submit_batch():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.path.exists("batch_input.jsonl"): return None

    batch_file = client.files.create(file=open("batch_input.jsonl", "rb"), purpose="batch")
    
    batch_job = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    return batch_job.id