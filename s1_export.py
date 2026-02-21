import mysql.connector, json, os, re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def pre_clean(text, char_limit=1000):
    if not text: return ""
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:char_limit]

def generate_tasks(limit=5000):
    filename = "batch_input.jsonl"
    db = mysql.connector.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"), database=os.getenv("DB_NAME"))
    cursor = db.cursor(dictionary=True)
    
   
    query = """
        SELECT id, 
               COALESCE(category, 'General Business') as category, 
               COALESCE(business_name, 'Business') as business_name, 
               COALESCE(description, '') as description 
        FROM updated_business WHERE is_processed = 0 ORDER BY id ASC LIMIT %s
    """
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    
    if not rows:
        db.close()
        return False

    with open(filename, "w", encoding="utf-8") as f:
        for row in rows:
            user_input = f"Business Name: {row['business_name']}\nCategory: {row['category']}\nOriginal Description: {pre_clean(row['description'])}"
            task = {
                "custom_id": f"row-{row['id']}", 
                "method": "POST", 
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o-mini", 
                    "messages": [
                        {"role": "system", "content": (
                            "Rephrase the description to be professional and clear. "
                            "If any phone numbers exist, include them in the description. Do not create or guess phone numbers, and do not mention contacting by phone unless a real phone number is available."
                            "Regenerate based on Category and Business Name if source is junk. "
                            "Remove ads, repetition, junk, emojis, and URLs. "
                            "Use 1-2 concise sentences."
                            "Simply provide the cleaned description without any additional commentary."
                            "Don't include category or business name explicitly in the description."
                            "Use any relevant information from the original description, but ensure it is well-written and professional like Phone number , business hours etc. But do not say 'is currently closed'.\n\n"
                        )},
                        {"role": "user", "content": user_input}
                    ], 
                    "max_tokens": 150
                }
            }
            f.write(json.dumps(task) + "\n")
    
    db.close()
    return True