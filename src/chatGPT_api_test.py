import openai
import random


class APITest:
    def __init__(self):
        self.system_background = "You’re a robot who's name is Naoqi, you should serve the me according to the my " \
                                 "emotion mood. My mood is currently {}. Also you do not need to mention what mood I " \
                                 "am "
        self.system_message = {"role": "system", "content": self.system_background}
        self.logit_bias = {
            1073: 10
        }
        self.messages = [self.system_message]

    openai.api_key = "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"

    def query(self, mood, content):
        print(f'Detecting mood: {mood}')
        print(f'User: {content}')
        self.system_message = {"role": "system", "content": self.system_background.format(mood)}
        self.messages[0] = self.system_message
        self.messages.append({"role": "user", "content": content})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            max_tokens=200,
            temperature=0.0,  # random degree
            logit_bias=self.logit_bias,
            # n=2
        )

        chat_response = completion.choices[0].message.content
        print(f'ChatGPT: {chat_response}')
        self.messages.append({"role": "assistant", "content": chat_response})


if __name__ == "__main__":
    api_test = APITest()
    mood_list = ['anger', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
    while True:
        # user_mood = random.choice(mood_list)
        user_mood = 'sad'
        user_content = input('input: ')
        api_test.query(user_mood, user_content)
        # break
