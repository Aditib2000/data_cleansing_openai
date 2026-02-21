import mysql.connector, json, os
from openai import OpenAI
from datetime import datetime

def finalize_import(file_id):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    content = client.files.content(file_id).text
    
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"), 
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASS"), 
        database=os.getenv("DB_NAME")
    )
    cursor = db.cursor()
    
    data_to_load = []
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for line in content.strip().split('\n'):
        if not line: continue
        res = json.loads(line)
        row_id = res['custom_id'].split('-')[1]
        
        if res['response']['status_code'] == 200:
            clean_text = res['response']['body']['choices'][0]['message']['content'].strip()
            data_to_load.append((row_id, clean_text, now))

    if data_to_load:
        try:
            # 1. Create a lightning-fast temporary table in memory
            cursor.execute("CREATE TEMPORARY TABLE temp_updates (id INT PRIMARY KEY, desc_clean TEXT, p_at DATETIME)")

            # 2. Bulk insert results into the temp table
            insert_sql = "INSERT INTO temp_updates (id, desc_clean, p_at) VALUES (%s, %s, %s)"
            cursor.executemany(insert_sql, data_to_load)

            update_sql = """
                UPDATE updated_business b
                JOIN temp_updates t ON b.id = t.id
                SET b.description_clean = t.desc_clean,
                    b.is_processed = 1,
                    b.processed_at = t.p_at
            """
            cursor.execute(update_sql)
            
            db.commit()
            print(f"High-Speed Import Complete: {len(data_to_load)} rows.")
            
        except Exception as e:
            db.rollback()
            print(f"SQL Error: {e}")
        finally:
            cursor.execute("DROP TEMPORARY TABLE IF EXISTS temp_updates")
            cursor.close()
            db.close()

    return len(data_to_load)