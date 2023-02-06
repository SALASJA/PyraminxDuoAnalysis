from itertools import product, permutations
class Corner:
	def __init__(self, corner_type, initial_state = None):
		self.state = 0 if initial_state == None else initial_state
		self.corner_type = corner_type
		self.corner_possibilities = {"U" : ["Y", "B", "G"],
		                             "L" : ["Y", "G", "R"],
		                             "R" : ["Y", "R", "B"],
		                             "B" : ["R", "G", "B"]} 
		
	def getState(self):
		return self.state
		
	def turn(self, value):
		self.state = (self.state + value) % 3
	
	def getCornerString(self):
		possibility_copy = self.corner_possibilities[self.corner_type].copy()
		possibility_copy[self.state] = "|" +  possibility_copy[self.state] + "|"
		return "".join(possibility_copy)
		

class Pyramid:
	def __init__(self, initial_states = None):
		if initial_states == None:
			initial_states = [0,0,0,0]
			
		self.state = {"U" : Corner("U", initial_states[0]), 
					  "L" : Corner("L", initial_states[1]),
					  "R" : Corner("R", initial_states[2]),
					  "B" : Corner("B", initial_states[3])}
	def turn(self, value):
		if value == "":
			return False
			
		if not isinstance(value, str):
			return False
			
		turn_value = 1
		if value[-1] == "'":
			turn_value = -1
		 
		corner_type = value[0].upper()
		if corner_type not in self.state:
			return False
		
		self.state[corner_type].turn(turn_value)
		return True
	
	def __or__(self, value):
		self.turn(value)
		return self
	
	def pyramidString(self):
		result = ""
		for corner_type in self.state:
			result += corner_type + " : " + self.state[corner_type].getCornerString() + "\n"
		result += "SOLVED!" if self.solved() else "NOT SOLVED!"
		return result
	
	def solved(self):
		for corner_type in self.state:
			if self.state[corner_type].getState() != 0:
				return False
		return True
	
	def __str__(self):
		return self.pyramidString()
	
	def __repr__(self):
		return self.__str__()
	
	def execute(self, operations):
		for operation in operations:
			self.turn(operation)
		
	
class BeadPyramid(Pyramid):
	def __init__(self, initial_states = None, initial_center_state = None):
		super().__init__(initial_states)
		self.center_state = ["Y", "B", "G", "R"] if initial_center_state == None else initial_center_state
	
	def turn(self, value):
		successful_turn = super().turn(value)
		if not successful_turn:
			return False
		operations = {"U"  : [0,1,2],
					  "U'" : [0,2,1],
					  "L"  : [0,2,3],
					  "L'" : [0,3,2],
					  "R"  : [0,3,1],
					  "R'" : [0,1,3],
					  "B"  : [3,2,1],
					  "B'" : [3,1,2]}
		operation = operations[value]
		self.shift(operation)
		
	def shift(self, indicies):
		temp = self.center_state[indicies[0]]
		self.center_state[indicies[0]] = self.center_state[indicies[1]]
		self.center_state[indicies[1]] = self.center_state[indicies[2]]
		self.center_state[indicies[2]] = temp
		
	def pyramidString(self):
		result = super().pyramidString()
		result = "centers: " + self.center_state.__str__() + "\n" + result
		return result
	
	def solved(self):
		is_corners_solved = super().solved()
		is_centers_solved = self.center_state == ["Y","B","G","R"]
		return is_centers_solved and is_corners_solved

def main():
	all_operations = constructOperations()
	all_centers = list(permutations(["Y", "B", "G", "R"]))
	all_corners = list(product([0,1,2],repeat=4))
	possibilities = product(all_corners,all_centers)
	i = 1
	for possibility in possibilities:
		solution = findSolution(possibility,all_operations)
		if solution != None:
			print(i, possibility, solution)
			i = i + 1

def findSolution(possibility, all_operations):	
	for operation in all_operations:
		centers = list(possibility[1])
		corners = possibility[0]
		p = BeadPyramid(corners, centers)
		p.execute(operation)
		if p.solved():
			return operation
	return None
	
def constructOperations():
	operations = ["U", "U'", "L", "L'", "R", "R'", "B", "B'"]
	all_operations = []
	i = 1
	while i <= 4:
		all_operations += list(product(operations, repeat=i))		
		i = i + 1
	all_operations = [""] + all_operations
	return all_operations

if __name__ == "__main__":
	main()

