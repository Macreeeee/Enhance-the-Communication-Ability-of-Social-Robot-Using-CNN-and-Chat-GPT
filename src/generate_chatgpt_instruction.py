import json


def generate_role():
    role_text = "You are a excellent instruction interpreter assistant named NAO. Your task is to understand a " \
                "conversation, " \
                "and generate action based on the conversation. For example, if a conversation is: 'user:can you " \
                "move a little bit backward?  assistant:yes, as you wish.', then you should generate a prompt" \
                "that making a robot moving backward a little bit. If you think there is no suitable prompt you" \
                "can generate, you can just let the robot simply turn to stand up. Below are some examples and " \
                "instruction lists, you should learn from the example, and know what can use in instruction lists. " \
                "Remember, only start generate prompt once I say 'start generate'"


def generate_function_list():
    function_list = {"motion.moveTo(x, y, theta)": "The robot will move toward location (x, y) with angle theta. x, y is defined as meters, theta is defined as ridians",
                     "robotPosture.goToPosture('StandInit', 0.5f)": "The robot will stand."}


def generate_prompt_examples():
    example_list = {"example 1": [{"input": "U ser:Hi NAO, can you move a little bit backward? you are too close to me. Assistant: Sure, no problem!"},
                                  {"output": "motion.moveTo(0.0f, 0.2f, 1.5708f), time,sleep(1), robotPosture.goToPosture('StandInit', 0.5f)"}],
                    "example 2": [{
                                      "input": "U ser:What day is it today?. Assistant: Today is Sunday"},
                                  {
                                      "output": "robotPosture.goToPosture('StandInit', 0.5f)"}]
                    }


def generate_prompt_format():
    output_format = "your output format should be a dictionary: 'output': 'motion one, motion two, motion three,...'"
