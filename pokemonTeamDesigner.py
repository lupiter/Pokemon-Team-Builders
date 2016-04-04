from numpy import array, zeros, sum, std
import csv
import sys
import random
from math import floor
import sqlite3

class Pokemon:
	def __init__(self, row=None):
		if row:
			self.dex = row[0]
			self.name = row[1].replace('\n', '/')
			self.types = row[2].replace('\n', '/')
			self.total = row[3]
			self.hp = row[4]
			self.attack = row[5]
			self.defence = row[6]
			self.specialAttack = row[7]
			self.specialDefence = row[8]
			self.speed = row[9]
			self.type1 = row[10]
			self.type2 = row[11]
	def __str__(self):
		return "{0}\t{1}\t{2}".format(self.dex, self.name.ljust(25, ' '), self.types)


class TeamBuilder:
	def __init__(self):
		self.pokemonDB = sqlite3.connect("pokemon.db").cursor()

		self.typeList = ["NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS",  "ICE", "FIGHTING", \
			"POISON", "GROUND",  "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DRAGON",  "DARK", "STEEL", "FAIRY"]
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

	def randomPokemon(self, currentPokemon):
		notTypes = []
		for pokemon in currentPokemon:
			if pokemon.type1 not in notTypes and pokemon.type1 is not None:
				notTypes.append(pokemon.type1)
			if pokemon.type2 not in notTypes and pokemon.type2 is not None:
				notTypes.append(pokemon.type2)
		notTypes = ", ".join([str(x) for x in notTypes])
		query = "select * from pokemon where type1 not in (" + notTypes + ") and type2 not in (" + notTypes + ") and total > 450 and not legendary order by random() limit 1;"
		# print query
		try:
			self.pokemonDB.execute(query)
		except sqlite3.OperationalError as e:
			print e
			print query
			return
		return Pokemon(self.pokemonDB.fetchone())

	def randomTeam(self, fixed=[]):
		team = fixed
		for pokeCount in range(len(fixed), 6):
			pokemon = self.randomPokemon(team)
			team.append(pokemon)
		return team

	def typeIndex(self, type1):
		return self.typeList.index(type1)

	def attack(self, pokeType, pokeType2):
		attack = self.matrix[pokeType-1, :].copy()
		if pokeType2 and pokeType2 != pokeType:
			attack = attack * self.matrix[pokeType2-1, :].copy()
		return attack

	def pokeAttackStats(self, pokemon):
		return float(pokemon.attack)/190 * float(pokemon.specialAttack)/194 * float(pokemon.speed)/180

	def pokeDefenceStats(self, pokemon):
		return float(pokemon.defence) + float(pokemon.specialDefence) + float(pokemon.hp)

	def defend(self, pokeType, pokeType2):
		defence = self.matrix[:, pokeType-1].copy()
		if pokeType2 and pokeType2 != pokeType:
			defence = defence * self.matrix[:, pokeType2-1].copy()
		return defence

	def scoreTeam(self, team, pprint=False):
		totalAttack = zeros(18)
		totalDefence = zeros(18)
		for pokemon in team:
			attack = self.attack(pokemon.type1, pokemon.type2) * self.pokeAttackStats(pokemon)
			totalAttack = totalAttack + attack
			defence = self.defend(pokemon.type1, pokemon.type2) / self.pokeDefenceStats(pokemon) * 10
			totalDefence = totalDefence + defence

		if pprint:
			print "Attack: " + " ".join(["{0:.2f}".format(x) for x in totalAttack])
			print "Defence: " + " ".join(["{0:.2f}".format(x) for x in totalDefence])
		score = sum(totalAttack - totalDefence) - (len(totalAttack) * (std(totalAttack) + std(totalDefence)))
		if pprint:
			print "Diversity: {0:.2f}".format(len(totalAttack) * (std(totalAttack) + std(totalDefence)))
			print "Total: {0:.2f}".format(score)
		return floor(score)

	def bruteforce(self, timeout=10000, fixed=[]):
		maxTeam = self.randomTeam(fixed)
		oldScore = self.scoreTeam(maxTeam)
		while timeout:
			sys.stdout.write(str(timeout) + "\r")
			newTeam = self.randomTeam(fixed)
			newScore = self.scoreTeam(newTeam)
			if newScore > oldScore:
				maxTeam = newTeam
				oldScore = newScore
			timeout -= 1
		sys.stdout.write(" "*20 + "\r")
		for pokemon in maxTeam:
			print pokemon
		self.scoreTeam(maxTeam, pprint=True)

if __name__ == '__main__':
	poke = TeamBuilder()
	poke.bruteforce()

