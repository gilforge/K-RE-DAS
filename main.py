############
# K-RE-DAS #
############
# Author = Gilles Aubin
# Website = gilles-aubin.net
# Version = 1.1.0

import pygame
import random

splash_image = pygame.image.load('img/splash_windows.png')  # Assurez-vous que l'image est dans le bon répertoire

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

#########
# SCORE #
#########

# Lecture ou création du fichier de score
def get_high_score():
    try:
        with open('high_score.txt', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

# Sauvegarde du score
def save_high_score(high_score):
    with open('high_score.txt', 'w') as f:
        f.write(str(high_score))

# Charger la variable score avec celui contenu dans le fichier
high_score = get_high_score()


###############
# ALIGNEMENTS #
###############

def check_alignments(grid):
    to_delete = []
    global score
    for i in range(10):
        for j in range(10):
            # Vérifier l'alignement horizontal
            if j <= 6:
                k = 0
                while j+k+1 < 10 and grid[i][j] is not None and grid[i][j] == grid[i][j+k+1]:
                    k += 1
                if k >= 3:
                    for l in range(k+1):
                        to_delete.append((i, j + l))
                    score += 4  # Ajouter 4 points pour chaque alignement
            # Vérifier l'alignement vertical
            if i <= 6:
                k = 0
                while i+k+1 < 10 and grid[i][j] is not None and grid[i][j] == grid[i+k+1][j]:
                    k += 1
                if k >= 3:
                    for l in range(k+1):
                        to_delete.append((i + l, j))
                    score += 4  # Ajouter 4 points pour chaque alignement
    # print(f"Nombre d'alignements trouvés : {len(alignments)}")
    return to_delete

# Fonction qui dessine la grille
def draw_grid():
    for i in range(10):
        for j in range(10):
            symbol = grid[i][j]
            if symbol is not None:
                pos = positions[i][j]
                symbol_size = symbols[symbol].get_size()  # Obtenez la taille du symbole
                centered_pos = (pos[0] + cell_size // 2 - symbol_size[0] // 2, pos[1] + cell_size // 2 - symbol_size[1] // 2)
                window.blit(symbols[symbol], centered_pos)
                if (i, j) == selected_pos1:  # If this is the selected symbol
                    pygame.draw.rect(window, (0, 0, 0), (grid_x + cell_x * cell_size, grid_y + cell_y * cell_size, cell_size, cell_size), 2)

                # Si le symbole est à supprimer, dessinez une surbrillance
                if (i, j) in to_delete:
                    pygame.draw.rect(window, (255, 255, 255), (pos[0], pos[1], cell_size, cell_size), 3)


#########
# SCORE #
#########

# Ecrire le high_score
def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    return high_score

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


###########
# BOUTONS #
###########


# >>>>>> BOUTON RESET HIGH SCORE

# Détecter le clic sur le high score
def click_on_button_HS(mouse_pos):
    if textHighScore_X - 10 < mouse_pos[0] < (textHighScore_X - 10 + 100) and textHighScore_Y < mouse_pos[1] < (textHighScore_Y + 40): 
        return True
    return False


# >>>>>> BOUTON NOUVEAU

# Variables du bouton NOUVEAU
width_new = 152
height_new = 40
posX_new = 58
posY_new = 590
posX_text_new = posX_new + 10
posY_text_new = posY_new + 5

def draw_button_new():
    pygame.draw.rect(window, color_White, (posX_new, posY_new, width_new, height_new),1)
    font_new = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text_new = font_new.render("Nouveau", True, color_White) 
    window.blit(text_new, (posX_text_new, posY_text_new)) 

# Détecter le clic sur le bouton Nouveau
def click_on_button_new(mouse_pos):
    if posX_new < mouse_pos[0] < (posX_new + width_new) and posY_new < mouse_pos[1] < (posY_new + height_new): 
        return True
    return False


# >>>>>> BOUTON AIDE

# Variables du bouton AIDE
width_help = 152
height_help = 40
posX_help = posX_new + width_new + 10
posY_help = 590
posX_text_help = posX_help + 10
posY_text_help = posY_help + 5

def draw_button_help():
    pygame.draw.rect(window, color_White, (posX_help, posY_help, width_help, height_help), 1)
    font_help = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text_help = font_help.render("Aide", True, color_White)
    window.blit(text_help, (posX_text_help, posY_text_help))

# Détecter le clic sur le bouton Aide
def click_on_button_help(mouse_pos):
    if posX_help < mouse_pos[0] < (posX_help + width_help) and posY_help < mouse_pos[1] < (posY_help + height_help):
        print(f"{showing_help} | BOUTON AIDE")
        return True
    return False


# >>>>>> BOUTON QUITTER

# Variables du bouton QUITTER
width_quit = 152
height_quit = 40
posX_quit = posX_help + width_help + 10
posY_quit = 590
posX_text_quit = posX_quit + 10
posY_text_quit = posY_quit + 5

def draw_button_quit():
    pygame.draw.rect(window, color_White, (posX_quit, posY_quit, width_quit, height_quit),1)
    font_quit = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text_quit = font_quit.render("Quitter", True, color_White) 
    window.blit(text_quit, (posX_text_quit, posY_text_quit)) 

# Détecter le clic sur le bouton Nouveau
def click_on_button_quit(mouse_pos):
    if posX_quit < mouse_pos[0] < (posX_quit + width_quit) and posY_quit < mouse_pos[1] < (posY_quit + height_quit): 
        return True
    return False


# >>>>>> BOUTON FERMER

# Variables du bouton FERMER
width_close = 152
height_close = 40
posX_close = posX_new + width_new + 10
posY_close = 590
posX_text_close = posX_close + 10
posY_text_close = posY_close + 5

# Dessiner le bouton Fermer
def draw_button_close():
    pygame.draw.rect(window, color_White, (posX_close, posY_close, width_close, height_close), 1)
    font_close = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 20)
    text_close = font_close.render("Fermer", True, color_White)
    window.blit(text_close, (posX_text_close, posY_text_close))

# Détecter le clic sur le bouton Fermer
def click_on_button_close(mouse_pos):
    if posX_close < mouse_pos[0] < (posX_close + width_close) and posY_close < mouse_pos[1] < (posY_close + height_close):
        return True
    return False


##############
# ECRAN AIDE #
##############

# Afficher l'écran d'aide
def show_help_screen():
    help_image = pygame.image.load('img/aide.jpg')
    window.blit(help_image, (0, 0))
    draw_button_close()
    pygame.display.flip()


#################
# SPLASH SCREEN #
#################

# Transition entre 2 images
def fade_between_images(image1, image2):
    for i in range(256):
        alpha = i  # Alpha pour l'image1
        beta = 255 - i  # Alpha pour l'image2

        # Créez une copie temporaire des images avec les valeurs alpha appropriées
        splash_temp = image2.copy()
        game_temp = image1.copy()
        splash_temp.set_alpha(alpha)
        game_temp.set_alpha(beta)

        # Dessinez les images avec les valeurs alpha
        window.blit(splash_temp, (0, 0))
        window.blit(game_temp, (0, 0))

        # Mettez à jour l'affichage
        pygame.display.flip()

        # Attendez un peu pour voir l'effet de fondu
        pygame.time.wait(10)  # Attendre 10 millisecondes

# Utilisation de la fonction
splash_image = pygame.image.load('img/splash_windows.png')
game_image = pygame.image.load('img/tapis.jpg')
fade_between_images(splash_image, game_image)

# Variable pour suivre le symbole actuellement sélectionné et sa position
selected_symbol1 = None
selected_pos1 = None
selected_symbol2 = None
selected_pos2 = None


#####################
# BOUCLE PRINCIPALE #
#####################

running = True
showing_help = False

while running:
    if showing_help:
        show_help_screen()
        pygame.display.flip()

        # Boucle interne pour attendre un clic de souris
        while showing_help:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    showing_help = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if click_on_button_close(mouse_pos):
                        showing_help = False

        continue  # Continue à la prochaine itération de la boucle, en sautant le reste du code

    # Remplir l'écran avec la couleur de fond
    image_fond = pygame.image.load("img/tapis.jpg")
    fond = pygame.transform.scale(image_fond, window_size)
    window.blit(fond,(0,0))

    # Titre
    fontTitle = pygame.font.Font("font/JetBrainsMono-ExtraBold.ttf", 36)
    textTitle = fontTitle.render(game_title, True, color_White)
    window.blit(textTitle, (70,10))

    # Nom de l'auteur
    fontAuthor = pygame.font.Font("font/JetBrainsMono-Light.ttf", 12)
    textAuthor = fontAuthor.render(game_author, True, color_White)
    window.blit(textAuthor, (70,50))  # -30 pour le rapprocher du titre

    # Score le plus élevé
    textHighScore_X = 300
    textHighScore_Y = 15
    fontHighScore = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 32)
    textHighScore = fontHighScore.render(f"{high_score:04}", True, color_White)
    window.blit(textHighScore, (textHighScore_X,textHighScore_Y))
    pygame.draw.rect(window, color_White, (textHighScore_X - 10,textHighScore_Y,100,40), 2)

    # Score
    fontScore = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 32)
    textScore = fontScore.render(f"{score:04}", True, color_White)
    window.blit(textScore, (450,15))

    draw_button_new()
    draw_button_help()
    draw_button_quit()

    to_delete = []

    # Dessiner la grille pour qu'elle soit belle
    for i in range(10):
        for j in range(10):
            symbol = grid[i][j]
            if symbol is not None:
                pos = positions[i][j]
                symbol_size = symbols[symbol].get_size()  # Obtenez la taille du symbole
                centered_pos = (pos[0] + cell_size // 2 - symbol_size[0] // 2, pos[1] + cell_size // 2 - symbol_size[1] // 2)
                window.blit(symbols[symbol], centered_pos)
                if (i, j) == selected_pos1:  # If this is the selected symbol
                    pygame.draw.rect(window, (0, 0, 0), (grid_x + cell_x * cell_size, grid_y + cell_y * cell_size, cell_size, cell_size), 2)

                    # Si le symbole est à supprimer, dessinez une surbrillance
                    if (i, j) in to_delete:
                        pygame.draw.rect(window, (255, 255, 255), (pos[0], pos[1], cell_size, cell_size), 3)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Parcourir tous les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            if showing_help:
                # Gestion des clics sur l'écran d'aide
                if click_on_button_close(mouse_pos):
                    showing_help = False
                continue  # Continue à la prochaine itération pour éviter de traiter d'autres clics

            # Gestion des clics sur l'écran de jeu principal
            if click_on_button_new(mouse_pos):
                high_score = update_high_score(score, high_score)
                reset_game()

            elif click_on_button_quit(mouse_pos):
                high_score = update_high_score(score, high_score)
                running = False

            elif click_on_button_help(mouse_pos):
                showing_help = True
                show_help_screen()

            if click_on_button_HS(mouse_pos):
                high_score = 0
                save_high_score(high_score)
                # print(f"RESET HS")

            cell_x = (mouse_pos[0] - grid_x) // cell_size
            cell_y = (mouse_pos[1] - grid_y) // cell_size

            if 0 <= cell_x < 10 and 0 <= cell_y < 10 and grid[cell_y][cell_x] is not None:
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
                        print(f"Alignments found: {alignments},\n {score}")
                        # score += len(alignments) // 4  # Augmenter le score pour chaque alignement trouvé

                        # Mettre en surbrillance les symboles à supprimer
                        for pos in alignments:
                            if len(pos) == 2:
                                i, j = pos
                                pygame.draw.rect(window, color_White, (positions[i][j][0], positions[i][j][1], cell_size, cell_size), 1)

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

high_score = update_high_score(score, high_score)

# Quitter Pygame une fois la boucle terminée
pygame.quit()