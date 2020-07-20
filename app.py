# Custom
import config

# Libraries
import json, requests, datetime
from flask import Flask, render_template

# Main
app = Flask(__name__)

@app.route("/")
def get_weather():
    # Flags and return variables
    weather_success = None
    weather_error = None
    weather_error_flag = 0
    
    # Setup the API call to OpenWeatherMap
    weather_api_key = config.weather_api_key
    weather_base_url = "http://api.openweathermap.org/data/2.5/weather?"
    weather_city_id = "5128581" # 5128581 is New York City, US
    weather_units = "imperial" # Kelvin is an empty string (""); celsius is "metric"
    weather_final_url = weather_base_url + "appid=" + weather_api_key + "&id=" + weather_city_id + "&weather_units=" + weather_units

    # JSON data returned from OpernWeatherMap API
    weather_data = (requests.get(weather_final_url)).json()
    weather_data_output = {}

    # Parse results or determine weather_error message, depending on API response
    if (weather_data["cod"] == 200):
        weather_data_output["location"] = weather_data["name"]
        weather_data_output["time"] = (datetime.datetime.now()).strftime("%-I:%M%p")    # From server's clock, not API response
        weather_data_output["date"] = (datetime.datetime.now()).strftime("%a %b %d %Y") # From server's clock, not API response
        weather_data_output["temp"] = weather_data["main"]["temp"]
        weather_data_output["cloudcover"] = weather_data["clouds"]["all"]
        weather_data_output["conditions"] = weather_data["weather"][0]["main"] + " (" + weather_data["weather"][0]["description"] + ")"
        weather_data_output["humidity"] = weather_data["main"]["humidity"]
        weather_data_output["windspeed"] = weather_data["wind"]["speed"]

    elif (weather_data["cod"] in [401, 404, 429]):
        weather_error = "weather_error: " + weather_data["message"]
        weather_error_flag = 1
    
    else:
        weather_error = "weather_error: An unknown issue has occured."
        weather_error_flag = 1

    if not weather_error_flag:
        if (weather_data_output):
            weather_success = weather_data_output
        else:
            weather_error = "weather_error: Output container is empty."

    return render_template("index.html", weather_success=weather_success, weather_error=weather_error)

# Verify file is running as main program, and set port/debug values
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
