# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 20:32:16 2021

@author: Michael
"""

import random
import operator
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import matplotlib.animation
import agentframework
import csv
import tkinter
import requests
import bs4


# Key variables. 
num_of_agents = 200
num_of_iterations = 40
neighbourhood = 20
agents = []


# Read in raster environment data.

# Creates an empty list for the environment data to be stored in. 
environment = []

# Reads in the raster data from a file.
# Appends rowlist to the environment list to create a 2D list.
f = open('in.txt', newline='')
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
for row in reader:
    rowlist = []
    for value in row:
        rowlist.append(value)
    environment.append(rowlist)
f.close()

#Shows the initial environment. 
matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.show()


# Imports x and y data from a table on this website. 
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})


# Function that runs the model. Will be used by the GUI.
def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=False, frames=num_of_iterations)
    canvas.draw()


# Function which updates the plot in the animation.
# Includes the bulk of the agent code. 
def update(frame_number):
    fig.clear()

# Prints to say iteration has begun.
# Agent order is shuffled to avoid bias towards early agents in the list. 
# Move the agents. 
# Agents are sick after moving.
# Agents then eat.
# Agents then share store. 
# Prints to show each agents position and variables. 
    print("Start of iteration " + str(frame_number + 1))
    random.shuffle(agents)
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].sick()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
        print(str(agents[i]))
    
  
# Relates to the individual plots after each iteration. 
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)

# Prints that an iteration has ended. 
    print("End of iteration " + str(frame_number + 1))


# Animation figure parameters.
fig = matplotlib.pyplot.figure(figsize=(8, 8))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_autoscale_on(False)


# This code relates to the GUI window, menu and run operation. 
root = tkinter.Tk()
root.wm_title("Model")
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run Model", command=run)
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


# Make the agents.
# This uses the data from the website as x and y. 
# Also allows for the number of agents to be over the number of agents from the web data.
# Not the perfect solution. Couldn't get the default value working. 
print("Initial agent locations, properties")
for i in range(num_of_agents):
    if i <= (len(td_ys)-1):
        y = int(td_ys[i].text)
    else:
        y = None
    if i <= (len(td_ys)-1):
        x = int(td_xs[i].text)
    else:
        x = None
    agents.append(agentframework.Agent(environment, agents, neighbourhood, i, y, x))
    print(str(agents[i]))


# Controls the animation settings
animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=False, frames=num_of_iterations)

# Both of these are not initiated when the code runs.
# Both are functional when run individually after the code has run.
# Write out the environment as a csv. 
with open("finalenvironment.txt", "w") as f:
    for line in environment:
        for value in line:
            f.write(str(value) + ",")
        f.write("\n")


# File to write the total amount stored by all the agents on a line.
# Appends this data to the file each time the code is run. 
with open("totalagentsstored.txt", "a") as f:
    for i in agents:
        f.write(str(i.store) + ",")
    f.write("\n")

# Code runs for ever and it gets stuck on this line.
# I have been unable to resove this issue and as such manual 
# KeyboardInterrupt is required to stop the code from running. 
tkinter.mainloop()
