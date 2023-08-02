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
window_size = (600, 650)  # Taille de la fenêtre
cell_size = (window_size[0] - 2 * margin) // 10  # Taille de chaque cellule de la grille

# Couleurs A DEFINIR
color_Black = (0, 0, 0)
color_White = (204, 204, 204)

# Créer la fenêtre
window = pygame.display.set_mode(window_size) # fenêtré
# window = pygame.display.set_mode(window_size, pygame.SCALED|pygame.FULLSCREEN) # plein écran

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

# Fonction qui vérifie l'alignement de 4 symboles
def check_alignments(grid):
    to_delete = []
    global score
    for i in range(10):
        for j in range(10):
            # Vérifier l'alignement horizontal
            if j <= 6:
                for k in range(1, 7):
                    # if j+k >= 10 or grid[i][j] is None or (j+k < 10 and grid[i][j] != grid[i][j+k]):
                    if j+k >= 10 or grid[i][j] is None or grid[i][j] != grid[i][j+k]:
                        break
                    if k >= 3:
                        for l in range(4):
                            to_delete.append((i, j + l))
                            print(f"Boucle 1 > i = {i} | j = {j} | k = {k} | HORZ")
                        score += k
            # Vérifier l'alignement vertical
            if i <= 6:
                for k in range(1, 7):
                    # if j+k >= 10 or grid[i][j] is None or (j+k < 10 and grid[i][j] != grid[i][j+k]):
                    if j+k >= 10 or grid[i][j] is None or grid[i][j] != grid[i+k][j]:
                        break
                    if k >= 3:
                        for l in range(4):
                            to_delete.append((i + l, j))
                            print(f"Boucle 2 > i = {i} | j = {j} | k = {k} | VERT")
                        score += k
    return to_delete

# Fonction qui dessine la grille
def draw_grid():
    for i in range(10):
        for j in range(10):
            symbol = grid[i][j]
            if symbol is not None:
                pos = positions[i][j]
                window.blit(symbols[symbol], pos)
                if (i, j) == selected_pos1:  # If this is the selected symbol
                    pygame.draw.rect(window, (0, 0, 0), (grid_x + cell_x * cell_size, grid_y + cell_y * cell_size, cell_size, cell_size), 2)

                # Si le symbole est à supprimer, dessinez une surbrillance
                if (i, j) in to_delete:
                    pygame.draw.rect(window, (255, 255, 255), (pos[0], pos[1], cell_size, cell_size), 3)

# Dessiner le bouton
width_new = 200
height_new = 40
posX_new = 50
posY_new = 590
posX_text_new = posX_new + 10
posY_text_new = posY_new + 5

def draw_button():
    pygame.draw.rect(window, color_White, (posX_new, posY_new, width_new, height_new),1)
    font_new = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text_new = font_new.render("Nouveau", True, color_White) 
    window.blit(text_new, (posX_text_new, posY_text_new)) 

# Détecter le clic sur le bouton
def click_on_button(mouse_pos):
    if posX_new < mouse_pos[0] < (posX_new + width_new) and posY_new < mouse_pos[1] < (posY_new + height_new): 
        return True
    return False

# Réinitialiser le jeu
def reset_game():
    global grid, score
    grid = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append(random.choice(list(symbols.keys())))
        grid.append(row)
    score = 0

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
    fond = pygame.transform.scale(image_fond, window_size)
    # fond = image_fond.convert()
    window.blit(fond,(0,0))

    # Dessiner le titre
    fontTitle = pygame.font.Font("font/JetBrainsMono-ExtraBold.ttf", 36)
    textTitle = fontTitle.render(game_title, True, (200, 200, 200))
    window.blit(textTitle, (margin, margin // 2 - textTitle.get_height() // 2))

    # Dessiner le nom de l'auteur
    fontAuthor = pygame.font.Font("font/JetBrainsMono-Light.ttf", 12)
    textAuthor = fontAuthor.render(game_author, True, (200, 200, 200))
    window.blit(textAuthor, (margin, margin // 2 + textTitle.get_height() - 30))  # -30 pour le rapprocher du titre

    # Dessiner le score
    fontScore = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 24)
    textScore = fontScore.render(str(score), True, (200, 200, 200))
    window.blit(textScore, (window_size[0] - textScore.get_width() - margin, margin // 2 - textScore.get_height() // 2 ))

    draw_button()
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     elif event.type == pygame.MOUSEBUTTONUP:
    #         mouse_pos = pygame.mouse.get_pos()
    #         if click_on_button(mouse_pos):
    #             reset_game()

    # Dessiner le cadre
    # pygame.draw.rect(window, (0, 0, 0), (grid_x, grid_y, 10 * cell_size, 10 * cell_size), 2)

    to_delete = []

    # Dessiner la grille pour qu'elle soit belle
    for i in range(10):
        for j in range(10):
            symbol = grid[i][j]
            if symbol is not None:
                pos = positions[i][j]
                window.blit(symbols[symbol], pos)
                if (i, j) == selected_pos1:  # If this is the selected symbol
                    pygame.draw.rect(window, (0, 0, 0), (grid_x + cell_x * cell_size, grid_y + cell_y * cell_size, cell_size, cell_size), 2)

                    # Si le symbole est à supprimer, dessinez une surbrillance
                    if (i, j) in to_delete:
                        pygame.draw.rect(window, (255, 255, 255), (pos[0], pos[1], cell_size, cell_size), 3)

    # Dessiner le contour
    # pygame.draw.rect(window, (250, 250, 250), (grid_x, grid_y, 10 * cell_size, 10 * cell_size), 2)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Parcourir tous les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            if click_on_button(mouse_pos):
                reset_game()

            cell_x = (mouse_pos[0] - grid_x) // cell_size
            cell_y = (mouse_pos[1] - grid_y) // cell_size
            print(f"Mouse up at {cell_x}, {cell_y}")

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

                    draw_grid()  # Redraw the grid after swapping the symbols
                    pygame.display.flip()  # Update the display to show the swapped symbols

                    # Reset the selected symbols and positions
                    selected_symbol1 = None
                    selected_pos1 = None
                    selected_symbol2 = None
                    selected_pos2 = None

                    # Vérifier les alignements après le mouvement
                    alignments = check_alignments(grid)
                    if alignments:  # Si la liste n'est pas vide
                        print(f"Alignments found: {alignments}")
                        # score += len(alignments) // 4  # Augmenter le score pour chaque alignement trouvé

                        # Mettre en surbrillance les symboles à supprimer
                        for pos in alignments:
                            if len(pos) == 2:
                                i, j = pos
                                pygame.draw.rect(window, (255, 255, 255), (positions[i][j][0], positions[i][j][1], cell_size, cell_size), 3)

                        pygame.display.flip()  # Mettre à jour l'affichage pour montrer la surbrillance
                        pygame.time.wait(500)  # Attendre 500 millisecondes (0.5 seconde)

                        # Supprimer les symboles à supprimer de la grille
                        for pos in alignments:
                            if len(pos) == 2:
                                i, j = pos
                                grid[i][j] = None
                        # Vider la liste alignments
                        alignments = None, None
                        draw_grid()
                        pygame.display.flip()  # Mettre à jour l'affichage pour montrer la surbrillance


# Quitter Pygame une fois la boucle terminée
pygame.quit()