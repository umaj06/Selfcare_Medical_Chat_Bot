from flask import Flask, render_template, jsonify, request
import processor
import threading
import time
import pyttsx3
import speech_recognition as sr
r = sr.Recognizer()

# engine = pyttsx3.init()
# engine.setProperty('rate', 150)
# engine.setProperty('volume', 0.7)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'


def speak(response):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.7)
    engine.say(response)
    engine.runAndWait()
    engine.endLoop()


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())


@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    if request.method == 'POST':
        print(request.form)
        the_question = request.form['question']
        if len(the_question) >= 1:
            response = processor.chatbot_response(the_question)
        
            return jsonify({"response": response})
        else:
            print("Tell Something")
            # audio = None
            # while audio:
            with sr.Microphone() as source:
                print("Speak something...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                try:
                    the_question = r.recognize_google(audio)
                    response = processor.chatbot_response(the_question)
                    print(the_question)
                    
                    print(response)
                    return jsonify({"response": response})
                except sr.UnknownValueError:
                    print("Oops! Unable to understand speech.")
                except sr.RequestError as e:
                    print("Error: ", e)

    else:
        print("Tell Something")
        # audio = None
        # while audio:
        with sr.Microphone() as source:
            print("Speak something...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                the_question = r.recognize_google(audio)
                response = processor.chatbot_response(the_question)
                print(the_question)
                return jsonify({"response": response})
            except sr.UnknownValueError:
                print("Oops! Unable to understand speech.")
            except sr.RequestError as e:
                print("Error: ", e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
