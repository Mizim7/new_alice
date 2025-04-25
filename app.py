from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)

# Инициализация переводчика
translator = Translator()


@app.route("/", methods=["POST"])
def main():
    # Получаем данные из запроса
    data = request.json

    # Обработка запроса
    response = handle_request(data)

    # Возвращаем ответ в формате JSON
    return jsonify(response)


def handle_request(request):
    # Получаем текст запроса пользователя
    user_input = request["request"]["original_utterance"].lower()

    # Проверяем, содержит ли запрос фразу "переведи слово"
    if "переведи слово" in user_input:
        # Извлекаем слово для перевода
        word_to_translate = user_input.replace("переведи слово", "").strip()

        if not word_to_translate:
            response_text = "Пожалуйста, укажите слово для перевода."
        else:
            # Переводим слово
            translated_word = translate_word(word_to_translate)
            response_text = translated_word or "Не удалось перевести слово."
    else:
        response_text = "Я могу перевести слово. Скажите: 'Переведи слово *слово*'."

    response = {
        "response": {
            "text": response_text,
            "tts": response_text,
            "end_session": False
        },
        "session": {
            "session_id": request["session"]["session_id"],
            "message_id": request["session"]["message_id"],
            "user_id": request["session"]["user"]["user_id"]
        },
        "version": "1.0"
    }

    return response


def translate_word(word):
    try:
        # Переводим слово на английский язык
        translation = translator.translate(word, src="ru", dest="en")
        return translation.text
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return None


if __name__ == "__main__":
    app.run(debug=True)