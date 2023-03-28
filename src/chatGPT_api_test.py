import openai


class APITest:
    def __init__(self, system_background):
        self.system_background = system_background

    openai.api_key = "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"

    def query(self, face_expression):
        print(face_expression)
        messages = [{"role": "system", "content": self.system_background.format(face_expression)}]
        # begin_sentence = 'Currently I am {}. '.format(face_expression)
        content = input("User: ")
        # messages.append({"role": "user", "content": begin_sentence})
        messages.append({"role": "user", "content": content})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            # n=2
        )

        chat_response = completion.choices[0].message.content
        print(f'ChatGPT: {chat_response}')
        messages.append({"role": "assistant", "content": chat_response})


if __name__ == "__main__":
    system_background = "You’re a robot who's name is Naoqi, you should serve the me according to the my emotion " \
                        "mood. My mood is currently {}. "
    api_test = APITest(system_background)
    while True:
        face_expression = 'sad'
        api_test.query(face_expression)
