# Register for an account at weatherapi.com. 
# OK!

# What is the URL to the documentation?
# https://www.weatherapi.com/docs/ is the basic docs
# https://www.weatherapi.com/api-explorer.aspx is another
# version where you can test things out without programming

# Make a request for the current weather where you are born, or somewhere you've lived.
# So first you have to scroll down to the "Request" section instead of going right
# to the "Realtime API" section, because for whatever reason they don't give you the endpoints
# when they're actually talking about the api
# So the current one is "/current.json or /current.xml"
# We love json so /current.json. Add the "http://api.weatherapi.com/v1" base URL
# and you get http://api.weatherapi.com/v1/current.json
# Scrolling down a bit more you see you need to give it a key and a query parameter q
import requests

# YOU WILL SCREW UP CUTTING AND PASTING THIS BECAUSE IT
# WILL INCLUDE THE "LIVE" BUTTON. it's done this for years!!!
# why they don't fix it, i don't know!
api_key = "c52fbcfa1fa84d819e114406200211"
url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q=New York City"
response = requests.get(url)
weather = response.json()
print(weather)

# Print out the country this location is in.
print(weather.keys())
# location, probably?? then poke around on the docs
# to discover that 'location' is returned with every request
# and includes a 'country' key
print(weather['location']['country'])

# Print out the difference between the current temperature and how warm it feels. Use "It feels ___ degrees colder" or "It feels ___ degrees warmer," not negative numbers.
print(weather['current'])
temp_feels = weather['current']['feelslike_f']
temp_is = weather['current']['temp_f']
if temp_feels == temp_is:
    print(f"It both feels and is {temp_is}")
elif temp_feels > temp_is:
    diff = temp_feels - temp_is
    print(f"It feels {diff} degrees warmer")
else:
    diff = temp_is - temp_feels
    print(f"It feels {diff} degrees colder")

# What's the current temperature at Heathrow International Airport?
# Use the airport's IATA code to search.
# Heathrow's code is LHR : 
api_key = "c52fbcfa1fa84d819e114406200211"
# This totally works, but...
url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q=LHR"
# ...you can also be specific based on what the documentation tells you to do
# when dealing with iata codes
url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q=iata:LHR"
response = requests.get(url)
weather = response.json()

# Same as before!
print(weather['current']['temp_f'])


# What URL would I use to request a 3-day forecast at Heathrow?
# this is so easy if you just go to https://www.weatherapi.com/api-explorer.aspx
# and click the 'forecast' tab
url = "https://api.weatherapi.com/v1/forecast.json?key=c52fbcfa1fa84d819e114406200211&q=LHR&days=3&aqi=no&alerts=no"

# Print the date of each of the 3 days you're getting a forecast for.
response = requests.get(url)
data = response.json()

# If you used the api explorer, you can just poke around and visually
# figure it out without toooooo much trouble
for day in data['forecast']['forecastday']:
    print(day['date'])

# Print the maximum temperature of each of the days.
# Again, just looking at it visually in the API explorer helps
# documentation is nice but... sometimes you'll be lazy instead
# (and hope you didn't do anything wrong)
for day in data['forecast']['forecastday']:
    print(day['date'], day['day']['maxtemp_f'])

# Print the day with the highest maximum temperature.

# METHOD ONE: Combine the previous two answers
# with the largest/smallest example from 
# http://jonathansoma.com/lede/foundations-2019/classes/data%20structures/looping-patterns/

# Start with no day having the highest temp
# and the highest temp we've seen be a very low number
# (not zero, because what if it were winter in a cold place?
# temperatures can get below zero!)
highest_day = ''
highest_temp = -999
for day in data['forecast']['forecastday']:
    # Is this day's temp higher than what we've seen before?
    if day['day']['maxtemp_f'] > highest_temp:
        highest_temp = day['day']['maxtemp_f']
        highest_day = day['date']
        print(f"New highest temp day is {highest_day} with a temp of {highest_temp}")

print("Highest temp day is", highest_day)

# METHOD TWO: using sort and keys
# say hey, we want you to sort the list of days
# but instead of alphabetically or whatever, look at each
# date's ['day']['maxtemp_f']
sorted_days = sorted(data['forecast']['forecastday'], key=lambda day: day['day']['maxtemp_f'])
highest = sorted_days[-1]
# smallest goes first, so the last one will be the highest temp
print(highest['date'], "with a temp of", highest['day']['maxtemp_f'])
