import requests
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import font

baseurl = 'http://api.weatherstack.com/'
endpoint = 'current'

def correctTimeZone(improperTime):
    military_time = datetime.strptime(improperTime, "%H:%M") #converts string to datetime object in corresponding military time
    standard_time = military_time.strftime("%I:%M %p") #converts military-time datetime object to standard-time datetime object
    return standard_time

def calculateWeather(city):    
    try:    
        response = requests.get(baseurl + endpoint + f'?access_key=582c814e46105afc5767dc7e333b894a&query={city}')
        data = response.json()
        if "error" in data: #Checks if API reponse contains an error (e.g. query entered is invalid)
            print(f"An error occurred when abstracting data. Error: {data['error']['info']}")
            return
            
    except requests.RequestException as e: #Catches Network-related issues raised by requests library
        print(f"Error Occurred: {e}")
        return
        
    except ValueError: #Catches error if JSON sends back invalid data
        print(f"Invalid JSON response from server.")
        return
    
    information = {    
        'Location' : data['request']['query'],
        'Time' : correctTimeZone(data['location']['localtime'].split()[1]),
        'Temperature' : f'{(data['current']['temperature']) * (9/5) + 32:.2f} degrees Fahrenheit',
        'Weather Descriptions' : ", ".join(data['current']['weather_descriptions']),
        'Wind Speed' : f"{data['current']['wind_speed']} mph",
        'Pressure' : f"{data['current']['pressure']} psi",
        'Precipitation' : data['current']['precip'],
        'Humidity' : f"{data['current']['humidity']}%",
        'UV Index' : data['current']['uv_index'],
    }

    return information


class MyGUI:
    def __init__(self):
        self.root = tk.Tk()

        self.root.attributes('-fullscreen', True)       #create window
        self.root.resizable(width=True, height=True)
        self.root.bind("<Configure>", self.resize)      #detect window resizing
        self.root.title("Weather App")  

        labelSize, entrySize, displayInfoSize = self.fontDimensions()
        #FONT SIZES
        self.labelFont = font.Font(family="SF Pro", size=labelSize, weight="bold")
        self.entryFont = font.Font(family="SF Pro", size=entrySize)
        self.displayInfoFont = font.Font(family="SF Pro", size=displayInfoSize)


        self.label = tk.Label(self.root, text="Weather Information")    #create weather app label
        self.label.config(font=self.labelFont)
        
        frameWidth, frameHeight = self.frameDimensions(self.root, 0.3, 0.05)       
        self.label.pack(pady=(frameHeight/2))


        self.enterFrame = tk.Frame(self.root, width=frameWidth, height=frameHeight)     #create frame for entering city name
        self.enterFrame.pack()
        self.enterFrame.pack_propagate(False) 


        self.enterCity = tk.Entry(self.enterFrame)         #create entry to type in city name
        self.enterCity.config(font=self.entryFont)

        self.enterCity.bind("<Return>", self.fetchAndDisplay)                   #binds enter key to enter button
        self.enterCity.pack(side='left', padx=(5,10), expand=True, fill = 'x')

        self.enterButton = ttk.Button(self.enterFrame, text="Enter", command = self.fetchAndDisplay)        #create enter button
        self.enterButton.pack(side='left', padx=(10,5))

        displayWidth, displayHeight = self.frameDimensions(self.root, 0.9, 0.7)         #create display frame
        self.displayFrame = tk.Frame(self.root, width=displayWidth, height=displayHeight)
        self.displayFrame.pack(pady=frameHeight)
        self.displayFrame.pack_propagate(False)

        self.displayInfo = tk.Text(self.displayFrame,height=9,bg=self.root['bg'], fg="white",bd=0, highlightthickness=0)
        self.displayInfo.config(font=self.displayInfoFont)
        self.displayInfo.config(state="disabled")
        self.displayInfo.pack(padx=(frameHeight/2))


        self.root.mainloop()        #display window
        
    def frameDimensions(self, window, xprop, yprop):
        screenWidth = window.winfo_screenwidth()
        screenHeight = window.winfo_screenheight()

        frameWidth = int(screenWidth * xprop)
        frameHeight = int(screenHeight * yprop)

        return frameWidth, frameHeight

    def fontDimensions(self):
        screenHeight = self.root.winfo_screenheight()

        displayFont = int(screenHeight * 0.05)
        labelFont = int(displayFont * 0.6)
        entryFont = int(displayFont * 0.4)

        return labelFont, entryFont, displayFont
    
    def displayWeather(self, weatherInfo):  #displays weather information onto the textbox
        self.displayInfo.config(state="normal")
        self.displayInfo.delete('1.0', tk.END)  #clear any existing information in the textbox
        for key, value in weatherInfo.items():
            self.displayInfo.insert(tk.END, f"{key}: {value}\n")    #print the key, values from the info dict
        self.displayInfo.config(state="disabled")
    
    def fetchAndDisplay(self,event="None"):      #calculates weather for given city in typed in entry box
        city = self.enterCity.get()
        weatherInfo = calculateWeather(city)
        self.displayWeather(weatherInfo)
    
    def resize(self, event):
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        self.resizeWidgets(width, height)
    
    def resizeWidgets(self, width, height):
        textFont = max(10, int(height * 0.05))

        #RESIZE WIDGET
        self.displayInfoFont.configure(size=textFont)
        self.labelFont.configure(size=int(textFont*0.6))
        self.entryFont.configure(size=int(textFont*0.4))

        self.displayInfo.config(font=self.displayInfoFont)
        self.label.config(font=self.labelFont)
        self.enterCity.config(font=self.entryFont)

        #RESIZE FRAMES
        self.enterFrame.config(width=int(width*0.3),height=int(height*0.05))
        self.displayFrame.config(width=int(width*0.9),height=int(height*0.7))



MyGUI()

