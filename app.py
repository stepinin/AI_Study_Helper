from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("API_KEY")
)

def ask_ai(prompt):
    try:
        res = client.chat.completions.create(
            model="deepseek-ai/deepseek-v3.2",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return res.choices[0].message.content
    except Exception as e:
        print("FULL ERROR:", e)
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
