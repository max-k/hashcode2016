#!/usr/bin/python
#coding: utf8
import math
import parser
import sys

actions = []

def distance(posA, posB):
	return int(math.ceil(math.sqrt((posA['x'] - posB['x'])**2 + (posA['y'] - posB['y'])**2)))

def fetchBestTarget(data, pos):
	indexes = [distance(warehouse, pos) for warehouse in data['warehouses']]
	warehouse = data['warehouses'][indexes.index(min(indexes))]

	indexes = [distance(order, warehouse) for order in data['orders']]
	order = data['orders'][indexes.index(min(indexes))]

	return order, warehouse

def checkWeight(data, drone, product = -1):
	x = 0 if product -1 else data['weights'][product]
	return (sum([data['weights'][p] for p in drone['products']]) + data['weights'][product]) <= data['load']

def countByProduct(o, product):
	return len([x for x in o['products'] if x == product])


def deliver(data):
	#print data
	actions = []
	orders = data['orders'][:]
	drones = [{'order': None, 'warehouse': None, 'x': 0, 'y': 0, 'products': []} for i in xrange(data['drones'])] # drone is (x,y) + a client target + products
	finished = False
	turns = data['turns']
	nbActions = len(actions)
	while (not finished) and turns: # While we have turns and the delivering is not finished
		for d in drones:
			if not d['order']:
				# Selecting an order
				order, warehouse = fetchBestTarget(data, d) # For each drone, decide which order is the best choice to deliver
				if order != None:
					d['order'] = order
					data['orders'].remove(order)
					for product in order['products'][:]:
						if checkWeight(data, d, product) and warehouse['products'][product] > 0:
							# For each product the order wants, check if the chosen warehouse has the item, and so, fetch them the weight does not overflow
							d['products'].append(product)
							#order['products'].remove(product)

					for product in set(d['products']): # Loading action + position update
						actions.append(str(drones.index(d))
										+ " L "
										+ str(data['warehouses'].index(warehouse))
										+ " "
										+ str(product)
										+ " "
										+ str(countByProduct(d, product)))
						turns -= 1 + distance(d, warehouse)
						d['x'] = warehouse['x']
						d['y'] = warehouse['y']
			else:
				# Delivering
				delivering = [0 for x in xrange(data['products'])] # number of delivered items per product
				delivered = False
				for product in d['order']['products'][:]:
					if product in d['products']:
						d['products'].remove(product)
						d['order']['products'].remove(product)
						delivering[product] += 1
				for product in xrange(len(delivering)):
					if delivering[product] > 0:
						delivered = True
						actions.append(str(drones.index(d))
									  	+ " D "
									  	+ str(orders.index(d['order']))
									  	+ " "
									  	+ str(product)
									  	+ " "
									  	+ str(delivering[product])
									  )
						turns -= 1

				if delivered:
					turns -= distance(d['order'], d)

				# Resetting the drone
				data['orders'].append(d['order'])
				d['order'] = None

		finished = False not in [len(order['products']) == 0 for order in orders] or len(actions) == nbActions
		nbActions = len(actions)
	#for order in data['orders']: print order
	return actions




def result(actions):
	print len(actions)
	for action in actions:
		print action

if __name__ == '__main__':
	result(deliver(parser.parse(sys.stdin)))