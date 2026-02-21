from openai import OpenAI
import os

def check_status(job_id):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    batch = client.batches.retrieve(job_id)
    return {
        "status": batch.status,
        "output_file_id": batch.output_file_id,
        "completed": batch.request_counts.completed,
        "total": batch.request_counts.total
    }