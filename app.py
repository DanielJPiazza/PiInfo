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
    success = None
    error = None
    return_flag = 0
    
    # Setup the API call to OpenWeatherMap
    api_key = config.api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_id = "5128581" # 5128581 is New York City, US
    units = "imperial" # Kelvin is an empty string (""); celsius is "metric"
    final_url = base_url + "appid=" + api_key + "&id=" + city_id + "&units=" + units

    # JSON data returned from OpernWeatherMap API
    weather_data = (requests.get(final_url)).json()
    weather_data_output = {}

    # Parse results or determine error message, depending on API response
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
        error = "ERROR: " + weather_data["message"]
        return_flag = 1
    
    else:
        error = "ERROR: An unknown issue has occured."
        return_flag = 1

    if not return_flag:
        if (weather_data_output):
            success = weather_data_output
        else:
            error = "ERROR: Output container is empty."

    return render_template("index.html", weather=success, error=error)

# Verify file is running as main program, and set port/debug values
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
