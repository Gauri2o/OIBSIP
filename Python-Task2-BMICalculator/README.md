# BMI Calculator – OASIS INFOBYTE

## Task
Python Programming – Task 2

## Project Overview

This project is an advanced BMI Calculator developed using Python and Tkinter.

The application allows users to calculate their Body Mass Index (BMI), classify the result into standard BMI categories, save records for different users, view historical records, and visualize BMI trends using a graph.

## Features

- User-friendly Tkinter GUI
- BMI calculation using weight and height
- BMI classification:
  - Underweight
  - Normal
  - Overweight
  - Obese
- Input validation
- Multiple user support
- SQLite database for BMI history
- View historical BMI records
- BMI trend visualization using Matplotlib
- Error handling for database operations
- Clear form functionality

## BMI Formula

BMI is calculated using:

BMI = Weight (kg) / Height² (m)

### Categories

| BMI Range | Category |
|---|---|
| Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25 – 29.9 | Overweight |
| 30 or above | Obese |

## Technologies Used

- Python 3.11
- Tkinter
- SQLite3
- Matplotlib

## Project Structure

```text
Python-Task2-BMICalculator/
│
├── main.py
├── bmi.db
├── requirements.txt
├── README.md
├── .gitignore
├── screenshots/
│   ├── calculator-result.png
│   ├── bmi-history.png
│   └── bmi-trend.png
└── venv/