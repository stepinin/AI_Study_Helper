from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("API_KEY"),
    default_headers={
        "HTTP-Referer": "http://localhost:5000", 
        "X-OpenRouter-Title": "AI Study Helper"
    }
)

response = client.chat.completions.create(
    model="openrouter/elephant-alpha",
    messages=[
        {"role": "user", "content": "What is the meaning of life?"}
    ],
    max_tokens=300
)

print(response.choices[0].message.content)

def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="openrouter/elephant-alpha",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return "❌ Ошибка ИИ"
      
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/explain", methods=["POST"])
def explain():
    topic = request.json.get("topic", "")
    answer = ask_ai(f"Объясни простым языком: {topic}")
    return jsonify({"answer": answer})

@app.route("/test", methods=["POST"])
def test():

    try:
        topic = request.json.get("topic", "")

        prompt = f"""
Сделай 3 коротких тестовых вопроса по теме: {topic}

Формат:
Вопрос 1
A)
B)
C)
D)
Ответ: X
"""

        text = ask_ai(prompt)

        questions = []
        answers = []

        blocks = text.split("Вопрос")

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            full = "Вопрос " + block

            correct = "A"
            clean = []

            for line in full.split("\n"):
                if "Ответ" in line:
                    correct = line.split(":")[-1].strip()
                else:
                    clean.append(line)

            q = "\n".join(clean).strip()

            if len(q) > 10:
                questions.append(q)
                answers.append(correct)

        return jsonify({
            "questions": questions,
            "answers": answers
        })

    except Exception as e:
        print("TEST ERROR:", e)
        return jsonify({
            "questions": ["❌ Ошибка генерации"],
            "answers": []
        })
        
if __name__ == "__main__":
    app.run(debug=True)
