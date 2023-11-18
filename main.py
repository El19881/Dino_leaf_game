import pygame, random

pygame.init()


#display surface
window_width = 1680
window_height = 1050

display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Feed the dino!")

background = pygame.image.load("display.jpg")

#fps and clock
fps = 60
clock = pygame.time.Clock()

#game values
player_starting_lives = 3
velocity = 10
leaf_starting_velocity = 6
leaf_acceleration = 0.25
buffer_distance = 400

score = 0
player_lives = player_starting_lives
leaf_velocity = 6

#set colors
green = (0,255,0)
darkgreen = (10,50,10)
white = (255,255,255)
black = (0,0,0)


#set fonts
font = pygame.font.Font('font.ttf', 32)

#set text
score_info = font.render("Score: " + str(score), True, green, darkgreen )
score_rect = score_info.get_rect()
score_rect.topleft = (10,10)

title = font.render("Feed the dino!", True, green, white)
title_rect = title.get_rect()
title_rect.centerx = (window_width//2)
title_rect.y = 10

lives = font.render("Lives: " + str(player_lives), True, green, darkgreen)
lives_rect = lives.get_rect()
lives_rect.topright = (window_width-10 ,10)

game_over = font.render("Game Over", True, green, darkgreen)
game_over_rect = game_over.get_rect()
game_over_rect.center = (window_width//2, window_height//2)

play_again = font.render("Press any key to continue", True, green, darkgreen)
play_again_rect = play_again.get_rect()
play_again_rect.center = (window_width//2, window_height//2 + 30)

#set sounds and music
leaf_catch_sound = pygame.mixer.Sound("catch.wav")
miss_sound = pygame.mixer.Sound("miss.wav")
miss_sound.set_volume(.1)
pygame.mixer.music.load("song.wav")

#set images
player_image = pygame.image.load("dino.png")
player_image_rect = player_image.get_rect()
player_image_rect.left = 32
player_image_rect.centery = window_height//2

leaf_image = pygame.image.load("leaf.png")
leaf_rect = leaf_image.get_rect()
leaf_rect.x = window_width + buffer_distance
leaf_rect.y = random.randint(64, window_height - 256)




#main game loop
pygame.mixer.music.play(-1,0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #check if key is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_image_rect.top > 64:
        player_image_rect.y -= velocity
    if keys[pygame.K_DOWN] and player_image_rect.bottom < window_height:
        player_image_rect.y += velocity
    if keys[pygame.K_LEFT] and player_image_rect.left > 0:
        player_image_rect.x -= velocity
    if keys[pygame.K_RIGHT] and player_image_rect.right < window_width:
        player_image_rect.x += velocity


    #move coin
    if leaf_rect.x < 0:
        #player missed coin
        player_lives -= 1
        miss_sound.play()
        leaf_rect.x = window_width + buffer_distance
        leaf_rect.y = random.randint(64, window_height - 256)
    else:
        leaf_rect.x -= leaf_velocity

    #check for collisions
    if player_image_rect.colliderect(leaf_rect):
        score += 1
        leaf_catch_sound.play()
        leaf_velocity += leaf_acceleration
        leaf_rect.x = window_width + buffer_distance
        leaf_rect.y = random.randint(64, window_height - 256)

    #update text for score/lives
    score_info = font.render("Score " + str(score), True, green, darkgreen )
    lives = font.render("Lives " + str(player_lives), True, green, darkgreen)


    #check for game over
    if player_lives == 0:
        display_surface.blit(game_over, game_over_rect)
        display_surface.blit(play_again, play_again_rect)
        pygame.display.update()

        #pause the game until player preses a key and rest
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                #player wants to play again:
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = player_starting_lives
                    player_image_rect.y = window_height//2
                    leaf_velocity = leaf_starting_velocity
                    is_paused = False
                    pygame.mixer_music.play(-1,0.0)
                #player wants to quit
                elif event.type == pygame.QUIT:
                    is_paused = False
                    running = False


    #fill the display
    display_surface.blit(background,(0,0))

    #bilt the hud
    display_surface.blit(score_info, score_rect)
    display_surface.blit(title, title_rect)
    display_surface.blit(lives,lives_rect)
    pygame.draw.line(display_surface, white, (0,64),(window_width, 64), 2)

     #blit assets to screen
    display_surface.blit(player_image, player_image_rect)
    display_surface.blit(leaf_image, leaf_rect) 

    #update display and tick clok
    pygame.display.update()
    clock.tick(fps)



pygame.quit()
