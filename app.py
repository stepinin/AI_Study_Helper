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
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        print("FULL ERROR:", e)
        return "❌ Ошибка ИИ"
    
    
@app.route("/" or "/home") 
def home():
    return render_template("index.html")
    topic = request.json.get("topic", "")
    answer = ask_ai(f"{topic}")
    return jsonify({"answer": answer})

@app.route("/explain", methods=["POST"])
def explain():
    topic = request.json.get("topic", "")
    answer = ask_ai(f"Объясни простым языком: {topic}")
    return jsonify({"answer": answer})


@app.route("/test", methods=["POST"])
def test():
    topic = request.json.get("topic", "")

    prompt = f"""
Сделай 3 коротких тестовых вопроса по теме: {topic}

Формат:
Вопрос
A)
B)
C)
D)
Ответ: X
"""

    text = ask_ai(prompt)
    print(text)
    questions = []
    answers = []

    blocks = text.split("Вопрос")

    for block in blocks:
        if not block.strip():
            continue

        full = "Вопрос" + block

        correct = "A"
        lines = full.split("\n")

        clean = []
        for line in lines:
            if "Ответ" in line:
                correct = line.split(":")[-1].strip()
            else:
                clean.append(line)
        questions.append("\n".join(clean))
        answers.append(correct)
    if '1' not in questions[0]:
        questions.pop(0)
    return jsonify({
        "questions": questions,
        "answers": answers
    })
except Exception as e:
    print("TEST ERROR:", e)
    return jsonify({"questions": ["❌ Ошибка генерации теста"]})
if __name__ == "__main__":
    app.run()
