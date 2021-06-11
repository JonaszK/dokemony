import pygame, sys, os, time
import createDokemons
from random import randint

dokemons = createDokemons.create()

# init
pygame.init()
pygame.mixer.init()
res = w, h = 1000, 600

enemy = dokemons[randint(0, 5)]

# Screen
screen = pygame.display.set_mode(res)
pygame.display.set_caption('Dokemony')
clock = pygame.time.Clock()
bg_img = pygame.image.load(os.path.join('assets', 'background.png'))
fight_img = pygame.image.load(os.path.join('assets', "fight_bg.png"))

pikachu_png = pygame.image.load(os.path.join('assets', 'pikachu.png'))
charmander_png = pygame.image.load(os.path.join('assets', 'charmander.png'))
bulbasaur_png = pygame.image.load(os.path.join('assets', 'bulbasaur.png'))
squirtle_png = pygame.image.load(os.path.join('assets', 'squirtle.png'))
onix_png = pygame.image.load(os.path.join('assets', 'onix.png'))
aerodactyl_png = pygame.image.load(os.path.join('assets', 'aerodactyl.png'))

# Fonts and colors
app_font = pygame.font.Font(os.path.join('assets', 'super-legend-boy.otf'), 50)
fight_font = pygame.font.Font(os.path.join('assets', 'super-legend-boy.otf'), 30)
log_font = pygame.font.Font(os.path.join('assets', 'super-legend-boy.otf'), 15)

# Background music # - off | Just change bg_music.wav file to something else
pygame.mixer.music.load(os.path.join('assets', 'bg_music.wav'))
pygame.mixer.music.play(-1, 0.0)

###########
# Loginfo #
###########

endgame_text = app_font.render('', True, (0, 0, 0))
restart_text = fight_font.render('Restart', True, (0, 0, 0))
endgame_rect = endgame_text.get_rect(center=(500, 100))
restart_rect = restart_text.get_rect(center=(500, 425))

###########
# Loginfo #
###########

enemy_log_text = log_font.render('Nothing', True, (0, 0, 0))
player_log_text = log_font.render('Nothing', True, (0, 0, 0))
enemy_log_rect = enemy_log_text.get_rect(center=(300, 100))
player_log_rect = enemy_log_text.get_rect(center=(300, 50))

###########
# Buttons #
###########

start_game_text = app_font.render('Start Game!', True, (0, 0, 0))
start_game_rect = start_game_text.get_rect(center=(500, 450))
start_game_text_shadow = app_font.render('Start Game!', True, (255, 255, 255))
start_game_rect_shadow = start_game_text.get_rect(center=(504, 454))

dokemons_btns = []
dokemons_btns.append((pikachu_png, pygame.Rect(w/2 - 300, h/2 + 100, 64, 64)))
dokemons_btns.append((charmander_png, pygame.Rect(w/2 - 200, h/2 + 100, 64, 64)))
dokemons_btns.append((bulbasaur_png, pygame.Rect(w/2 - 100, h/2 + 100, 64, 64)))
dokemons_btns.append((squirtle_png, pygame.Rect(w/2 + 100, h/2 + 100, 64, 64)))
dokemons_btns.append((onix_png, pygame.Rect(w/2 + 200, h/2 + 100, 64, 64)))
dokemons_btns.append((aerodactyl_png, pygame.Rect(w/2 + 300, h/2 + 100, 64, 64)))

##############
# HealthBars #
##############

player_health_container = pygame.Rect(40, 550, 100, 30)
enemy_health_container = pygame.Rect(870, 550, 100, 30)
player_health = pygame.Rect(40, 550, 100, 30)
enemy_health = pygame.Rect(870, 550, 100, 30)

current_scene = 'main'
winner = True
turn = 0
game_status = True
heal_count_player = 0
heal_count_enemy = 0

def restart_game():
    global player, enemy, turn, dokemons, player_log_rect, player_log_text, enemy_log_rect, enemy_log_rect
    for dokemon in dokemons:
        dokemon.health = dokemon.max_health
    player_log_text = log_font.render(' ', True, (0, 0, 0))
    player_log_rect = player_log_text.get_rect(center=(300, 50))
    enemy_log_text = log_font.render(' ', True, (0, 0, 0))
    enemy_log_rect = player_log_text.get_rect(center=(300, 100))
    player = ''
    enemy = dokemons[randint(0, 5)]
    turn = 0

def end_game(winner):
    global current_scene, endgame_rect, endgame_text, restart_text, restart_rect
    current_scene = 'end'
    if winner == True:
        # User Won
        endgame_text = app_font.render('You won!', True, (0, 0, 0))

    else:
        # Enemy Won
        endgame_text = app_font.render('You lost!', True, (0, 0, 0))
    endgame_rect = endgame_text.get_rect(center=(500, 100))

def player_action (user_action):
    if user_action == 1:
        attack_value = randint(int(player.attack1.dmg_min), int(player.attack1.dmg_max))
        attack_value = (100-enemy.defense)/100 * attack_value
        attack_value = int(type_check(attack_value))
        if enemy.health - attack_value <= 0:
            winner = True
            global game_status
            game_status = False
            show_log('player', player.attack1.name, player.name)
            end_game(winner)
        else:
            enemy.health -= attack_value
            show_log('player', player.attack1.name, player.name)
            enemy_action()

    elif user_action == 2:
        if player.attack2.name == 'Spowolnienie':
            enemy.speed = 0.7 * enemy.speed
            show_log('player', player.attack2.name, player.name)
        elif player.attack2.name == 'Zmniejszenie obrony':
            enemy.defense = 0.8 * enemy.defense
            enemy.special_defense = 0.8 * enemy.special_defense
            show_log('player', player.attack2.name, player.name)
        elif player.attack2.name == 'Zmniejszenie ataku':
            enemy.attack = 0.8 * enemy.attack
            enemy.special_attack = 0.8 * enemy.special_attack
            show_log('player', player.attack2.name, player.name)
        enemy_action()

    elif user_action == 3:
        attack_value = randint(player.attack3.dmg_min, player.attack3.dmg_max)
        attack_value = (100-player.special_defense)/100 * attack_value
        attack_value = int(type_check(attack_value))
        if enemy.health - attack_value <= 0:
            winner = True
            game_status = False
            show_log('player', player.attack3.name, player.name)
            end_game(winner)
        else:
            enemy.health -= attack_value
            show_log('player', player.attack3.name, player.name)
            enemy_action()

    elif user_action == 4:
        heal_value = heal()
        global heal_count_player
        heal_count_player += 1
        if heal_count_player <= 5:
            if player.health + heal_value <= player.max_health:
                player.health += heal_value
            else:
                player.health = player.max_health
            show_log('player', 'heal', player.name)
        else:
            show_log('player', 'All heals used!')

def show_log(who, what, dokemon):
    global enemy_log_text, player_log_text
    if who == 'enemy':
        enemy_log_text = log_font.render(dokemon + ' used ' + what + '. Enemy health: ' + str(enemy.health) + '/' + str(enemy.max_health), True, (0, 0, 0))
        enemy_log_rect = enemy_log_text.get_rect(center=(300, 100))
    elif who == 'player':
        player_log_text = log_font.render(dokemon + ' used ' + what + '. Player health: ' + str(player.health) + '/' + str(player.max_health), True, (0, 0, 0))
        player_log_rect = player_log_text.get_rect(center=(300, 50))

def enemy_action ():
    if (enemy.health / enemy.max_health) - (player.health / player.max_health) < -0.1:
        heal_value = heal()
        global heal_count_enemy
        heal_count_enemy += 1
        if heal_count_enemy <= 5:
            if enemy.health + heal_value <= enemy.max_health:
                enemy.health += heal_value
            else:
                enemy.health = enemy.max_health
            show_log('enemy', 'heal', enemy.name)
        else: enemy_attack()
    else: enemy_attack()



def enemy_attack ():
     action = randint(1, 3)
     if action == 1:
            attack_value = randint(enemy.attack1.dmg_min, enemy.attack1.dmg_max)
            attack_value = ((100-player.defense)/100) * attack_value
            attack_value = int(type_check(attack_value))
            print('hello')
            if player.health - attack_value <= 0:
                winner = False
                global game_status
                game_status = False
                show_log('enemy', enemy.attack1.name, enemy.name)
                end_game(winner)
            else:
                player.health -= attack_value
                show_log('enemy', enemy.attack1.name, enemy.name)
     elif action == 2:
            if enemy.attack2.name == 'Spowolnienie':
                player.speed *= 0.7
                show_log('enemy', 'spowolnienie', enemy.name)
            elif enemy.attack2.name == 'Zmniejszenie obrony':
                player.defense *= 0.8
                player.special_defense *= 0.8
                show_log('enemy', 'zmniejszenie obrony', enemy.name)
            elif enemy.attack2.name == 'Zmniejszenie ataku':
                player.attack *= 0.8
                player.special_attack *= 0.8
                show_log('enemy', 'zmniejszenie ataku', enemy.name)
     elif action == 3:
            attack_value = randint(enemy.attack3.dmg_min, enemy.attack3.dmg_max)
            attack_value = ((100-player.special_defense)/100) * attack_value
            attack_value = int(type_check(attack_value))
            if player.health - attack_value <= 0:
                winner = False

                game_status = False
                show_log('enemy', enemy.attack3.name, enemy.name)
                end_game(winner)
            else:
                player.health -= attack_value
                show_log('enemy', enemy.attack3.name, enemy.name)


def type_check(val):
    if player.attack3.typ2 == 'electric':
        if enemy.typ == 'flying':
                val *= 1.3
        elif enemy.typ == 'ground':
                val *= 0.7
    elif player.attack3.typ2 == 'fire':
        if enemy.typ == 'grass':
                val *= 1.3
        elif enemy.typ == 'water':
                val *= 0.7
    elif player.attack3.typ2 == 'grass':
        if enemy.typ == 'water':
                val *= 1.3
        elif enemy.typ == 'fire':
                val *= 0.7
    elif player.attack3.typ2 == 'water':
        if enemy.typ == 'fire':
                val *= 1.3
        elif enemy.typ == 'grass':
                val *= 0.7
    elif player.attack3.typ2 == 'ground':
        if enemy.typ == 'electric':
                val *= 1.3
        elif enemy.typ == 'flying':
                val *= 0.7
    elif player.attack3.typ2 == 'flying':
        if enemy.typ == 'electric':
                val *= 1.3
        elif enemy.typ == 'ground':
                val *= 0.7
    return val


def heal():
    heal_value = randint(5,30)
    return heal_value

def next_turn ():
    global turn
    global game_status
    turn += 1
    #print current status of the game

    if player.speed >= enemy.speed:
        player_action()
        if game_status == True:
            enemy_action()
    else:
        enemy_action()
        if game_status == True:
            player_action()
    if game_status == True:
        next_turn()

def who_starts():
    global turn
    turn += 1
    if enemy.speed > player.speed:
        enemy_action()

def draw_ui():
    # Draw healthbars
    pygame.draw.rect(screen, (0, 0, 0), player_health_container)
    pygame.draw.rect(screen, (0, 0, 0), enemy_health_container)
    player_health.width = player.health / player.max_health * 100
    enemy_health.width = enemy.health / enemy.max_health * 100

    # Draw green health
    pygame.draw.rect(screen, (32, 252, 3), player_health)
    pygame.draw.rect(screen, (32, 252, 3), enemy_health)

    if enemy.name == 'Pikachu':
        screen.blit(pikachu_png, (800, 500))
    if enemy.name == 'Charmander':
        screen.blit(charmander_png, (800, 500))
    if enemy.name == 'Bulbasaur':
        screen.blit(bulbasaur_png, (800, 500))
    if enemy.name == 'Squirtle':
        screen.blit(squirtle_png, (800, 500))
    if enemy.name == 'Onix':
        screen.blit(onix_png, (800, 500))
    if enemy.name == 'Aerodactyl':
        screen.blit(aerodactyl_png, (800, 500))

    if player.name == 'Pikachu':
        screen.blit(pikachu_png, (150, 500))
    if player.name == 'Charmander':
        screen.blit(charmander_png, (150, 500))
    if player.name == 'Bulbasaur':
        screen.blit(bulbasaur_png, (150, 500))
    if player.name == 'Squirtle':
        screen.blit(squirtle_png, (150, 500))
    if player.name == 'Onix':
        screen.blit(onix_png, (150, 0))
    if player.name == 'Aerodactyl':
        screen.blit(aerodactyl_png, (150, 500))

    global attack_text, attack_rect
    global attack2_text, attack2_rect
    global attack3_text, attack3_rect
    global attack4_text, attack4_rect
    attack_text = fight_font.render(player.attack1.name, True, (0, 0, 0))
    attack_rect = attack_text.get_rect(center=(350, 450))
    attack2_text = fight_font.render(player.attack2.name, True, (0, 0, 0))
    attack2_rect = attack2_text.get_rect(center=(350, 490))
    attack3_text = fight_font.render(player.attack3.name, True, (0, 0, 0))
    attack3_rect = attack3_text.get_rect(center=(350, 530))
    attack4_text = fight_font.render(player.attack4.name, True, (0, 0, 0))
    attack4_rect = attack4_text.get_rect(center=(350, 570))

    screen.blit(enemy_log_text, enemy_log_rect)
    screen.blit(player_log_text, player_log_rect)

    screen.blit(attack_text, attack_rect)
    screen.blit(attack2_text, attack2_rect)
    screen.blit(attack3_text, attack3_rect)
    screen.blit(attack4_text, attack4_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Use event.pos or pg.mouse.get_pos().
                    if current_scene == 'main':
                        if start_game_rect.collidepoint(event.pos):
                            current_scene = 'menu'
                    elif current_scene == 'menu':
                        global player
                        if dokemons_btns[0][1].collidepoint(event.pos):
                            player = dokemons[0]
                            current_scene = 'fight'
                        if dokemons_btns[1][1].collidepoint(event.pos):
                            player = dokemons[1]
                            current_scene = 'fight'
                        if dokemons_btns[2][1].collidepoint(event.pos):
                            player = dokemons[2]
                            current_scene = 'fight'
                        if dokemons_btns[3][1].collidepoint(event.pos):
                            player = dokemons[3]
                            current_scene = 'fight'
                        if dokemons_btns[4][1].collidepoint(event.pos):
                            player = dokemons[4]
                            current_scene = 'fight'
                        if dokemons_btns[5][1].collidepoint(event.pos):
                            player = dokemons[5]
                            current_scene = 'fight'
                    elif current_scene == 'fight':
                        if attack_rect.collidepoint(event.pos):
                            player_action(1)
                        if attack2_rect.collidepoint(event.pos):
                            player_action(2)
                        if attack3_rect.collidepoint(event.pos):
                            player_action(3)
                        if attack4_rect.collidepoint(event.pos):
                            player_action(4)
                    elif current_scene == 'end':
                        if restart_rect.collidepoint(event.pos):
                            current_scene = 'menu'
                            restart_game()

    if current_scene == 'main':
        screen.blit(bg_img, (0, 0))
        screen.blit(start_game_text_shadow, start_game_rect_shadow)
        screen.blit(start_game_text, start_game_rect)
    elif current_scene == 'menu':
        screen.blit(bg_img, (0, 0))
        for btn in dokemons_btns:
            pygame.draw.rect(screen, (116, 227, 221), btn[1])
            screen.blit(btn[0], (btn[1].x, btn[1].y))
    elif current_scene == 'fight':
        screen.blit(fight_img, (0, 0))
        # Draw user choices
        draw_ui()
        # whose turn
        if turn == 0:
            who_starts()
    elif current_scene == 'end':
        screen.blit(bg_img, (0, 0))
        # screen.blit(endgame_text_shadow, endgame_rect_shadow)
        screen.blit(endgame_text, endgame_rect)
        # screen.blit(restart_text_shadow, restart_rect_shadow)
        screen.blit(restart_text, restart_rect)

    pygame.display.update()

    clock.tick(30)