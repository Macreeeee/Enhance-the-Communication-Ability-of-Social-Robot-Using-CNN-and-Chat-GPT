import openai
import sys
import json

#D:\GitRepos\COMP66090\cognitive_robot_with_machine_learning\src\chat.py
openai.api_key = "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"
# messages = []
# content = ' '.join(sys.argv[1:])
# # print(content)
# message = {"role": "user", "content": content}
# messages.append(message)

with open('./communication_recording.json', 'r') as openfile:
    # Reading from json file
    log = json.load(open("./communication_recording.json", "r"))['log']
    # print(log)
    # communication = json.load(openfile)['log']

completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=log,
            max_tokens=30,
)

chat_response = completion.choices[0].message.content
# print(f'ChatGPT: {chat_response}')
print(chat_response)
