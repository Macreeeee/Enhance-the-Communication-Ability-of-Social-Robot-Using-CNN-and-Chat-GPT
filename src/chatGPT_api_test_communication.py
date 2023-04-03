import openai
import random


class APITest:
    def __init__(self):
        self.system_background = "You’re a robot who's name is Naoqi. If I ask for any help, ou should then answer me " \
                                 "according to my " \
                                 "emotion mood.  You should also give a " \
                                 "behavior as body gesture like 'my body gesture is bowing'. "
        self.system_message = {"role": "system", "content": self.system_background}
        self.logit_bias = {
            1073: 10
        }
        self.messages = [self.system_message]
        self.known_person = {}
        self.last_face = {}
        self.last_name = ''

    openai.api_key = "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"

    def communication(self):
        face = self.get_face()

        # Exit the programe and check log. Delete in the future.
        if face == {'e'}:
            print(self.messages)
            exit()

        print(f'[detect face: {face}]')
        if face != self.last_face:
            self.match_known_person(face)
        else:
            print(f'[No new person appears]')
        content = self.detect_voice()
        if content:
            emotion = self.get_emotion(face)
            self.query(self.last_name, emotion, content)

    def detect_voice(self):
        # Detect human voice by Naoqi. Turn voice into content.
        content = input('-->Input a content: ')
        if content:
            return content
        else:
            return False

    def query(self, name, mood, content):

        print(f'[Detecting mood: {mood}]')
        print(f'[User: {content}]')
        self.system_message = {"role": "system", "content": self.system_background.format(mood)}
        self.messages[0] = self.system_message
        self.messages.append({"role": "user", "content": f'{name} said {content} in motion of {mood}'})

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

    # TODO achieve effect: user B:'Did you see user A? what is going on with him?', Nao:'I met him just know,
    #  he looks sad.'
    # TODO: multi users appear in screen case consideration.
    def get_emotion(self, face):
        # Self-develop FER
        emotion = 'sad'
        return emotion

    def get_face(self, img=None):
        # Plug in Naoqi's face detection or self-developed face detection.
        face = input('-->Input a face: ')
        return {face}

    def ask_name(self):
        asking_name_sentence = 'Hi, new person. Could you please tell me what is your name?\n'
        name = input(asking_name_sentence)
        self.messages.append({"role": "assistant", "content": asking_name_sentence})
        self.messages.append({"role": "user", "content": f'{name} said Yes, my name is {name}'})
        return name

    def add_known_person(self, name='', face={}):
        self.known_person[name] = face

    def get_known_person(self):
        return self.known_person

    def match_known_person(self, face):
        for name, f in self.known_person.items():
            if face == f:
                print(f'[known person {name} appears]')
                self.last_name = name
                self.last_face = face
                return name
        name = self.ask_name()
        self.last_name = name
        print(f'[new person {name} appears]')
        self.add_known_person(name, face)
        print(f'[new person {name} becomes known person]')
        self.last_face = face
        return True


if __name__ == "__main__":
    api_test = APITest()
    mood_list = ['anger', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
    while True:
        # user_mood = random.choice(mood_list)
        # user_mood = 'sad'
        # user_content = input('user input: ')
        # api_test.query(user_mood, user_content)
        # break

        api_test.communication()
