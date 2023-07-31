import pygame
import random

# Initialiser Pygame
pygame.init()

# Charger les images
pique = pygame.image.load('img/pique.png')
carreau = pygame.image.load('img/carreau.png')
coeur = pygame.image.load('img/coeur.png')
trefle = pygame.image.load('img/trefle.png')

# Stocker les images dans un dictionnaire pour un accès facile
symbols = {
    "pique": pique,
    "carreau": carreau,
    "coeur": coeur,
    "trefle": trefle
}

# Créer une grille vide de 10x10
grid = []
for i in range(10):
    row = []
    for j in range(10):
        row.append(None)  # None représente une cellule vide
    grid.append(row)

# Remplir la grille avec des symboles aléatoires
for i in range(10):
    for j in range(10):
        grid[i][j] = random.choice(list(symbols.keys()))

# Définir la taille de la fenêtre
window_size = (400, 400)

# Créer la fenêtre
window = pygame.display.set_mode(window_size)

# Définir une couleur pour le fond (RGB)
background_color = (200, 200, 200)  # Gris

# Taille de chaque cellule de la grille
cell_size = 40

# Variable pour suivre le symbole actuellement sélectionné et sa position
selected_symbol = None
selected_pos = None

# Boucle principale du jeu
running = True
while running:
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
            cell_x = mouse_pos[0] // cell_size
            cell_y = mouse_pos[1] // cell_size
            # Sélectionner le symbole et sa position
            selected_symbol = grid[cell_y][cell_x]
            selected_pos = (cell_x, cell_y)
        # Si l'événement est un mouvement de souris
        elif event.type == pygame.MOUSEMOTION:
            # Si un symbole est sélectionné
            if selected_symbol is not None:
                # Déplacer le symbole à la position de la souris
                selected_pos = event.pos
        # Si l'événement est le relâchement du bouton de la souris
        elif event.type == pygame.MOUSEBUTTONUP:
            # Si un symbole est sélectionné
            if selected_symbol is not None:
                # Calculer l'indice de la cellule la plus proche
                cell_x = min(max(round((selected_pos[0] + cell_size // 2) / cell_size), 0), 9)
                cell_y = min(max(round((selected_pos[1] + cell_size // 2) / cell_size), 0), 9)
                # Échanger le symbole sélectionné avec le symbole de la cellule la plus proche
                grid[selected_pos[1]//cell_size][selected_pos[0]//cell_size], grid[cell_y][cell_x] = grid[cell_y][cell_x], grid[selected_pos[1]//cell_size][selected_pos[0]//cell_size]
                # Réinitialiser le symbole sélectionné et sa position
                selected_symbol = None
                selected_pos = None

    # Remplir l'écran avec la couleur de fond
    window.fill(background_color)

    # Dessiner la grille
    for i in range(10):
        for j in range(10):
            symbol = grid[i][j]
            if symbol is not None:
                # Utiliser la position de la grille de positions
                pos = (j * cell_size, i * cell_size)
                window.blit(symbols[symbol], pos)

    # Si un symbole est sélectionné, le dessiner à la position de la souris
    if selected_symbol is not None:
        window.blit(symbols[selected_symbol], (selected_pos[0] - cell_size // 2, selected_pos[1] - cell_size // 2))

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame une fois la boucle terminée
pygame.quit()
