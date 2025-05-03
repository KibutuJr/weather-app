from flask import Flask, request, jsonify, render_template_string
import requests
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

API_KEY = "a67dfcbd9143c133ff7dde86ba451c1e"

# Frontend Route
@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>🌦️ My Modern Weather App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to right, #00c6ff, #0072ff);
            color: white;
            text-align: center;
            padding: 20px;
            margin: 0;
            transition: 0.3s;
        }
        .dark {
            background: linear-gradient(to right, #232526, #414345);
            color: #eee;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 30px rgba(0,0,0,0.2);
            backdrop-filter: blur(8px);
        }
        input {
            padding: 10px;
            border: none;
            border-radius: 5px;
            margin: 5px;
            width: 70%;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background: #ffce00;
            color: #333;
            font-weight: bold;
            cursor: pointer;
            margin: 5px;
            font-size: 16px;
            transition: 0.2s;
        }
        button:hover {
            background: #ffd633;
        }
        .weather {
            margin-top: 20px;
        }
        .forecast-item {
            background: rgba(255,255,255,0.2);
            padding: 15px;
            margin: 10px 0;
            border-radius: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        img {
            width: 60px;
        }
        .toggle {
            margin-top: 10px;
            cursor: pointer;
            font-size: 14px;
            color: #ffce00;
        }
        @media (max-width: 600px) {
            input {
                width: 80%;
            }
            .forecast-item {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather App</h1>
        <input id="city" placeholder="Enter City (e.g. Nairobi)" />
        <br>
        <button onclick="getWeather()">Get Weather</button>
        <button onclick="useMyLocation()">Use My Location 📍</button>
        <div class="toggle" onclick="toggleDark()">🌙 Toggle Dark Mode</div>
        <div class="weather" id="weather"></div>
    </div>
    <script>
        function getWeather() {
            const city = document.getElementById('city').value;
            fetch(`/api/weather?city=${encodeURIComponent(city)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('weather').innerHTML = `<p style="color: red;">${data.error}</p>`;
                    } else {
                        showWeather(data);
                    }
                })
                .catch(err => {
                    console.error(err);
                    document.getElementById('weather').innerHTML = `<p style="color: red;">Error fetching data.</p>`;
                });
        }

        function useMyLocation() {
            navigator.geolocation.getCurrentPosition(pos => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                fetch(`/api/weather?lat=${lat}&lon=${lon}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            document.getElementById('weather').innerHTML = `<p style="color: red;">${data.error}</p>`;
                        } else {
                            showWeather(data);
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        document.getElementById('weather').innerHTML = `<p style="color: red;">Error fetching data.</p>`;
                    });
            });
        }

        function showWeather(data) {
            const container = document.getElementById('weather');
            container.innerHTML = `
                <h2>${data.city}, ${data.country}</h2>
                <p>🕒 Local Time: ${data.local_time}</p>
            `;
            data.forecast.forEach(day => {
                const iconUrl = `https://openweathermap.org/img/wn/${day.icon}@2x.png`;
                container.innerHTML += `
                    <div class="forecast-item">
                        <div>
                            <strong>${day.date}</strong><br>
                            ${day.weather}<br>
                            🌡️ ${day.temp}°C
                        </div>
                        <img src="${iconUrl}" alt="${day.weather}" />
                    </div>
                `;
            });
        }

        function toggleDark() {
            document.body.classList.toggle('dark');
        }
    </script>
</body>
</html>
    """)

# Backend API Route
@app.route('/api/weather')
def weather():
    city = request.args.get('city')
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    # Validate input
    if not city and not (lat and lon):
        return jsonify({"error": "Please provide a city name or allow location access."}), 400

    # Build request URL
    if city:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"

    res = requests.get(url)
    data = res.json()

    # Handle API errors
    if data.get("cod") != "200":
        return jsonify({"error": data.get("message", "Could not fetch weather data.")}), 500

    forecast_list = []
    seen_dates = set()
    for item in data['list']:
        # original date string
        date_str = item['dt_txt'].split(' ')[0]
        # parse to date object then format with weekday
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted = dt_obj.strftime('%a, %Y-%m-%d')  # e.g. Mon, 2025-05-03

        if formatted not in seen_dates:
            seen_dates.add(formatted)
            forecast_list.append({
                "date": formatted,
                "temp": item['main']['temp'],
                "weather": item['weather'][0]['description'],
                "icon": item['weather'][0]['icon']
            })
        if len(forecast_list) >= 5:
            break

    # Calculate local time
    timezone_offset = data['city']['timezone']  
    local_time = datetime.utcnow() + timedelta(seconds=timezone_offset)
    local_time_str = local_time.strftime('%Y-%m-%d %H:%M')

    return jsonify({
        "city": data['city']['name'],
        "country": data['city']['country'],
        "local_time": local_time_str,
        "forecast": forecast_list
    })

if __name__ == '__main__':
    app.run(debug=True)
