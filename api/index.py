from flask import Flask, render_template, request
import requests
import os


app = Flask(__name__)
API_KEY = "897e740be87d4d3a7afc002bc24dbdb9"

def get_background(condition):
    mapping = {
        "Clear": "clear.jpeg",
        "Clouds": "cloudy.jpeg",
        "Rain": "rain.jpeg",
        "Snow": "snow.jpeg",
        "Thunderstorm": "thunderstorm.jpeg",
    }
    return mapping.get(condition, "default.jpeg")

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    weather_data = {
        "background": "default.jpeg"  
    }

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "city": city.title(),
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"],
                    "background": get_background(data["weather"][0]["main"])
                }
            else:
                error = "City not found. Please try again."
        else:
            error = "Please enter a city name."

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
