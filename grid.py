from cell import Cell
from random import randint
import pygame

class Grid:

	def __init__(self, length, height):
		self.board = [[Cell() for k in range(height)] for i in range(length)]
		
	def generate(self, quota):
		mines = []
		while quota > 0:
			for i in range(len(self.board)):
				for k in range(len(self.board[i])):
					if quota > 0:
						if self.board[i][k].value != "×":
							random_value = randint(0, 100)
							if random_value > 99:
								quota -= 1
								self.board[i][k].value = "×"
								mines.append((i, k))
							else:
								if self.board[i][k] == " ":
									self.board[i][k].value = " "

		for coords in mines:
			for i in range(max(0, coords[0]-1), min(len(self.board), coords[0]+2)):
				for k in range(max(0, coords[1]-1), min(len(self.board[i]), coords[1]+2)):
					if self.board[i][k].value == " ":
						self.board[i][k].value = "1"
					else:
						if self.board[i][k].value != "×":
							self.board[i][k].value = str(int(self.board[i][k].value)+1)
	
	def display(self, window, font):
		couleurs = { "×": (0, 0, 0), "1": (0, 0, 255), "2": (0, 128, 0), "3": (255, 0, 0), "4": (200, 0, 200), "5": (255, 255, 0), "6": (0, 255, 255), "7": (106, 230, 201), "8": (106, 230, 201), " ": (255, 255, 255)}
		cell_false = pygame.image.load("./assets/cell_false.png")
		cell_true = pygame.image.load("./assets/cell_true.png")
		cell_flag = pygame.image.load("./assets/cell_flag.png")

		for i in range(len(self.board)):
			for k in range(len(self.board[i])):
				if self.board[i][k].display == True:
					pygame.draw.rect(window, (192, 192, 192), (25*k, 25*i, 25, 25))
					texte = font.render(self.board[i][k].value, True, couleurs[self.board[i][k].value])
					window.blit(cell_true, (25*k, 25*i))
					window.blit(texte, (25*k+8, 25*i+5))
				else:
					if self.board[i][k].flag == True:
						window.blit(cell_flag, (25*k, 25*i))
					else:
						window.blit(cell_false, (25*k, 25*i))
	
	def game_end(self):
		for i in range(len(self.board)):
			for k in range(len(self.board[i])):
				if (self.board[i][k].value == "×" and self.board[i][k].flag == False) or (self.board[i][k].value != "×" and self.board[i][k].flag == True) or (self.board[i][k].value != "×" and self.board[i][k].display != True):
					return False
		return True


	def game_over(self):
		for i in range(len(self.board)):
			for k in range(len(self.board[i])):
				self.board[i][k].display = True

	def flood_fill(self, coords):
		movements = [[0,-1], [0,1], [-1,0], [1,0], [-1,-1], [-1,1], [1,1], [1,-1]]
		remains_to_be_done = [coords]
		cell_edges = []
		while len(remains_to_be_done) > 0:
			current_cell = remains_to_be_done[0]
			del remains_to_be_done[0]
			self.board[current_cell[0]][current_cell[1]].display = True
			cell_edges.extend(correct_cell_edges(self, current_cell))
			for movement in movements:
				neighbour_cell = [current_cell[0]+movement[0], current_cell[1]+movement[1]]
				if correct_cell(self, neighbour_cell):
					remains_to_be_done.append(neighbour_cell)
		for k in range(len(cell_edges)):
			self.board[cell_edges[k][0]][cell_edges[k][1]].display = True

def correct_cell(grid, cell):
	return (0 <= cell[0] < len(grid.board)) and (0 <= cell[1] < len(grid.board[0])) and (grid.board[cell[0]][cell[1]].value == " ") and (grid.board[cell[0]][cell[1]].display == False)

def correct_cell_edges(grid, cell):
	movements = [[0,-1],[0,1],[-1,0],[1,0],[-1,-1],[-1,1],[1,1],[1,-1]]
	cell_edges = []
	cell_visited = cell
	for movement in movements:
		cell = [cell_visited[0]+movement[0], cell_visited[1]+movement[1]]
		if 0 <= cell[0] < len(grid.board) and  0 <= cell[1] < len(grid.board[0]):
			if grid.board[cell[0]][cell[1]].value != " " and grid.board[cell[0]][cell[1]].value != "X":
				cell_edges.append(cell)
	return cell_edges
