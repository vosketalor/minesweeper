try:
	from grid import Grid
	from cell import Cell
	import os
	import pygame
	from math import floor

except Exception as e:
	print("[ERROR] : \n{}".format(e))

else:

	os.environ['SDL_VIDEO_CENTERED'] = '1'

	pygame.init()
	pygame.display.set_caption("MINESWEEPER - Ready to play !")

	length, height = 15, 15
	
	font = pygame.font.SysFont(None, 24)

	window = pygame.display.set_mode((length*25, height*25))
	icon = pygame.image.load("./assets/icon.png").convert_alpha()
	pygame.display.set_icon(icon)

	clock = pygame.time.Clock()
	pygame.display.flip()

	board = Grid(length, height)
	board.remplir(floor((15/100)*(length*height)))

	end = False
	while not end:
		board.display(window, font)

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed():
					if pygame.mouse.get_pressed()[0] == 1:
						x, y = event.pos
						clicked_cell = board.board[floor(y/25)][floor(x/25)]
						if clicked_cell.flag == False:
							if clicked_cell.value == "×":
								pygame.display.set_caption("MINESWEEPER - Kabooom!")
								board.game_over()
							else:
								if clicked_cell.value == " ":
									board.flood_fill([floor(y/25), floor(x/25)])
								else:
									clicked_cell.display = True
								if board.game_end():
									pygame.display.set_caption("MINESWEEPER - Congratulations !")
					elif pygame.mouse.get_pressed()[2] == 1:
						x, y = event.pos
						clicked_cell = board.board[floor(y/25)][floor(x/25)]
						if clicked_cell.display == False:
							if clicked_cell.flag == True:
								clicked_cell.flag = False
							else:
								clicked_cell.flag = True
						if board.game_end():
							pygame.display.set_caption("MINESWEEPER - Congratulations !")
			if event.type == pygame.QUIT:
				end = True

		pygame.display.update()
		clock.tick(60)

finally:
	pygame.quit()