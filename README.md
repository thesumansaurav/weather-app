# weather-app

Weather App is a web-based application that allows users to retrieve and update weather information for different cities. It integrates with a weather API to provide real-time weather data.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)
7. [Acknowledgments](#acknowledgments)

## Introduction
Weather App is designed to fetch weather data for specified cities and store it for future reference. It includes features to update weather information based on user queries and maintains a user session to personalize the experience.

## Features
- Retrieve weather data for a specific city.
- Update and store weather information in the database.
- Unique user session management.
- Error handling for API requests.

## Getting Started
Follow these steps to set up and run the Weather App on your local machine.

### Prerequisites
- Python 3.7 or higher
- Django 3.2

### Installation
Clone the repository:

```bash
git clone https://github.com/thesumansaurav/weather-app.git
cd weather-app
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
 ## Urls
 For landing page: http://localhost:8000/
 For Api :  http://localhost:8000/swagger/
 
