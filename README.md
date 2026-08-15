# 🐍 OASIS INFOBYTE – Python Programming Internship

## 📌 Internship Overview

This repository contains the projects completed as part of the **OASIS INFOBYTE Python Programming Internship**.

The internship focused on developing practical Python applications and applying programming concepts such as GUI development, API integration, database management, validation, automation, and secure programming.

---

## 📚 Completed Tasks

| Task       | Project                             | Description                                                                                                                                 |
| ---------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Task 1** | 🎙️ Voice Assistant                 | Advanced Python voice assistant with weather, web search, reminders, date/time, and knowledge-based commands                                |
| **Task 2** | ⚖️ BMI Calculator                   | BMI calculation application with category classification, calculation history, SQLite storage, and BMI trend visualization                  |
| **Task 3** | 🔐 Secure Random Password Generator | Cryptographically secure password generator with customizable character options, strength detection, clipboard support, and session history |

---

# 🎙️ Task 1 – Voice Assistant

### Project Overview

An advanced desktop voice assistant developed using Python.

The assistant accepts voice commands, identifies the requested intent, performs the required operation, and provides a voice response.

### Key Features

* 🎙️ Voice command recognition
* 🔊 Text-to-speech responses
* 🕐 Time and date
* 🌦️ Weather information
* 🌐 Web search
* ⏰ Reminders
* 🧠 Knowledge-based queries
* 📋 Intent detection
* 🔐 API configuration
* 🛡️ Error handling

### Technologies

* Python
* SpeechRecognition
* pyttsx3
* Requests
* PyAudio
* OpenWeather API

### Project

[Open Task 1 – Voice Assistant](Python-Task1-VoiceAssistant/)

---

# ⚖️ Task 2 – BMI Calculator

### Project Overview

An interactive BMI Calculator developed using Python.

The application calculates Body Mass Index from the user's height and weight, classifies the result into standard BMI categories, stores previous calculations, and displays BMI trends.

### Key Features

* ⚖️ BMI calculation
* 📊 BMI category classification
* 🗃️ Calculation history
* 💾 SQLite database
* 📈 BMI trend visualization
* 🧪 Input validation
* 🖥️ User-friendly interface

### BMI Categories

| BMI Range      | Category      |
| -------------- | ------------- |
| Below 18.5     | Underweight   |
| 18.5 – 24.9    | Normal Weight |
| 25.0 – 29.9    | Overweight    |
| 30.0 and above | Obesity       |

> BMI is a general screening measure and is not a medical diagnosis.

### Technologies

* Python
* Tkinter
* SQLite
* Matplotlib

### Project

[Open Task 2 – BMI Calculator](Python-Task2-BMICalculator/)

---

# 🔐 Task 3 – Secure Random Password Generator

### Project Overview

A secure password generator developed using Python and Tkinter.

The application uses Python's `secrets` module to generate cryptographically secure passwords based on user-selected requirements.

### Key Features

* 🔐 Secure password generation
* 📏 Adjustable password length
* 🔠 Uppercase letters
* 🔡 Lowercase letters
* 🔢 Numbers
* 🔣 Symbols
* 🚫 Ambiguous character exclusion
* 💪 Password strength indicator
* 📋 Copy to clipboard
* 🕒 Last 5 generated passwords during the current session
* 🧪 Input validation
* 🔒 No permanent password history storage

### Technologies

* Python
* Tkinter
* secrets
* string
* pyperclip

### Project

[Open Task 3 – Secure Password Generator](Python-Task3-RandomPasswordGenerator/)

---

# 📁 Repository Structure

```text
OIBSIP/
│
├── Python-Task1-VoiceAssistant/
│   ├── screenshots/
│   ├── .gitignore
│   ├── config.json
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
├── Python-Task2-BMICalculator/
│   ├── screenshots/
│   ├── .gitignore
│   ├── bmi.db
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
├── Python-Task3-RandomPasswordGenerator/
│   ├── screenshots/
│   ├── .gitignore
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
└── README.md
```

---

# 🛠️ General Technologies

The projects in this repository use a combination of:

* Python 3.11+
* Tkinter
* SQLite
* Matplotlib
* SpeechRecognition
* pyttsx3
* Requests
* PyAudio
* secrets
* pyperclip
* REST APIs

---

# ⚙️ Running the Projects

Each task is maintained as a separate project with its own dependencies and README.

Navigate to the required task folder and follow the installation instructions provided in its README.

For example:

```bash
cd Python-Task1-VoiceAssistant
```

or:

```bash
cd Python-Task2-BMICalculator
```

or:

```bash
cd Python-Task3-RandomPasswordGenerator
```

---

# 🔐 Security Practices

The projects follow basic security practices where applicable.

* Sensitive API credentials should not be committed to GitHub.
* Virtual environments are excluded using `.gitignore`.
* Python cache files are excluded from version control.
* The password generator uses Python's `secrets` module for security-sensitive random generation.
* Password history in Task 3 is maintained only during the current application session.

---

# 📸 Project Screenshots

Screenshots demonstrating the functionality of each project are available inside their respective `screenshots` folders.

* Task 1 → Voice Assistant screenshots
* Task 2 → BMI Calculator screenshots
* Task 3 → Password Generator screenshots

---

# 🎯 Internship Details

**Organization:** OASIS INFOBYTE

**Track:** Python Programming

**Internship:** OASIS INFOBYTE Python Programming Internship

**Completed Tasks:** 3

---

# 👩‍💻 Author

**Gauri Srivastava**

B.Tech – Computer Science and Engineering
