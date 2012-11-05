import random

def randomHash(length):
	word = ''
	for i in range(length):
		word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
	return word