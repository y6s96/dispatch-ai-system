# AI-Based Freight Dispatch and Driver–Load Matching System

## Overview

This project is an AI-powered freight dispatch and driver–load matching system developed using Machine Learning, Exploratory Data Analysis (EDA), and Python.

The system analyses freight loads and recommends suitable loads for drivers based on operational efficiency, profitability, truck compatibility, deadhead distance, and driver preferences.

The project was developed as part of the MSc Artificial Intelligence and Data Science programme for module CSC-44112.

---

# Features

- Freight load analysis
- Driver–load matching
- Machine Learning prediction models
- XGBoost optimisation
- Hyperparameter tuning
- Exploratory Data Analysis (EDA)
- Learning curve visualisation
- Feature importance analysis
- Tkinter frontend prototype
- Broker information integration

---

# Machine Learning Models Used

The following models were implemented and compared:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- XGBoost Regressor

The models were evaluated using:

- R² Score
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Matplotlib
- Seaborn
- Tkinter
- Jupyter Notebook

---

# Project Structure

```text
dispatch-ai-system/
│
├── Frontend/
├── Backend/
├── dataset/
├── outputs/
├── dispatch_ai_analysis.ipynb
├── requirements.txt
├── README.md
└── report/
```

---

# Dataset

This project uses a synthetic freight logistics dataset generated for academic and research purposes.

Dataset includes:
- Origin and destination cities
- Freight rates
- Miles
- Truck types
- Deadhead distances
- Broker information
- Pickup and delivery dates
- Driver operational information

---

# Frontend Prototype

The project includes a Tkinter-based frontend prototype with:

- Load search interface
- AI matching system
- Broker details popup
- EDA dashboard
- Driver information input

---

# How to Run

## Install Requirements

```bash
pip install -r requirements.txt
```

## Run Frontend

```bash
python Frontend/app.py
```

## Run Notebook

```bash
jupyter notebook
```

Open:

```text
dispatch_ai_analysis.ipynb
```

---

# Results

The XGBoost model achieved the strongest overall performance during evaluation and hyperparameter tuning.

Important operational features included:
- RPM (Rate Per Mile)
- Deadhead distance
- Efficiency score
- Truck compatibility
- Driver rating

---

# Academic Context

This project was developed for:

**Module:** CSC-44112 Advanced Applications of AI and Machine Learning  
**Programme:** MSc Artificial Intelligence and Data Science

---

# AI Usage Disclosure

ChatGPT (OpenAI GPT-5.5) was used for idea refinement, report structuring, debugging assistance, and documentation support. All implementation, experimentation, evaluation, and final decisions were independently completed and verified by the author.

---

# Author

Hamza Javid  
MSc Artificial Intelligence and Data Science
