# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 20:39:16 2021

@author: Michael
"""

import random

class Agent():
    def __init__(self, environment, agents, neighbourhood, i, y=None, x=None,):
        if (y == None):
            self._y = random.randint(0,299)
        else:
            self._y = y
        if (x == None):
            self._x = random.randint(0,299)
        else:
            self._x = x
        self.environment = environment
        self.store = 0
        self.agents = agents
        self.neighbourhood = neighbourhood
        self.name = i + 1
        
    def gety(self):
        return self._y
    
    def sety(self, value):
        self._y = value
        
    def dely(self, value):
        del self._y
    
    y = property(gety, sety, dely, "I'm the 'y' property.")
    
    def getx(self):
        return self._x

    def setx(self, value):
        self._x = value
        
    def delx(self, value):
        del self._x

    x = property(getx, setx, delx, "I'm the 'x' property.")

    def move(self): # Controls the movement of agents. If store is above 50, the agent moves twice as far. 
        if random.random() < 0.5:
            if self.store > 50:
                self._y = (self._y + 2) % 300
            else:
                self._y = (self._y + 1) % 300
        else:
            if self.store > 50:
                self._y = (self._y - 2) % 300
            else:
                self._y = (self._y - 1) % 300

        if random.random() < 0.5:
            if self.store > 50:
                self._x = (self._x + 2) % 300
            else:
                self._x = (self._x + 1) % 300 
        else:
            if self.store > 50:
                self._x = (self._x - 2) % 300
            else:
                self._x = (self._x - 1) % 300
        
    def eat(self): # Controls the eating by agents. How much they eat and also allows them to eat the leftover if food is 10 or below without creating negative values.
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        else:
            self.store += self.environment[self.y][self.x]
            self.environment[self.y][self.x] -= self.environment[self.y][self.x]
            
    def __str__(self): # Can be used to print relevant information about specific agents. 
        return "Agent name = " + str(self.name) + ", x = " + str(self._x) + ", y = " + str(self._y) + ", store = " + str(self.store)
    
    def sick(self): # Agent is sick after their store reaches a specific value. All food is added back to the environment where the agent is. 
        if self.store >= 100:
            self.environment[self.y][self.x] += self.store
            self.store = 0

    def share_with_neighbours(self, neighbourhood): # Agents share their store when they are within proximity of each other meaning they all end with the average store.
        for agent in self.agents:
            dist = self.distance_between(agent)
            if dist <= neighbourhood:
                sum = self.store + agent.store
                ave = sum / 2
                self.store = ave
                agent.store = ave

    def distance_between(self, agent): # Works out the distance between agents for use in communication/neighbourhoods. 
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5
