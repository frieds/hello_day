## Hello Day

### Original Problem

Living in New York, I have experienced firsthand the unpredictable nature of fall and winter weather. In an effort to 
stay active and enjoy the city's beauty, I aim to go outside 3-5 times a day. However, it is not uncommon for me to lose
track of time, spend 5+ hours working indoors and feel cabin fever. Additionally, when I do intend to go outside, I 
always look up the weather and try to make informed decisions about what to wear and what accessories to bring, such as 
a hat or umbrella. Unfortunately, I often forget to pack essential items like an umbrella on rainy days.

To solve these problems, I created logic in this Python service and two Apple Shortcuts.

### Solutions

#### Personalized Clothing & Accessories Recommendations Based on Weather

One [Apple Shortcut](https://www.icloud.com/shortcuts/7759e43905d54459b1b69d160f7add18) recommends clothing and 
accessories based on real-time weather data. I run the Shortcut from my iPhone home screen in one click. 

<iframe width="188" height="355" src="https://www.youtube.com/embed/DTJAUE3NoiA" title="Apple Shortcut: Personalized Clothing Recommendations Based on Weather" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
 
Interested in this functionality and live in the United States? If yes, email me at dan [@] dfrieds.com, and I'll 
incorporate your clothing & accessory suggestions for the Shortcut too.

#### Automated Sunrise & Sunset Walk Calendar Events 

Another [Apple Shortcut](https://www.icloud.com/shortcuts/c999c3b235d84297bd6d40d07d4f5cc7) automatically creates 
calendar events for sunrise and sunset walks. The Shortcut runs every day at 1 am and uses your location to create the 
two events. Sunrise walk starts at sunrise and lasts 30 minutes. Sunset walk starts 30 minutes before sunset and lasts
until sunset. 

You can use this Shortcut and automation now. You can duplicate the Shortcut to customize the time and duration 
of these events given the sunrise and sunset times. Please send any feedback to dan (@) dfrieds.com

### Privacy

The Shortcuts will ask for your location data and calendar access on your phone only. I do not store any data.


### Tech Stack / Resources

Python, external APIs for weather and sunrise/sunset data, HTTP server hosted on [Replit](https://replit.com/@frieds/helloday)
with 2 FastAPI endpoints, pydantic for data validation, Apple Shortcuts to get location data on device and integrate 
with calendar account to create events. All code open-source.

### Disclaimer

My API is not versioned. It's in beta. Email me to have always-working functionality.