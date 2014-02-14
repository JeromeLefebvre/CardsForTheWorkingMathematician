#!/usr/local/bin/python3.3

'''
http://projecteuler.net/problem=106
Special subset sums: meta-testing
Problem 106
'''

'''
Notes on problem 106():
'''

from math import factorial as f
def nCk(n,k):
	if k > n:
		return 0
	return f(n)//(f(k)*f(n-k))

def problem106():
	n = 4
	total = 0
	for i in range(1,n+1):
		sub = 0
		for j in range(i,n-i):
			sub += nCk(n-i,j)
		total += nCk(n,i)*sub
	return total

from cProfile import run
if __name__ == "__main__":
	run("problem106()")
	print(problem106()) 