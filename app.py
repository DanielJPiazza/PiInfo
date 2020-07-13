import json, requests, datetime
from flask import Flask

app = Flask(__name__)

@app.route("/")
def get_weather():
    api_key = "569c2c65dc9ec74dd2082cf106b62fca"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_id = "5128581" # 5128581 is New York City, US
    units = "imperial" # Kelvin is an empty string (""); celsius is "metric"
    final_url = base_url + "appid=" + api_key + "&id=" + city_id + "&units=" + units

    # JSON data returned from API
    weather_data = (requests.get(final_url)).json()
    weather_data_output = {}

    # Parse results, or print error message depending on API response
    if (weather_data["cod"] == 200):
        weather_data_output["Location"] = weather_data["name"]
        weather_data_output["Time"] = (datetime.datetime.now()).strftime("%-I:%M%p")    # From server's clock, not API response
        weather_data_output["Date"] = (datetime.datetime.now()).strftime("%a %b %d %Y") # From server's clock, not API response
        weather_data_output["Temperature (F)"] = weather_data["main"]["temp"]
        weather_data_output["Cloud Cover (%)"] = weather_data["clouds"]["all"]
        weather_data_output["Conditions"] = weather_data["weather"][0]["main"] + " (" + weather_data["weather"][0]["description"] + ")"
        weather_data_output["Humidity (%)"] = weather_data["main"]["humidity"]
        weather_data_output["Wind Speed (MPH)"] = weather_data["wind"]["speed"]

    elif (weather_data["cod"] in [401, 404, 429]):
        return "ERROR: " + weather_data["message"]
    else:
        return "ERROR: An unknown issue has occured."

    # Final output, from dictionary
    if (weather_data_output):
        return weather_data_output
    else:
        return "ERROR: Output container is empty."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
