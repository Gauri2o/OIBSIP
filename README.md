# 🎙️ Advanced Python Voice Assistant

## 📌 OASIS INFOBYTE — Python Programming Internship

**Task:** Task 1 – Voice Assistant  
**Track:** Python Programming  
**Tier:** Advanced  
**Internship:** OASIS INFOBYTE SIP

---

## 📖 Project Overview

This project is an advanced Python-based Voice Assistant that accepts
spoken commands through a microphone and responds using text-to-speech.

The assistant can perform several useful tasks such as telling the
current time and date, searching the web, providing weather information,
answering general knowledge questions, setting reminders, and executing
user-defined custom commands.

The project demonstrates speech recognition, natural language intent
detection, API integration, text-to-speech, JSON-based configuration,
and error handling in Python.

---

## ✨ Features

### 🎤 Voice Interaction

- Captures commands using a microphone.
- Converts speech into text using SpeechRecognition.
- Provides spoken responses using pyttsx3.

### 👋 Greeting

The assistant responds to commands such as:

> Hello

with a predefined greeting.

### 🕐 Time and Date

The assistant can provide:

- Current time
- Current date
- Current day

Example:

> What is the time?

> What is today's date?

### 🌐 Web Search

The assistant can perform Google searches using voice commands.

Example:

> Search Python programming

The corresponding search is opened automatically in the web browser.

### 🌦️ Live Weather

The assistant uses the OpenWeatherMap API to provide:

- City name
- Temperature in Celsius
- Temperature in Fahrenheit
- Humidity
- Weather condition
- Wind speed

Example:

> What's the weather in Allahabad?

### ⏰ Timed Reminders

Users can set reminders using voice commands.

Example:

> Remind me after 10 seconds

After the specified duration, the assistant gives an audible reminder.

### 🧠 Knowledge Base

The assistant contains a local knowledge base for answering
general questions related to topics such as:

- Python
- Java
- JavaScript
- Artificial Intelligence
- Machine Learning
- Computer Science
- OpenCV
- MediaPipe
- SQL
- Databases
- General knowledge

Example:

> What is Python programming?

The answer is provided both in the terminal and through voice.

### ⚙️ Custom Commands

Users can add their own commands through `config.json`.

Example:

```json
{
    "custom_commands": {
        "open youtube": "https://www.youtube.com",
        "open github": "https://github.com",
        "open linkedin": "https://www.linkedin.com"
    }
}