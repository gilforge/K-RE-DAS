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

# Charger les images
symbols = {
    "pique": pygame.image.load('img/pique.png'),
    "carreau": pygame.image.load('img/carreau.png'),
    "coeur": pygame.image.load('img/coeur.png'),
    "trefle": pygame.image.load('img/trefle.png')
}

# Créer une grille vide de 10x10
grid = []
for i in range(10):
    row = []
    for j in range(10):
        row.append(random.choice(list(symbols.keys())))  # Remplir la grille avec des symboles aléatoires
    grid.append(row)

# Variable pour suivre le symbole actuellement sélectionné et sa position
selected_symbol = None
selected_pos = None

# Boucle principale du jeu
running = True
while running:
    # Remplir l'écran avec la couleur de fond
    window.fill((200, 200, 200))  # Gris

    # Dessiner le titre
    fontTitle = pygame.font.Font("font/JetBrainsMono-ExtraBold.ttf", 36)
    fontScore = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 24)
    fontAuthor = pygame.font.Font("font/JetBrainsMono-Light.ttf", 12)
    textTitle = fontTitle.render(game_title, True, (0, 0, 0))
    textAuthor = fontAuthor.render(game_author, True, (0, 0, 0))
    window.blit(textTitle, (window_size[0] // 2 - textTitle.get_width() // 2, margin // 2 - textTitle.get_height() // 2))
    window.blit(textAuthor, (window_size[0] // 2 - textAuthor.get_width() // 2, margin // 2 - textAuthor.get_height() // 2))

    # Dessiner le score
    textScore = fontScore.render("Score: " + str(score), True, (0, 0, 0))
    window.blit(textScore, (window_size[0] // 2 - textScore.get_width() // 2, window_size[1] - margin // 2 - textScore.get_height() // 2))

    # Dessiner le cadre
    pygame.draw.rect(window, (0, 0, 0), (margin, margin, window_size[0] - 2 * margin, window_size[1] - 2 * margin), 2)

    # Dessiner la grille
    for i in range(10):
        for j in range(10):
            symbol = grid[i][j]
            if symbol is not None:
                pos = (margin + j * cell_size, margin + i * cell_size)
                window.blit(symbols[symbol], pos)

    # Si un symbole est sélectionné, le dessiner à la position de la souris
    if selected_symbol is not None:
        window.blit(symbols[selected_symbol], (selected_pos[0] - cell_size // 2, selected_pos[1] - cell_size // 2))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Parcourir tous les événements
    for event in pygame.event.get():
        # Si l'événement est le fait de fermer la fenêtre, arrêter la boucle
        if event.type == pygame.QUIT:
            running = False
        # Si l'événement est un clic de souris
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Obtenir la position de la souris
            mouse_pos = pygame.mouse.get_pos()
            # Calculer l'indice de la cellule
            cell_x = (mouse_pos[0] - margin) // cell_size
            cell_y = (mouse_pos[1] - margin) // cell_size
            # Sélectionner le symbole et sa position
            selected_symbol = grid[cell_y][cell_x]
            selected_pos = (cell_x, cell_y)
        # Si l'événement est le relâchement du bouton de la souris
        elif event.type == pygame.MOUSEBUTTONUP:
            # Si un symbole est sélectionné
            if selected_symbol is not None:
                # Calculer l'indice de la cellule la plus proche
                cell_x = min(max(round((event.pos[0] + cell_size // 2) / cell_size), 0), 9)
                cell_y = min(max(round((event.pos[1] + cell_size // 2) / cell_size), 0), 9)
                # Échanger le symbole sélectionné avec le symbole de la cellule la plus proche
                temp = grid[selected_pos[1]//cell_size][selected_pos[0]//cell_size]
                grid[selected_pos[1]//cell_size][selected_pos[0]//cell_size] = grid[cell_y][cell_x]
                grid[cell_y][cell_x] = temp
                # Réinitialiser le symbole sélectionné et sa position
                selected_symbol = None
                selected_pos = None

# Quitter Pygame une fois la boucle terminée
pygame.quit()
