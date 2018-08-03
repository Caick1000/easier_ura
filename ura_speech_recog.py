import speech_recognition as sr
import pyaudio


speech = sr.Recognizer()
with sr.Microphone() as source:                # use the default microphone as the audio source
    audio = speech.listen(source)                   # listen for the first phrase and extract it into audio data

try:
    print("You said " + r.recognize(audio))         # recognize speech using Google Speech Recognition
except IndexError:                                  
    print("No internet connection")
except KeyError:                                    # the API key didn't work
    print("Invalid API key or quota maxed out")
except LookupError:                                 # speech is unintelligible
    print("Could not understand audio")
