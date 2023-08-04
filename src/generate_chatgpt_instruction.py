import openai
import sys
import json

openai.api_key = "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"

role_text = "You are a excellent instruction interpreter assistant named NAO. Your task is to understand a " \
            "conversation, " \
            "and generate action based on the conversation. For example, if a conversation is: 'user:can you " \
            "move a little bit backward?  assistant:yes, as you wish.', then you should generate a prompt" \
            "that making a robot moving backward a little bit. If you think there is no suitable prompt you" \
            "can generate, you can just let the robot simply turn to stand up. Below are some examples and " \
            "instruction lists, you should learn from the example, and know what can use in instruction lists. " \
            "Remember, only start generate prompt once I say 'start generate'"

function_list = {
    "motion_proxy.moveTo(x, y, theta)": "The robot will move toward location (x, y) with angle theta. x, y is defined as "
                                        "meters, theta is defined as ridians. if theta is zero, then x is the direction "
                                        "that the robot currently face to",
    "posture_proxy.goToPosture('StandInit', 0.5)": "The robot will stand.",
    "motion_proxy.rest()": "The robot will sit down and rest. This is the most stable posture."
}

example_list = {"example 1": [
    {"input": "User:Hi NAO, can you move a little bit backward? you are too close to me. Assistant: Sure, no problem!"},
    {
        "output": "posture_proxy.goToPosture('StandInit', 0.5), motion_proxy.moveTo(-0.2, 0.0, 0.0), time,sleep(1), "
                  "posture_proxy.goToPosture('StandInit', 0.5)"}],
    "example 2": [{"input": "User:What day is it today?. Assistant: Today is Sunday"},
                  {"output": "posture_proxy.goToPosture('StandInit', 0.5)"}],
    "example 3": [{"input": "User:Hi, NAO, can you sit down?. Assistant: Sure!"},
                  {"output": "motion_proxy.rest()"}],
    "example 4": [
        {
            "input": "User:Hi NAO, stand close to me. Assistant: I am coming!"},
        {
            "output": "posture_proxy.goToPosture('StandInit', 0.5), motion_proxy.moveTo(0.2, 0.0, 0.0), time,sleep(1), "
                      "posture_proxy.goToPosture('StandInit', 0.5)"}],
}

output_format = "your output format should use slash symbol to saperat each motion:'motion one/motion two/motion three', the arguments used like x, y can be changed by you with any unmber."

log = json.load(open("./recordings/communication_recording.json", "r"))['log']
last_communication = log[-2:]
last_communication = '{}. {}: {}.'.format(last_communication[0]['content'], last_communication[1]['role'],
                                          last_communication[1]['content'])
# print(last_communication)

background = str(role_text) + str(function_list) + str(example_list) + str(output_format)
# print(background)

message = [{'content': background, 'role': 'system'},
           {'content': last_communication, 'role': 'user'}]

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=message,
    max_tokens=100,
)

chat_response = completion.choices[0].message.content
print(chat_response)
