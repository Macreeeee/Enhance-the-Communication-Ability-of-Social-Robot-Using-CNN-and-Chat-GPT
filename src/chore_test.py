from naoqi import ALProxy
IP = "pepper.local"
PORT = 9559
motion = ALProxy("ALMotion", IP, PORT)
tts = ALProxy("ALTextToSpeech", IP, PORT)
motion.moveInit()
motion.moveTo(0.5, 0, 0) # (x; y; theta)
tts.say("I am walking")