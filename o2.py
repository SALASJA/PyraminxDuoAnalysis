class O2Cube:
	def __init__(self):
		self.faces = {"w" : 0, 
					  "o" : 1, 
					  "y" : 2,
					  "r" : 3, 
					  "b" : 4, 
					  "g" : 5}
		self.centers = ["w","o","y", "r", "b","g"]
		self.moves = 0
	
	def toString(self):
		result = ""
		for face, index in self.faces.items():
			result += "{:s} => {:s}\n".format(face, self.centers[index])
		result += f"\nMOVES : {self.moves}\n"
		return result
	
	def __str__(self):
		return self.toString()
		
	def __repr__(self):
		return self.__str__()
		
	
	def __or__(self, value):
		self.turn(value)
		return self
		
	def __invert__(self):
		self.reset()
		return self
		
	def turn(self, value):
		if value in ["", None]:
			self.moves += 1
			return False
		
		operations = {"u" : [0,1,2,3],
		              "d" : [0,3,2,1],
		              "l" : [1,4,3,5],
		              "r" : [1,5,3,4]}
		if value not in operations:
			return False
		
		operation = operations[value]
		self.shift(operation)
		self.moves += 1
		return True
		
	def shift(self, operation):
		index = operation[0]
		temp = self.centers[index]
		n = len(operation)
		i = 0
		while i < n - 1:
			shift_index = operation[i + 1] 
			self.centers[index] = self.centers[shift_index]
			i = i + 1
			index = operation[i]
		self.centers[index] = temp
	
	def reset(self):
		self.moves = 0
		self.centers = ["w","o","y", "r", "b","g"]
		
		
	
	
	
	

		
			
			