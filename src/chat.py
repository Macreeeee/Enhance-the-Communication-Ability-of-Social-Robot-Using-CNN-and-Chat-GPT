import openai
import sys
import json

if __name__ == '__main__':
    openai.api_key = sys.argv[1]
    with open('./recordings/communication_recording.json', 'r') as openfile:
        # Reading from json file
        log = json.load(open("./recordings/communication_recording.json", "r"))['log']

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=log,
        max_tokens=30,
    )

    chat_response = completion.choices[0].message.content
    print(chat_response)
