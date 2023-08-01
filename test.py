import pygame
import random

# Initialiser Pygame
pygame.init()

# Définir les variables du jeu
# set the pygame window name
pygame.display.set_caption('K-RE-DAS')
game_title = "K-RE-DAS"
game_author = "by Gilles Aubin"
score = 0
margin = 50  # Espace pour le titre et le score
window_size = (600, 600)  # Taille de la fenêtre
cell_size = (window_size[0] - 2 * margin) // 10  # Taille de chaque cellule de la grille

# Créer la fenêtre
window = pygame.display.set_mode(window_size)

# Créer des surfaces pour les symboles
# pique = pygame.Surface((cell_size, cell_size))
# pique.fill((255, 0, 0))  # Rouge
# carreau = pygame.Surface((cell_size, cell_size))
# carreau.fill((0, 255, 0))  # Vert
# coeur = pygame.Surface((cell_size, cell_size))
# coeur.fill((0, 0, 255))  # Bleu
# trefle = pygame.Surface((cell_size, cell_size))
# trefle.fill((255, 255, 0))  # Jaune

# # # Stocker les surfaces dans un dictionnaire pour un accès facile
# symbols = {
#     "pique": pique,
#     "carreau": carreau,
#     "coeur": coeur,
#     "trefle": trefle
# }

# Charger les images
symbols = {
    "pique": pygame.image.load('img/pique.png'),
    "carreau": pygame.image.load('img/carreau.png'),
    "coeur": pygame.image.load('img/coeur.png'),
    "trefle": pygame.image.load('img/trefle.png')
}

# Définir les coordonnées de la grille et du cadre
grid_x = 50
grid_y = 75

# Créer une grille de 10x10 et la remplir de symboles aléatoires
grid = []
for i in range(10):
    row = []
    for j in range(10):
        # Remplir la grille avec des symboles aléatoires
         row.append(random.choice(list(symbols.keys())))
    grid.append(row)

# Créer une grille vide pour les positions des symboles
positions = []
for i in range(10):
    row = []
    for j in range(10):
        # La position initiale est basée sur l'indice de la cellule
        row.append((grid_x + j * cell_size, grid_y + i * cell_size))
    positions.append(row)

# Variable pour suivre le symbole actuellement sélectionné et sa position
selected_symbol1 = None
selected_pos1 = None
selected_symbol2 = None
selected_pos2 = None

# Boucle principale du jeu
running = True
while running:
    # Remplir l'écran avec la couleur de fond
    image_fond = pygame.image.load("img/tapis.jpg")
    fond = image_fond.convert()
    window.blit(fond,(0,0))

    # Dessiner le titre
    fontTitle = pygame.font.Font("font/JetBrainsMono-ExtraBold.ttf", 36)
    textTitle = fontTitle.render(game_title, True, (255, 255, 255))
    window.blit(textTitle, (margin, margin // 2 - textTitle.get_height() // 2))

    # Dessiner le nom de l'auteur
    fontAuthor = pygame.font.Font("font/JetBrainsMono-Light.ttf", 12)
    textAuthor = fontAuthor.render(game_author, True, (255, 255, 255))
    window.blit(textAuthor, (margin, margin // 2 + textTitle.get_height() - 30))  # -30 pour le rapprocher du titre

    # Dessiner le score
    fontScore = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 24)
    textScore = fontScore.render(str(score), True, (255, 255, 255))
    window.blit(textScore, (window_size[0] - textScore.get_width() - margin, margin // 2 - textScore.get_height() // 2 ))

    # Dessiner le cadre
    # pygame.draw.rect(window, (0, 0, 0), (grid_x, grid_y, 10 * cell_size, 10 * cell_size), 2)

    # Dessiner la grille
    for i in range(10):
        for j in range(10):
            symbol = grid[i][j]
            if symbol is not None:
                pos = positions[i][j]
                window.blit(symbols[symbol], pos)
                if (i, j) == selected_pos1:  # If this is the selected symbol
                    pygame.draw.rect(window, (0, 0, 0), (grid_x + cell_x * cell_size, grid_y + cell_y * cell_size, cell_size, cell_size), 2)
                    # pygame.draw.rect(window, (0, 0, 0), (pos[0], pos[1], cell_size, cell_size), 2)  # Draw a black border

    # Dessiner le contour
    # pygame.draw.rect(window, (250, 250, 250), (grid_x, grid_y, 10 * cell_size, 10 * cell_size), 2)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Parcourir tous les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            cell_x = (mouse_pos[0] - grid_x) // cell_size
            cell_y = (mouse_pos[1] - grid_y) // cell_size
            print(cell_x)
            print(cell_y)
            if 0 <= cell_x < 10 and 0 <= cell_y < 10:  # Check if the click is within the grid
                if selected_symbol1 is None:  # If no symbol is selected yet
                    selected_symbol1 = grid[cell_y][cell_x]
                    selected_pos1 = (cell_x, cell_y)
                else:  # If a symbol is already selected
                    selected_symbol2 = grid[cell_y][cell_x]
                    selected_pos2 = (cell_x, cell_y)
                    # Swap the symbols
                    grid[selected_pos1[1]][selected_pos1[0]] = selected_symbol2
                    grid[selected_pos2[1]][selected_pos2[0]] = selected_symbol1
                    # Reset the selected symbols and positions
                    selected_symbol1 = None
                    selected_pos1 = None
                    selected_symbol2 = None
                    selected_pos2 = None

# Quitter Pygame une fois la boucle terminée
pygame.quit()