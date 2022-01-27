# Central Limit Theorem
# =====================

import math
from random import randint

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider


def roll():
	""" One die roll. """
	return randint(1,6)

def multiroll(n):
	""" Roll n dice and return the sum. """
	total=0
	for i in range(n):
		total=total+roll()
	return total

def theory(p,n,s):
	""" Source: https://mathworld.wolfram.com/Dice.html (10) """
	kmax=np.floor((p-n)/s)
	k_range=np.arange(0,kmax+1,1,int)

	if k_range.size==0:
		return 0

	sum=0
	for k in k_range:
		a=math.pow(-1,k)
		b=math.comb(n,k)
		c=math.comb(p-s*k-1,n-1)
		sum+=a*b*c

	return sum

class Graph:
	def __init__(self):
		# Create plot.
		fig,self.axes=plt.subplots()
		self.line,=plt.plot(0)
		self.line2,=plt.plot(0)
		self.axes.set_ylabel("Occurences")
		# First update.
		self.update(2,1000)
		# Widgets.
		plt.subplots_adjust(bottom=0.25)
		slider_rolls=Slider(plt.axes((0.2,0.05,0.6,0.025)),'Rolls',1,10000,5000)
		slider_dice=Slider(plt.axes((0.2,0.10,0.6,0.025)),'Dice',1,10,2,valstep=1,valfmt="%i")
		slider_rolls.on_changed(lambda x:self.update(self.dice,int(x)))
		slider_dice.on_changed(lambda x:self.update(int(x),self.rolls))
		plt.show()

	def update(self,dice,rolls):
		self.dice=dice
		self.rolls=rolls

		# Perform random rolls.
		ys=[0]*(self.dice*6+1)
		for i in range(0,self.rolls):
			r=multiroll(self.dice)
			ys[r]=ys[r]+1
		# Update the empirical curve.
		self.line.set_data(range(len(ys))[self.dice:],ys[self.dice:])

		# Theoretical curve.
		x_range=range(self.dice,self.dice*6+1)
		t=[theory(x,self.dice,6) for x in x_range]
		t=np.array(t)/sum(t)*self.rolls
		self.line2.set_data(x_range,t)

		# Rescale axes.
		self.axes.relim()
		self.axes.autoscale()
		self.axes.set_ylim(ymin=0)

		# Update titles.
		dice_str=['die','dice'][self.dice>1]
		self.axes.set_title(f"{self.dice} {dice_str} rolled {self.rolls} times")
		self.axes.set_xlabel(f"Sum of {self.dice} {dice_str}")

def main():
	graph=Graph()

if __name__=="__main__":
	main()
