############
# K-RE-DAS #
############
# Author = Gilles Aubin
# Website = gilles-aubin.net
# Version = 1.2.0

import pygame
import random
import json

# Initialiser Pygame
pygame.init()


#############
# VARIABLES #
#############

# Définir les variables du jeu
game_title = "K-RE-DAS"
pygame.display.set_caption(game_title)

game_author = "by Gilles Aubin"
score = 0
margin = 50  # Espace pour le titre et le score
window_size = (600, 650)  # Taille de la fenêtre
cell_size = (window_size[0] - 2 * margin) // 10  # Taille de chaque cellule de la grille

color_Black = (0, 0, 0)
color_White = (204, 204, 204)

# Définir les coordonnées de la grille, du cadre et des cellules
grid_x = 50
grid_y = 75


##########
# IMAGES #
##########

splash_image = pygame.image.load('img/splash_windows.png')  # Assurez-vous que l'image est dans le bon répertoire
game_image = pygame.image.load('img/tapis.jpg')
symbols = {
    "pique": pygame.image.load('img/pique.png'),
    "carreau": pygame.image.load('img/carreau.png'),
    "coeur": pygame.image.load('img/coeur.png'),
    "trefle": pygame.image.load('img/trefle.png')
}
help_image = pygame.image.load('img/aide.jpg')
endgame_image = pygame.image.load('img/findejeu.jpg')
obstacle_image = pygame.image.load('img/obstacle.png')


###########
# NIVEAUX #
###########

# Lecture des informations du fichier config.json
def load_config_data() :
    try :
        with open('config/config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError :
        return None

config_data = load_config_data()

# Trouver le niveau avec une progression de 1
def load_progress(config_data):
    if config_data :
        current_level = next(level for level in config_data['config'] if level['progression'] == 1)
    return current_level

# Chargement des données de progression
current_level = load_progress(config_data)

# Charger les données du niveau en cours
levelToPlay = current_level['level']
current_objectif = current_level['objectif']
current_progress = current_level['progression']
current_meilleurScore = current_level['meilleurScore']
current_obstacles = current_level['obstacles']


def save_config_data(config_data):
    print(f"SAVE CONGIGDATA\n>>> config : {config_data}")
    with open('config/config.json', 'w') as file:
        json.dump(config_data, file, indent=4)

def load_next_level():
    global levelToPlay, current_level, current_objectif, current_meilleurScore, high_score

    print("LOADNEXTLEVEL")

    if levelToPlay < len(config_data['config']):  # Vérifier si ce n'est pas le dernier niveau

        levelToPlay += 1
        current_level = config_data['config'][levelToPlay-1]
        current_objectif = current_level['objectif']
        current_meilleurScore = current_level['meilleurScore']
        high_score = current_meilleurScore
        reset_game()
    else:
        show_endgame_screen()
        # Ajouter une boucle pour maintenir l'écran de fin de jeu à l'affichage
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or click_on_button_close(pygame.mouse.get_pos()):
                    return

# Fonction pour compter les symboles restants
def count_remaining_symbols(grid):
    count = 0
    for row in grid:
        for cell in row:
            if cell in symbols.keys():  # Vérifier si la cellule contient un symbole
                count += 1
    return count


#########
# SCORE #
#########

# Lecture du meilleur score du niveau
def get_high_score():
    global config_data
    # Récupérer le meilleur score du niveau actuel
    print(f"GET HIGHSCORE\n>>> meilleurScore : {current_meilleurScore}")

    return current_level['meilleurScore']


# Charger la variable score avec celui contenu dans le fichier
high_score = get_high_score()

# MISE A JOUR DU HIGH_SCORE > OK
def update_high_score():
    global high_score, score, config_data
    print(f"UPDATE HIGHSCORE\n>>> meilleurScore : {current_meilleurScore}")
    if score > current_level['meilleurScore']:
        current_level['meilleurScore'] = score
        save_config_data(config_data)

    return current_level['meilleurScore']


# REINITIALISER > OK
def reset_game():
    global config_data, grid, score
    grid = initialize_grid()
    score = 0
    print(f"RESSET GAME\n>>> {score}")
    return grid, score

# SAUVEGARDE PROGRESSION > OK
def save_progress(config_data):
    for level in config_data['config']:
        if level['level'] == current_level['level']:
            level['progression'] = 0
        elif level['level'] == current_level['level'] + 1:
            level['progression'] = 1
    save_config_data(config_data)
    print(f"SAVE PROGRESS\n>>> progression : {current_progress}")


# # SAUVEGARDE MEILLEUR SCORE > OK
# if config_data:
#     if score > current_level['meilleurScore']:
#         current_level['meilleurScore'] = score
#         save_progress(config_data)


#########################
# INITIALISER LA GRILLE #
#########################

def initialize_grid():
    global config_data
    grid = []
    symbol_counts = {"pique": 0, "carreau": 0, "coeur": 0, "trefle": 0}
    symbols_list = list(symbols.keys())

    for i in range(10):
        row = []
        for j in range(10):
            if any(obstacle['row'] == i and obstacle['col'] == j for obstacle in current_level['obstacles']):
                row.append('obstacle')  # Ajouter un obstacle
            else:
                # Choisir un symbole qui n'a pas encore été ajouté 25 fois
                available_symbols = [symbol for symbol in symbols_list if symbol_counts[symbol] < 25]
                chosen_symbol = random.choice(available_symbols)
                row.append(chosen_symbol)
                symbol_counts[chosen_symbol] += 1  # Incrémenter le compteur pour le symbole choisi
        grid.append(row)
    return grid

grid = initialize_grid()

# Créer une grille vide pour les positions des symboles
positions = []
for i in range(10):
    row = []
    for j in range(10):
        # La position initiale est basée sur l'indice de la cellule
        row.append((grid_x + j * cell_size, grid_y + i * cell_size))
    positions.append(row)


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
    return to_delete

# Fonction d'animation des échanges de symboles
def lerp(start, end, factor):
    return (1 - factor) * start + factor * end


######################
# DESSINER LA GRILLE #
######################

# Créer une fenêtre
window = pygame.display.set_mode(window_size)

# Fonction qui dessine la grille et place les obstacles en fonction du niveau
def draw_grid(grid, positions, symbols, cell_size, window, selected_pos1=None, selected_pos2=None, to_delete=None):
    for i in range(10):
        for j in range(10):

            # Si la position actuelle est l'une des positions sélectionnées ET que les deux positions sont définies, continuez à la prochaine itération
            if selected_pos2 is not None and ((i, j) == selected_pos1 or (i, j) == selected_pos2):
                continue

            symbol = grid[i][j]
            pos = positions[i][j]

            if symbol == 'obstacle':
                obstacle_size = obstacle_image.get_size()  # Obtenez la taille de l'image de l'obstacle
                centered_obstacle_pos = (pos[0] + cell_size // 2 - obstacle_size[0] // 2, pos[1] + cell_size // 2 - obstacle_size[1] // 2)
                window.blit(obstacle_image, centered_obstacle_pos)

                continue  # Passer à l'itération suivante si c'est un obstacle
            if symbol is not None:
                symbol_size = symbols[symbol].get_size()  # Obtenez la taille du symbole
                centered_pos = (pos[0] + cell_size // 2 - symbol_size[0] // 2, pos[1] + cell_size // 2 - symbol_size[1] // 2)
                window.blit(symbols[symbol], centered_pos)
                if (i, j) == selected_pos1:  # If this is the selected symbol
                    pygame.draw.rect(window, (color_Black), (grid_x + cell_x * cell_size, grid_y + cell_y * cell_size, cell_size, cell_size), 2)

                # Si le symbole est à supprimer, dessinez une surbrillance
                if (i, j) in to_delete:
                    pygame.draw.rect(window, (255, 0, 0), (pos[0], pos[1], cell_size, cell_size), 3)


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
        print("BOUTON NOUVEAU")
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

# Détecter le clic sur le bouton QUITTER
def click_on_button_quit(mouse_pos):
    if posX_quit < mouse_pos[0] < (posX_quit + width_quit) and posY_quit < mouse_pos[1] < (posY_quit + height_quit): 
        print("BOUTON QUITTER")
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
        print("BOUTON FERMER")
        return True
    return False


##############
# ECRAN AIDE #
##############

def show_help_screen():
    print("SHOW HELPSCREEN")
    window.blit(help_image, (0, 0))
    draw_button_close()
    pygame.display.flip()


####################
# ECRAN FIN DE JEU #
####################

def show_endgame_screen():
    print("SHOW ENDGAME")
    window.blit(endgame_image, (0, 0))
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
        pygame.time.wait(3)  # Attendre 10 millisecondes

fade_between_images(splash_image, game_image)


#####################
# BOUCLE PRINCIPALE #
#####################

# Variable pour suivre le symbole actuellement sélectionné et sa position
selected_symbol1 = None
selected_pos1 = None
selected_symbol2 = None
selected_pos2 = None

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

    # Remplir l'écran avec l'image de fond
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
    high_score_BTN = pygame.draw.rect(window, color_White, (textHighScore_X - 10,textHighScore_Y,100,40), 2)

    # Score
    fontScore = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 32)
    textScore = fontScore.render(f"{score:04}", True, color_White)
    window.blit(textScore, (450,15))

    # Niveau
    fontLevel = pygame.font.Font("font/JetBrainsMono-Bold.ttf", 12)
    textLevel = fontLevel.render(f"Level: {levelToPlay}", True, color_White)
    window.blit(textLevel, (450, 5))  # Vous pouvez ajuster la position selon vos besoins

    draw_button_new()
    draw_button_help()
    draw_button_quit()

    to_delete = []

    draw_grid(grid, positions, symbols, cell_size, window, selected_pos1, selected_pos2, to_delete)

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
                high_score = update_high_score()
                reset_game()

            elif click_on_button_quit(mouse_pos):
                high_score = update_high_score()
                running = False

            elif click_on_button_help(mouse_pos):
                showing_help = True
                show_help_screen()

            if high_score_BTN.collidepoint(mouse_pos):
                pygame.draw.rect(window, color_Black, high_score_BTN)

            if click_on_button_HS(mouse_pos):
                high_score = 0
                score = 0
                update_high_score()

            cell_x = (mouse_pos[0] - grid_x) // cell_size
            cell_y = (mouse_pos[1] - grid_y) // cell_size

            if 0 <= cell_x < 10 and 0 <= cell_y < 10 and grid[cell_y][cell_x] is not None:
                if grid[cell_y][cell_x] == 'obstacle':  # Si c'est un obstacle, ignorez la sélection
                    continue
                if selected_symbol1 is None:  # If no symbol is selected yet
                    selected_symbol1 = grid[cell_y][cell_x]
                    selected_pos1 = (cell_x, cell_y)
                    # print(f"Symbole1 : {selected_symbol1} à la position {selected_pos1}")

                else:  # If a symbol is already selected
                    if (cell_x, cell_y) != selected_pos1:
                        selected_symbol2 = grid[cell_y][cell_x]
                        selected_pos2 = (cell_x, cell_y)
                        # print(f"Symbole2 : {selected_symbol1} à la position {selected_pos1}")

                    # Animation de l'échange
                    vitessEchange = 10 # plus petit = plus rapide
                    for _ in range(vitessEchange):
                        # 1. Effacer l'écran
                        window.blit(fond, (0, 0))

                        # 2. Dessiner les éléments
                        factor = _ / vitessEchange
                        pos1_x = lerp(positions[selected_pos1[1]][selected_pos1[0]][0], positions[selected_pos2[1]][selected_pos2[0]][0], factor)
                        pos1_y = lerp(positions[selected_pos1[1]][selected_pos1[0]][1], positions[selected_pos2[1]][selected_pos2[0]][1], factor)
                        pos2_x = lerp(positions[selected_pos2[1]][selected_pos2[0]][0], positions[selected_pos1[1]][selected_pos1[0]][0], factor)
                        pos2_y = lerp(positions[selected_pos2[1]][selected_pos2[0]][1], positions[selected_pos1[1]][selected_pos1[0]][1], factor)

                        # Dessiner la grille sans les symboles en mouvement
                        draw_grid(grid, positions, symbols, cell_size, window, selected_pos1, selected_pos2, to_delete)

                        # Dessiner les symboles en mouvement à leurs positions interpolées
                        window.blit(symbols[selected_symbol1], (pos1_x, pos1_y))
                        window.blit(symbols[selected_symbol2], (pos2_x, pos2_y))

                        # 3. Mettre à jour l'affichage

                        pygame.time.wait(50)
                        pygame.display.flip()
                        # Échangez les symboles dans la grille
                        grid[selected_pos1[1]][selected_pos1[0]] = selected_symbol2
                        grid[selected_pos2[1]][selected_pos2[0]] = selected_symbol1

                    # Reset the selected symbols and positions
                    selected_symbol1 = None
                    selected_pos1 = None
                    selected_symbol2 = None
                    selected_pos2 = None

                    # Vérifier les alignements après le mouvement
                    alignments = check_alignments(grid)
                    if alignments:  # Si la liste n'est pas vide

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

                        draw_grid(grid, positions, symbols, cell_size, window, selected_pos1, selected_pos2, to_delete)
                        pygame.display.flip()  # Mettre à jour l'affichage pour montrer la surbrillance

                        remaining_symbols = count_remaining_symbols(grid)
                        if remaining_symbols <= current_objectif:
                            # Gérer la fin de jeu ici (par exemple, passer au niveau suivant)
                            print("FIN DU NIVEAU !")
                            save_progress(config_data)
                            high_score = update_high_score()
                            load_next_level()

high_score = update_high_score()

# Quitter Pygame une fois la boucle terminée
pygame.quit()