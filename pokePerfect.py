from numpy import array, zeros, sum, std
from scipy import optimize
import random
from math import floor
import sys
import csv


class PokeMatrix:
	def __init__(self):
		self.sequence = 0
		self.typeList = ["Normal", "Fire", "Water", "Electric", "Grass",  "Ice", "Fighting", \
			"Poison", "Ground",  "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon",  "Dark", "Steel", "Fairy"]
		self.pokemonDB = []
		with open("Pokemon.csv") as f:
			reader = csv.reader(f)
			for row in reader:
				self.pokemonDB.append(row)
		self.matrix = array([
			[1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, .5,  0,  1,  1, .5,  1],
			[1, .5, .5,  1,  2,  2,  1,  1,  1,  1,  1,  2, .5,  1, .5,  1,  1,  1],
			[1,  2, .5,  1, .5,  1,  1,  1,  2,  1,  1,  1,  2,  1, .5,  1,  1,  1],
			[1,  1,  2, .5, .5,  1,  1,  1,  0,  2,  1,  1,  1,  1, .5,  1,  1,  1],
			[1, .5,  2,  1, .5,  1,  1, .5,  2, .5,  1, .5,  2,  1, .5,  1, .5,  1],
			[1, .5, .5,  1,  2, .5,  1,  1,  2,  2,  1,  1,  1,  1,  2,  1, .5,  1],
			[2,  1,  1,  1,  1,  2,  1, .5,  1, .5, .5, .5,  2,  0,  1,  2,  2, .5],
			[1,  1,  1,  1,  2,  1,  1, .5, .5,  1,  1,  1, .5, .5,  1,  1,  0,  2],
			[1,  2,  1,  2, .5,  1,  1,  2,  1,  0,  1, .5,  2,  1,  1,  1,  2,  1],
			[1,  1,  1, .5,  2,  1,  2,  1,  1,  1,  1,  2, .5,  1,  1,  1, .5,  1],
			[1,  1,  1,  1,  1,  1,  2,  2,  1,  1, .5,  1,  1,  1,  1,  0, .5,  1],
			[1, .5,  1,  1,  2,  1, .5, .5,  1, .5,  2,  1,  1, .5,  1,  2, .5, .5],
			[1,  2,  1,  1,  1,  2, .5,  1, .5,  2,  1,  2,  1,  1,  1,  1, .5,  1],
			[0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  1,  1,  2,  1, .5,  1,  1],
			[1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  1, .5,  0],
			[1,  1,  1,  1,  1,  1, .5,  1,  1,  1,  2,  1,  1,  2,  1, .5,  1, .5],
			[1, .5, .5, .5,  1,  2,  1,  1,  1,  1,  1,  1,  2,  1,  1,  1, .5,  2],
			[1, .5,  1,  1,  1,  1,  2, .5,  1,  1,  1,  1,  1,  1,  2,  2, .5,  1]
		], dtype=float)
		self.exists = array([
			[True, False, True,  False, True,  False, True,  False, False, True,  True,  False, False, False, False, False, False, True],
			[True, False, False, True,  False, False, True,  False, True,  True,  True,  True,  True,  True,  True,  True,  True,  False],
			[True, True,  False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True],
			[True, False, True,  True,  True,  True,  False, False, True,  True,  False, True,  False, True,  True,  False, True,  True],
			[True, True,  False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  False, False, True,  True,  True],
			[True, False, False, True,  True,  True,  False, False, True,  True,  True,  False, False, True,  True,  True,  False, False],
			[True, True,  True,  True,  False, True,  False, True,  False, False, True,  True,  True,  False, False, True,  True,  False],
			[True, False, False, True,  False, True,  False, True,  True,  True,  False, True,  False, True,  False, True,  False, False],
			[True, False, True,  True,  True,  True,  True,  False, True,  True,  True,  True,  True,  True,  True,  True,  True,  False],
			[True, True,  True,  True,  True,  True,  True,  False, True,  True,  True,  True,  True,  True,  True,  True,  True,  True],
			[True, True,  True,  True,  False, True,  True,  True,  False, True,  True,  False, True,  False, True,  False, True,  True],
			[True, False, True,  True,  True,  True,  False, True,  True,  True,  True,  False, True,  True,  False, False, True,  False],
			[True, False, True,  True,  False, True,  False, True,  False, True,  True,  True,  True,  False, False, True,  True,  True],
			[True, False, True,  True,  True,  False, True,  False, True,  True,  True,  False, True,  False, True,  True,  False, False],
			[True, False, True,  True,  True,  False, True,  False, False, True,  True,  True,  False, False, True,  True,  True,  False],
			[True, False, True,  True,  False, True,  True,  True,  True,  True,  True,  False, False, True,  True,  True,  True,  False],
			[True, False, True,  True,  True,  True,  False, True,  False, True,  True,  True,  True,  True,  False, True,  True,  True],
			[True, False, True,  True,  True,  False, False, False, False, True,  True,  False, True,  False, False, False, True,  True]
			])

	def attack(self, pokeType, pokeType2):
		attack = self.matrix[pokeType, :].copy()
		attack += self.matrix[pokeType2, :].copy()
		return attack

	def defend(self, pokeType, pokeType2):
		defence = self.matrix[:, pokeType].copy()
		if pokeType2 and pokeType2 != pokeType:
			defence = defence * self.matrix[:, pokeType2].copy()
		return defence

	def scoreTeam(self, pokeTeam):
		totalAttack = zeros(18)
		totalDefence = zeros(18)
		for pokemon in pokeTeam:
			totalAttack = totalAttack + self.attack(pokemon[0], pokemon[1])
			totalDefence = totalDefence + self.defend(pokemon[0], pokemon[1])
		# print (max(totalAttack) - min(totalAttack)) * std(totalAttack)
		# print sum(totalAttack)
		score = sum(totalAttack - (1.0 * totalDefence)) - 1 * ((max(totalAttack) - min(totalAttack)) + (max(totalDefence) - min(totalDefence)))
		# print score
		return floor(score)

	def randomTeam(self, fixed=[]):
		team = fixed
		# for pokeCount in range(0, random.randint(1, 6)):
		for pokeCount in range(len(fixed), 6):
			pokemon = self.randomPokemon()
			while (not self.exists[pokemon[0]][pokemon[1]]) \
				or (pokemon in team) \
				or (self.flatten(team).count(pokemon[0]) >= 1) \
				or (self.flatten(team).count(pokemon[1]) >= 1):
				pokemon = self.randomPokemon()
			team.append(pokemon)
		return sorted(team)

	def flatten(self, l):
		return [item for sublist in l for item in sublist]

	def randomPokemon(self):
		type1, type2 = (self.seqType(), self.randomType())
		paring = (0, 0)
		if type1 < type2:
			paring = (type1, type2)
		else:
			paring = (type2, type1)
		return paring

	def seqType(self):
		self.sequence += 1
		return self.sequence % 18

	def randomType(self):
		return random.randint(0, 17)

	def optimal(self):
		team = optimize.anneal(self.scoreTeam, self.randomTeam())[0]
		print team

	def example(self, type1, type2):
		examples = []
		for row in self.pokemonDB:
			if type1.upper() in row[2] and ((type2 == type1 and type1.upper() == row[2]) or (type2.upper() in row[2] and type2 != type1)):
				examples.append(row[1])
		return examples

	def bruteforce(self, timeout=1000000, fixed=[]):
		maxTeam = self.randomTeam(fixed)
		oldScore = self.scoreTeam(maxTeam)
		while timeout:
			sys.stdout.write(str(timeout) + "\r")
			newTeam = self.randomTeam(fixed)
			# print newTeam
			newScore = self.scoreTeam(newTeam)
			# print newScore
			if newScore > oldScore:
				maxTeam = newTeam
				oldScore = newScore
			timeout -= 1
		# print maxTeam
		for pokemon in maxTeam:
			print self.typeList[pokemon[0]] + ", " + self.typeList[pokemon[1]]
			print '\t' + str(self.example(self.typeList[pokemon[0]], self.typeList[pokemon[1]]))
		print oldScore

if __name__ == '__main__':
	poke = PokeMatrix()
	# cathyTeam = [
	# 	(poke.typeList.index("Grass"), 	poke.typeList.index("Grass")),
	# 	(poke.typeList.index("Water"),	poke.typeList.index("Flying")),
	# 	(poke.typeList.index("Electric"), poke.typeList.index("Steel")),
	# 	(poke.typeList.index("Grass"),	poke.typeList.index("Normal")),
	# 	(poke.typeList.index("Electric"), poke.typeList.index("Electric")),
	# 	(poke.typeList.index("Fire"),		poke.typeList.index("Fire"))
	# ]
	# AnthonyTeam = [
	# 	(poke.typeList.index("Fighting"), poke.typeList.index("Steel")),
	# 	(poke.typeList.index("Fire"), poke.typeList.index("Fighting")),
	# 	(poke.typeList.index("Electric"), poke.typeList.index("Electric")),
	# 	(poke.typeList.index("Ground"), poke.typeList.index("Steel")),
	# 	(poke.typeList.index("Water"), poke.typeList.index("Flying")),
	# 	(poke.typeList.index("Grass"), poke.typeList.index("Ice"))
	# ]
	# print poke.scoreTeam(AnthonyTeam)
	# poke.bruteforce(fixed=AnthonyTeam[:2])
	# proTeam = [
	# 	(poke.typeList.index("Rock"),	poke.typeList.index("Dark")),
	# 	(poke.typeList.index("Dragon"),	poke.typeList.index("Ground")),
	# 	(poke.typeList.index("Psychic"), poke.typeList.index("Psychic")),
	# 	(poke.typeList.index("Dark"),	poke.typeList.index("Dragon")),
	# 	(poke.typeList.index("Electric"), poke.typeList.index("Water")),
	# 	(poke.typeList.index("Steel"), poke.typeList.index("Psychic"))
	# ]
	# print poke.scoreTeam(proTeam)
	# print poke.scoreTeam(cathyTeam)
	# print "\n"
	# poke.bruteforce(fixed=AnthonyTeam[:2])
	poke.bruteforce()