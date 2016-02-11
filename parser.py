#!/usr/bin/python
#coding: utf8
import sys

def parse(f):
	width, height, drones, turns, load, products, nbwarehouses, nborders, i = 0, 0, 0, 0, 0, 0, 0, 0, 0
	lastsection = -1
	weights = []
	warehouses = []
	orders = []
	for line in f:
		line = line.replace('\n', '')

		# First section
		if i == 0: # number of rows, of columns, of drones, deadline, maximum load
			width, height, drones, turns, load = [int(x) for x in line.split(' ')]

		# Second section
		elif i == 1: # number of product types
			products = int(line)
		elif i == 2: # width per products
			weights = [int(x) for x in line.split(' ')]

		# Third section
		elif i == 3: # number of warehouses
			nbwarehouses = int(line)
			lastsection = 4+nbwarehouses*2
		elif i >= 4 and i < lastsection: # warehouses properties
			data = [int(x) for x in line.split(' ')]
			if i%2 == 0: # First line
				warehouses.append({'x': data[0], 'y': data[1]})
			else: # Second line
				warehouses[-1]['products'] = data

		# Last section
		elif i >= lastsection:
			if i == lastsection: # number of products
				nborders = int(line)
			else:
				data = [int(x) for x in line.split(' ')]
				pos = (i-lastsection-1)
				if pos%3 == 0: # First line
					orders.append({'x': data[0], 'y': data[1]})
				elif pos%3 == 1: # Second line
					orders[-1]['nbproducts'] = data[0]
				else: # Third line
					orders[-1]['products'] = data[:]
		i += 1
	return locals()

if __name__ == '__main__':
	print parse(sys.stdin)