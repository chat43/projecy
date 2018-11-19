import re
from functools import reduce
import time
import sys

class LazyDfa():

	def  __init__(self, path):
		self.final_state, self.epsilon_state, self.state= self.initNfa(path)		#get the final state, epsilon state, state transition list
		self.dfa_state=[0]    #init of dfa state with first epsilon state
		self.transitions=[]	#init of a stack to store transitions
		self.result=set([])  #use a set to store the results

	def initNfa(self,path):
		state = re.split(r'//',path)
		epsilon_state=[]
		del(state[0])
		epsilon_state.append(0)			#first epsilon state
		for i in range(len(state)):
			state[i]=re.split(r'/',state[i])
			epsilon_state.append(epsilon_state[-1]+len(state[i]))		#epsilon state number = last epsilon number+length of state between two "//"
		return epsilon_state.pop(), epsilon_state,  reduce(lambda x,y:x+y, state)		#last of epsilon state is final state, so we pop it out,  and we combine all split query label into transition list called self.state

	def ldfa_run(self,label,index):
		self.transition(label)		#when something in, we do the transition operation
		while self.final_state in self.dfa_state:	#dfa_state may have several final state, so we use a set to store result and clear final state in dfa_state
			self.result.add(index)
			self.dfa_state.remove(self.final_state)

	def transition(self,label):#construct a new dfa state
		trans = []	
		handle=self.dfa_state.copy()		
		for item in handle:		#every state in dfa
			if self.state[item]==label:			#if coming label match
				if item in self.epsilon_state:	#if this state is a epsilon state
					self.dfa_state.append(item+1)	#just store the new state
				else:
					self.dfa_state.append(item+1)	#else, we remove the original state and store new state(original state+1)
					self.dfa_state.remove(item)
				trans.append(item+1)		#store this transition 
		self.transitions.append(trans)	#store all of transition of this input

	def reverse_transition(self):
		trans=self.transitions.pop()		#get the transition of this popped label
		handle=self.dfa_state.copy()		
		for item in trans:		
			if item==self.final_state:		#if this label is matched label
				pass													#do nothing
			else:															
				self.dfa_state.remove(item)		#else, we remove this state
			if item-1 in handle:								#if this state-1 which represent the last state of this state exist in the dfa state, we do nothing
				pass
			else:																#else, we add the last state in it
				self.dfa_state.append(item-1)

def main():
	start = time.time()
	file = sys.argv[1]
	path = sys.argv[2]
	auto = LazyDfa(path)   #New a lazy dfa algorithm instance
	index=-1
	for line in open(file):
		line = re.split(r' ',line.strip())		#read the xml stream
		if line[0]=='0':	
			index+=1					#to mark label 
			auto.ldfa_run(line[1],index)	 #when we get a input, we run the algorithm
		else:
			auto.reverse_transition()		#when one label is finish, we do a retransition 
	answer=list(auto.result)
	answer.sort()										#sort the answer
	print("answer:",answer)
	end = time.time()
	print("run-time:",end-start)

if __name__ == '__main__':
	main()


