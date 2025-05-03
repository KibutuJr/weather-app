import { useState, useEffect } from "react";
import moment from "moment-timezone";
import { motion } from "framer-motion";

const API_BASE = "http://127.0.0.1:5000/api/weather";

function App() {
  const [city, setCity] = useState("");
  const [data, setData] = useState(null);

  const fetchWeather = (query) => {
    fetch(`${API_BASE}?city=${encodeURIComponent(query)}`)
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  };

  // On mount, try geolocation:
  useEffect(() => {
    navigator.geolocation?.getCurrentPosition((pos) => {
      fetch(
        `${API_BASE}?lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`
      )
        .then((r) => r.json())
        .then(setData)
        .catch(console.error);
    });
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-200 to-white p-6">
      <div className="max-w-md mx-auto bg-white p-6 rounded-2xl shadow-lg">
        <h1 className="text-2xl font-bold mb-4">Weather App</h1>
        <div className="flex mb-4">
          <input
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="flex-1 border rounded-l px-3 py-2"
            placeholder="Enter city…"
          />
          <button
            onClick={() => fetchWeather(city)}
            className="bg-blue-500 text-white px-4 rounded-r"
          >
            Go
          </button>
        </div>

        {data ? (
          <>
            <h2 className="text-xl mb-2">
              {data.city}, {data.country}
            </h2>
            <p className="mb-4">Local time: {data.local_time}</p>
            <div className="space-y-4">
              {data.forecast.map((day) => (
                <motion.div
                  key={day.date}
                  className="flex justify-between items-center bg-blue-50 p-3 rounded-lg"
                  whileHover={{ scale: 1.02 }}
                >
                  <div>
                    <p className="font-medium">{day.date}</p>
                    <p className="capitalize">{day.weather}</p>
                  </div>
                  <div className="text-right">
                    <p>{Math.round(day.temp)}°C</p>
                    <img
                      src={`https://openweathermap.org/img/wn/${day.icon}@2x.png`}
                      alt={day.weather}
                      className="w-12 h-12"
                    />
                  </div>
                </motion.div>
              ))}
            </div>
          </>
        ) : (
          <p className="text-center">Loading...</p>
        )}
      </div>
    </div>
  );
}

export default App;
