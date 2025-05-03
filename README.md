# Weather App 🌦️

A full-stack **Weather Application** that allows users to fetch real-time weather data by city. Built using a **React.js** frontend and **Flask** backend (Python), styled with **Tailwind CSS**.

---

## 📚 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Project Structure](#project-structure)
* [Getting Started](#getting-started)
* [API Usage](#api-usage)
* [Contributing](#contributing)
* [License](#license)

---

## 🚀 Overview

This project is a simple yet functional weather app that demonstrates modern full-stack development. The user inputs a city name, and the app fetches and displays weather information using a third-party weather API.

* Frontend: React with Tailwind CSS for responsive design.
* Backend: Python Flask REST API.

---

## ✨ Features

* 🌍 Search current weather by city name.
* 📦 React frontend with Tailwind CSS styling.
* 🚀 Flask backend acting as a proxy server for API calls.
* 🎯 Clean code structure with separation of concerns.

---

## 🛠️ Tech Stack

**Frontend:**

* React.js (Vite setup)
* Tailwind CSS

**Backend:**

* Python 3
* Flask
* Requests (for API calls)

**Version Control:**

* Git & GitHub

---

## 📂 Project Structure

```
Weather App/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── assets/
│   │   └── styles/
│   ├── package.json
│   └── tailwind.config.js
├── backend/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

---

## 🔥 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/KibutuJr/weather-app.git
cd weather-app
```

### 2. Setup Backend (Flask)

#### Create a virtual environment and activate:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

#### Install Python dependencies:

```bash
pip install -r requirements.txt
```

#### Run Flask server:

```bash
flask run
```

Server will run at `http://127.0.0.1:5000`

### 3. Setup Frontend (React + Tailwind)

#### Navigate to frontend folder:

```bash
cd ../frontend
```

#### Install Node dependencies:

```bash
npm install
```

#### Run React App:

```bash
npm run dev
```

App will be available at `http://localhost:5173`

---

## 🌐 API Usage

The app uses **OpenWeatherMap API** (or any other weather API service you configure).

* Endpoint: `/weather?city={city_name}`
* Method: `GET`

Example:

```
http://127.0.0.1:5000/weather?city=Nairobi
```

---

## 🤝 Contributing

Feel free to fork the repository and submit pull requests!

1. Fork it 🍴
2. Create your feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a pull request 🚀

---

## 📄 License

This project is licensed under the MIT License.

---

> Built by Kibutu Jr
