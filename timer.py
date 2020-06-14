#!/usr/bin/env python3
import psutil
from datetime import datetime
import time
import webbrowser
import random
import os
import json
import pyautogui
#print(str(datetime.now())[11:19])
PROCNAME = "java"
playTime = 3#*60**2
earliest = "12:00:00"
afktimer = 60
afktime = 0
t = datetime.now()

start = 0

earlys = ["Maybe go do some math?", "Wanna go draw something?", "Any homework that needs to be done?"]
urls = ["https://play.prodigygame.com/", "https://play.dreambox.com/"]

if os.path.exists("day.json"):
    with open("day.json") as f:
        day = json.load(f)
    if day[0] != t.day:
        day = [t.day, time.time()]
        with open("day.json", 'w') as f:
            json.dump(day, f)            
else:
    day = [t.day, time.time()]
    with open("day.json", 'w') as f:
        json.dump(day, f)


def timeToSeconds(arg):
    result = 0
    arg = arg.split(":")
    for i, t in enumerate(arg):
        result += int(t)*60**(2-i)
    return result

def convert(seconds): 
    mint, sec = divmod(seconds, 60) 
    hour, mint = divmod(mint, 60) 
    return hour, mint, sec

def show(args):

    with open("day.json") as f:
        day = json.load(f)

    delta = time.time() - day[1]
    if delta//60 >= 1:

        with open("day.json", 'w') as f:
            day = [t.day, time.time()]
            json.dump(day, f)

        with open("page.html", 'w') as f:
            if args[0] == "early":
                f.write(f"<center> <h1> It might be a little early to play minecraft right now</h1> <p>{args[1]}")
            elif args[0] == "too much":
                f.write(f"<center> <h1> Time to close minecraft ;)</h1> <p> You have been playing for {args[1]} hours and {args[2]} minutes by now")

        if random.randint(0, 1):
            webbrowser.open("page.html", new=2)
        else:
            webbrowser.open(random.choice(urls), new=2)
        time.sleep(0.5)
        pyautogui.hotkey("winleft", "up")


while True:
    try:
        for proc in psutil.process_iter():
            if proc.name() == PROCNAME:
                if start == 0:
                    #playing = True
                    start = proc.create_time()
                    mouse = [pyautogui.position(), time.time()]

                # checking for mouse activity
                """ deltaTime = time.time()-mouse[1]
                if pyautogui.position() != mouse[0] and deltaTime <= afktimer:
                    mouse = [pyautogui.position(), time.time()]
                    playing = True
                elif pyautogui.position() == mouse[0] and deltaTime > afktimer:
                    playing = False
                    afktime += afktimer
                    mouse[1] = time.time() """
                

                # if playing:
                # too early
                nowTime = str(datetime.now())[11:19]
                deltaEarly = timeToSeconds(nowTime) - timeToSeconds(earliest)
                if deltaEarly < 0:
                    show(["early", random.choice(earlys)])
                
                # too long
                delta = time.time() - start
                if delta > playTime:
                    h, m, s = convert(time.time()-start-afktime)
                    show(["too much", int(h), int(m)])
            else:
                start = 0

            #print(proc.create_time(), time.time())
    except psutil.NoSuchProcess:
        pass