from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator

app = Flask(__name__)


@app.route("/", methods=["POST"])
def main():
    data = request.json
    response = handle_request(data)
    return jsonify(response)


def handle_request(request_data):
    session = request_data["session"]
    user_input = request_data["request"]["original_utterance"].lower().strip()

    if session["new"] or not user_input:
        return build_response("Привет! Я могу перевести слово. Скажите: 'Переведи слово *слово*'.", session)

    if "переведи слово" in user_input:
        word_to_translate = user_input.replace("переведи слово", "").strip()

        if not word_to_translate:
            return build_response("Пожалуйста, укажите слово для перевода.", session)

        translated = translate_word(word_to_translate)
        if translated:
            return build_response(translated, session)
        else:
            return build_response("Не удалось перевести слово.", session)

    return build_response("Я могу перевести слово. Скажите: 'Переведи слово *слово*'.", session)


def build_response(text, session):
    return {
        "response": {
            "text": text,
            "tts": text,
            "end_session": False
        },
        "session": {
            "session_id": session["session_id"],
            "message_id": session["message_id"],
            "user_id": session["user"]["user_id"]
        },
        "version": "1.0"
    }


def translate_word(word):
    try:
        return GoogleTranslator(source='ru', target='en').translate(word)
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return None


if __name__ == "__main__":
    app.run(debug=True)
