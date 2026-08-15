import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import threading
import requests
import os
import re
import json

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak(text):
    """
    Display the response in terminal
    and speak it using pyttsx3.
    """

    text = str(text).strip()

    if not text:
        return

    print(f"Assistant: {text}")

    try:
        engine = pyttsx3.init()

        engine.setProperty("rate", 160)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()

        engine.stop()

    except Exception as error:
        print("Text-to-speech error:", error)


# ============================================================
# SPEECH RECOGNITION
# ============================================================

recognizer = sr.Recognizer()


def listen():
    """
    Listen to microphone input and convert
    speech into text.
    """

    with sr.Microphone() as source:

        print("\nListening...")

        try:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:

            speak(
                "I didn't hear anything. Please try again."
            )

            return ""

    try:

        print("Recognizing...")

        text = recognizer.recognize_google(
            audio
        )

        text = text.lower().strip()

        print(f"You: {text}")

        return text

    except sr.UnknownValueError:

        speak(
            "Sorry, I couldn't understand that. "
            "Please repeat."
        )

        return ""

    except sr.RequestError:

        speak(
            "Speech recognition service is unavailable."
        )

        return ""


# ============================================================
# GREETING
# ============================================================

def greeting():

    speak(
        "Hello! How can I help you?"
    )


# ============================================================
# TIME
# ============================================================

def tell_time():

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    speak(
        f"The current time is {current_time}."
    )


# ============================================================
# DATE
# ============================================================

def tell_date():

    current_date = datetime.datetime.now().strftime(
        "%A, %d %B %Y"
    )

    speak(
        f"Today is {current_date}."
    )


# ============================================================
# WEB SEARCH
# ============================================================

def web_search(command):

    search_query = command

    remove_words = [
        "search for",
        "search",
        "google",
        "look up",
        "find"
    ]

    for word in remove_words:

        search_query = search_query.replace(
            word,
            ""
        )

    search_query = search_query.strip()

    if not search_query:

        speak(
            "What would you like me to search for?"
        )

        search_query = listen()

        if not search_query:
            return

    speak(
        f"Searching the web for {search_query}."
    )

    url = (
        "https://www.google.com/search?q="
        + search_query.replace(" ", "+")
    )

    webbrowser.open(url)


# ============================================================
# WEATHER
# ============================================================

def get_weather(city):

    if not WEATHER_API_KEY:

        speak(
            "Weather API key is not configured."
        )

        return

    if not city:

        speak(
            "Please tell me the city name."
        )

        return

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        # Invalid API key
        if response.status_code == 401:

            speak(
                "The weather API key is invalid."
            )

            return

        # City not found
        if response.status_code == 404:

            speak(
                f"I could not find weather information "
                f"for {city}."
            )

            return

        # Other errors
        if response.status_code != 200:

            speak(
                "Sorry, I could not fetch the weather right now."
            )

            return

        city_name = data["name"]

        temperature = data["main"]["temp"]

        humidity = data["main"]["humidity"]

        condition = data["weather"][0]["description"]

        wind_speed = data["wind"]["speed"]

        fahrenheit = (
            temperature * 9 / 5
        ) + 32

        print("\nWeather Information")
        print("-------------------")

        print(f"City: {city_name}")

        print(
            f"Temperature: {temperature:.1f} °C"
        )

        print(
            f"Temperature: {fahrenheit:.1f} °F"
        )

        print(
            f"Humidity: {humidity}%"
        )

        print(
            f"Condition: {condition}"
        )

        print(
            f"Wind Speed: {wind_speed:.1f} m/s"
        )

        speak(
            f"The weather in {city_name} is "
            f"{temperature:.1f} degrees Celsius, "
            f"or {fahrenheit:.1f} degrees Fahrenheit. "
            f"The condition is {condition}. "
            f"Humidity is {humidity} percent. "
            f"Wind speed is {wind_speed:.1f} meters per second."
        )

    except requests.exceptions.Timeout:

        speak(
            "The weather service took too long to respond."
        )

    except requests.exceptions.ConnectionError:

        speak(
            "I could not connect to the weather service."
        )

    except Exception as error:

        print(
            "Weather error:",
            error
        )

        speak(
            "Sorry, I could not retrieve the weather information."
        )


# ============================================================
# EXTRACT CITY
# ============================================================

def extract_city(command):

    city = command.lower().strip()

    phrases_to_remove = [

        "what is the weather in",
        "what's the weather in",

        "what is weather in",
        "what's weather in",

        "tell me the weather in",
        "tell me weather in",

        "what is the temperature in",
        "what's the temperature in",

        "tell me the temperature in",

        "temperature in",
        "temperature of",

        "weather in",
        "weather of",

        "forecast in",
        "forecast for",

        "what is the weather",
        "what's the weather",

        "tell me the weather",

        "weather",
        "temperature",
        "forecast",

        "today"
    ]

    for phrase in phrases_to_remove:

        city = city.replace(
            phrase,
            ""
        )

    city = city.strip()

    city = re.sub(
        r"\s+",
        " ",
        city
    )

    return city


# ============================================================
# REMINDER
# ============================================================

def reminder_alert():

    speak(
        "Reminder! Your scheduled reminder is due."
    )


def set_reminder(command):

    pattern = (
        r"(\d+(?:\.\d+)?)\s*"
        r"(seconds?|minutes?|hours?)"
    )

    match = re.search(
        pattern,
        command
    )

    if not match:

        speak(
            "Please specify the duration. "
            "For example, remind me after ten seconds."
        )

        return

    amount = float(
        match.group(1)
    )

    unit = match.group(2).lower()

    if "second" in unit:

        delay = amount

    elif "minute" in unit:

        delay = amount * 60

    elif "hour" in unit:

        delay = amount * 3600

    else:

        speak(
            "I could not understand the duration."
        )

        return

    timer = threading.Timer(
        delay,
        reminder_alert
    )

    timer.daemon = True

    timer.start()

    if amount.is_integer():

        amount_text = str(
            int(amount)
        )

    else:

        amount_text = str(amount)

    speak(
        f"Reminder set for {amount_text} {unit}."
    )


# ============================================================
# KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_BASE = {

    "python": (
        "Python is a high level programming language. "
        "It is popular for artificial intelligence, "
        "machine learning, data science, automation, "
        "and web development."
    ),

    "python programming": (
        "Python is a high level programming language "
        "with simple and readable syntax. "
        "It is widely used for artificial intelligence, "
        "machine learning, data science, automation, "
        "and web development."
    ),

    "artificial intelligence": (
        "Artificial intelligence is a field of computer "
        "science that creates systems capable of performing "
        "tasks that normally require human intelligence."
    ),

    "machine learning": (
        "Machine learning is a branch of artificial "
        "intelligence where computers learn patterns "
        "from data to make predictions or decisions."
    ),

    "computer science": (
        "Computer science is the study of computers, "
        "algorithms, software, and information processing."
    ),

    "india": (
        "India is a country in South Asia. "
        "Its capital is New Delhi. "
        "India is known for its diverse cultures, "
        "languages, history, and technology sector."
    ),

    "mahatma gandhi": (
        "Mahatma Gandhi was an Indian independence leader "
        "who played a major role in India's freedom movement "
        "through nonviolent resistance."
    ),

    "albert einstein": (
        "Albert Einstein was a famous physicist. "
        "He developed the theory of relativity "
        "and made important contributions to modern physics."
    ),

    "javascript": (
        "JavaScript is a programming language mainly "
        "used to create interactive web pages. "
        "It is also used for server side development."
    ),

    "java": (
        "Java is an object oriented programming language "
        "used for enterprise applications, Android "
        "development, web applications, and many "
        "other software systems."
    ),

    "database": (
        "A database is an organized collection of data "
        "that can be stored, managed, searched, and updated."
    ),

    "sql": (
        "SQL stands for Structured Query Language. "
        "It is used to manage data in relational databases."
    ),

    "opencv": (
        "OpenCV is an open source computer vision library "
        "used for image processing, video processing, "
        "object detection, and face detection."
    ),

    "mediapipe": (
        "MediaPipe is a framework developed by Google "
        "for machine learning solutions involving "
        "computer vision, face tracking, hand tracking, "
        "and pose detection."
    )
}


# ============================================================
# KNOWLEDGE QUESTION
# ============================================================

def answer_question(command):

    question = command.lower().strip()

    phrases = [

        "who is",
        "who was",

        "what is",
        "what was",

        "tell me about",
        "explain",

        "give me information about",

        "can you tell me about",

        "please tell me about",

        "what do you know about"
    ]

    for phrase in phrases:

        question = question.replace(
            phrase,
            ""
        )

    question = question.strip()

    if not question:

        speak(
            "Please tell me what you would like to know."
        )

        return

    # Exact match

    if question in KNOWLEDGE_BASE:

        answer = KNOWLEDGE_BASE[question]

        print(
            f"Knowledge Answer: {answer}"
        )

        speak(answer)

        return

    # Partial match

    for topic, answer in KNOWLEDGE_BASE.items():

        if (
            topic in question
            or question in topic
        ):

            print(
                f"Knowledge Answer: {answer}"
            )

            speak(answer)

            return

    speak(
        "I don't have that topic in my local knowledge base."
    )


# ============================================================
# CUSTOM COMMANDS
# ============================================================

def load_custom_commands():

    """
    Load user-defined commands from config.json.
    """

    try:

        with open(
            "config.json",
            "r",
            encoding="utf-8"
        ) as file:

            config = json.load(file)

        commands = config.get(
            "custom_commands",
            {}
        )

        if not isinstance(
            commands,
            dict
        ):

            print(
                "custom_commands must be an object."
            )

            return {}

        return commands

    except FileNotFoundError:

        print(
            "config.json not found."
        )

        return {}

    except json.JSONDecodeError:

        print(
            "Invalid JSON format in config.json."
        )

        return {}

    except Exception as error:

        print(
            "Custom command error:",
            error
        )

        return {}


def execute_custom_command(command):

    """
    Check whether the spoken command exists
    in config.json and execute it.
    """

    custom_commands = load_custom_commands()

    command = command.lower().strip()

    for custom_command, action in custom_commands.items():

        custom_command = str(
            custom_command
        ).lower().strip()

        action = str(
            action
        ).strip()

        if command == custom_command:

            speak(
                f"Opening {custom_command}."
            )

            webbrowser.open(
                action
            )

            return True

    return False


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(command):

    if not command:

        return "unknown"

    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    greeting_patterns = [

        r"\bhello\b",
        r"\bhi\b",
        r"\bhey\b",

        r"\bgood morning\b",
        r"\bgood afternoon\b",
        r"\bgood evening\b"
    ]

    for pattern in greeting_patterns:

        if re.search(
            pattern,
            command
        ):

            return "greeting"

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    time_patterns = [

        r"\bwhat.*time\b",
        r"\btell.*time\b",
        r"\bcurrent time\b",
        r"\btime now\b",
        r"\btime is it\b"
    ]

    for pattern in time_patterns:

        if re.search(
            pattern,
            command
        ):

            return "time"

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    date_patterns = [

        r"\bwhat.*date\b",
        r"\btoday.*date\b",
        r"\bwhat day\b",
        r"\bcurrent date\b"
    ]

    for pattern in date_patterns:

        if re.search(
            pattern,
            command
        ):

            return "date"

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    weather_patterns = [

        r"\bweather\b",
        r"\btemperature\b",
        r"\bforecast\b",
        r"\bhow hot\b",
        r"\bhow cold\b"
    ]

    for pattern in weather_patterns:

        if re.search(
            pattern,
            command
        ):

            return "weather"

    # --------------------------------------------------------
    # REMINDER
    # --------------------------------------------------------

    reminder_patterns = [

        r"\bremind me\b",
        r"\bset a reminder\b",
        r"\breminder\b",
        r"\bremind me after\b",
        r"\bremind me in\b"
    ]

    for pattern in reminder_patterns:

        if re.search(
            pattern,
            command
        ):

            return "reminder"

    # --------------------------------------------------------
    # KNOWLEDGE
    # --------------------------------------------------------

    knowledge_patterns = [

        r"\bwho is\b",
        r"\bwho was\b",
        r"\bwhat is\b",
        r"\bwhat was\b",

        r"\btell me about\b",
        r"\bexplain\b",

        r"\bwhat do you know about\b",

        r"\bgive me information about\b"
    ]

    for pattern in knowledge_patterns:

        if re.search(
            pattern,
            command
        ):

            return "knowledge"

    # --------------------------------------------------------
    # WEB SEARCH
    # --------------------------------------------------------

    search_patterns = [

        r"\bsearch\b",
        r"\bgoogle\b",
        r"\blook up\b",
        r"\bsearch for\b"
    ]

    for pattern in search_patterns:

        if re.search(
            pattern,
            command
        ):

            return "search"

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    exit_patterns = [

        r"\bexit\b",
        r"\bquit\b",
        r"\bstop\b",
        r"\bgoodbye\b",
        r"\bbye\b"
    ]

    for pattern in exit_patterns:

        if re.search(
            pattern,
            command
        ):

            return "exit"

    return "unknown"


# ============================================================
# PROCESS COMMAND
# ============================================================

def process_command(command):

    # ========================================================
    # CUSTOM COMMANDS FIRST
    # ========================================================

    if execute_custom_command(command):

        return True

    # ========================================================
    # NORMAL INTENT DETECTION
    # ========================================================

    intent = detect_intent(
        command
    )

    print(
        f"Detected Intent: {intent}"
    )

    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if intent == "greeting":

        greeting()

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    elif intent == "time":

        tell_time()

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    elif intent == "date":

        tell_date()

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    elif intent == "weather":

        city = extract_city(
            command
        )

        if not city:

            speak(
                "Which city would you like the weather for?"
            )

            city = listen()

            if city:

                city = extract_city(
                    city
                )

        if city:

            print(
                f"Weather city: {city}"
            )

            get_weather(
                city
            )

    # --------------------------------------------------------
    # REMINDER
    # --------------------------------------------------------

    elif intent == "reminder":

        set_reminder(
            command
        )

    # --------------------------------------------------------
    # KNOWLEDGE
    # --------------------------------------------------------

    elif intent == "knowledge":

        answer_question(
            command
        )

    # --------------------------------------------------------
    # WEB SEARCH
    # --------------------------------------------------------

    elif intent == "search":

        web_search(
            command
        )

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    elif intent == "exit":

        speak(
            "Goodbye. Have a great day."
        )

        return False

    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    else:

        speak(
            "I'm not sure what you mean. "
            "Please try asking in another way."
        )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    speak(
        "Hello! I am your advanced voice assistant."
    )

    speak(
        "I can tell you the time and date, "
        "search the web, answer general questions, "
        "check the weather, set reminders, "
        "and execute custom commands."
    )

    while True:

        command = listen()

        if not command:

            continue

        should_continue = process_command(
            command
        )

        if not should_continue:

            break


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    main()