from fuzzywuzzy import fuzz
import pyttsx3
import speech_recognition as sr
import sys


class Logger:

    ALERT = '\033[31m'
    WARN = '\033[33m'
    INFO = '\033[34m'
    SUCCESS = '\033[36m'
    FOCUS = '\033[40m'
    ENDC = '\033[0m'

    def __init__(self, *args, **kwargs):
        self.say = True if kwargs.get('say') else False
        if self.say:
            self.engine = pyttsx3.init()
        pass

    def sayit(self, msg):
        if self.say:
            self.engine.say(msg)
            self.engine.runAndWait()

    def log(self, msg, **kwargs):
        self.sayit(msg)
        print(kwargs.get('color') + msg + self.ENDC)

    def alert(self, msg):
        self.log(msg, color=self.ALERT)

    def warn(self, msg):
        self.log(msg, color=self.WARN)

    def info(self, msg):
        self.log(msg, color=self.INFO)

    def success(self, msg):
        self.log(msg, color=self.SUCCESS)

    def focus(self, msg):
        self.log(msg, color=self.FOCUS)


class Receiver:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.logger = Logger(say=True)
        self.resolver = Resolver()

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        while True:
            with self.microphone as source:
                audio = self.recognizer.listen(source)
            try:
                value = self.recognizer.recognize_google(audio)
                self.resolver.resolve(value)
            except sr.UnknownValueError:
                self.logger.alert('Oops, could not catch that')
            except sr.RequestError:
                self.logger.alert('unexpected request error')


class Resolver:

    response_mapping = {
        'hello': 'welcome sir!',
        'hi': 'hello sir!',
        'auto': 'hello sir! how can i help you',
        'update': 'you have been lazy lately, sir!'
    }

    def __init__(self, *args, **kwargs):
        self.logger = Logger(say=True)

    def resolve(self, msg):
        if 'exit' in msg:
            sys.exit(0)
        matched_key = None
        match_percentage = 0
        for key in self.response_mapping:
            current_match_percentage = fuzz.ratio(key, msg)
            if current_match_percentage > match_percentage:
                match_percentage = current_match_percentage
                matched_key = key
        if not matched_key:
            self.logger.alert('I dont understand, could you try again sir?')
        else:
            self.logger.info(self.response_mapping[matched_key])
