import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"


def analyze_candidate_score(candidate_text):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n" \
             f"Ты эксперт программы inVision U. Оцени кандидата: '{candidate_text}'. " \
             f"Напиши один короткий совет и балл от 0.1 до 0.9. " \
             f"Формат строго: SCORE: [число] | ADVICE: [текст]<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"

    # Добавили "wait_for_model": True — это КЛЮЧЕВОЙ момент
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 100, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }

    try:
        # Увеличили таймаут до 60 секунд, чтобы точно дождаться
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()
            full_text = result[0]['generated_text']
            ai_answer = full_text.split("assistant")[-1].strip()

            if "SCORE:" in ai_answer and "ADVICE:" in ai_answer:
                score_str = ai_answer.split("SCORE:")[1].split("|")[0].strip()
                advice = ai_answer.split("ADVICE:")[1].strip()
                return float(score_str), advice
            else:
                return 0.45, ai_answer[:150]

        return 0.35, "ИИ анализирует... Попробуй отправить сообщение еще раз через 10 секунд."
    except Exception as e:
        print(f"Ошибка: {e}")
        return 0.35, "Хорошее начало! Попробуй описать свой опыт подробнее."