import asyncio
import pygame

async def run():
    pygame.init()
    pygame.font.init()

    display = pygame.display.set_mode((1280,720))

    p1_img = pygame.image.load("assets/user-1.png")
    player1 = p1_img.get_rect()
    player1_score = 0
    player1_speed = 7

    p2_img = pygame.image.load("assets/user-2.png")
    player2 = p2_img.get_rect(right=1280)
    player2_score = 0
    player2_speed = 7

    ball_img = pygame.image.load("assets/bola.png")
    ball = ball_img.get_rect(center=[1280 / 2, 720 /2])
    ball_dir_x = 10
    ball_dir_y = 10

    font = pygame.font.Font(None, 50)
    placar_player1 = font.render(str(player1_score), True, "white")
    placar_player2 = font.render(str(player2_score), True, "white")

    campo_img = pygame.image.load("assets/campo.png")
    campo = campo_img.get_rect()

    cena = "menu"

    fps = pygame.time.Clock()

    fade_img = pygame.Surface((1280, 720)).convert_alpha()
    fade_img.fill("black")
    fade_alpha = 255

    music = pygame.mixer.Sound("assets/music.ogg")
    music.play(-1)

    loop = True
    while loop:
        
        if cena == "jogo":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        loop = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player1_speed *= -1 
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player2_speed *= -1 
            
            if player2_score >= 3 or player1_score >= 3:
                cena = "gameover"

            if ball.colliderect(player1) or ball.colliderect(player2):
                ball_dir_x *= -1
                hit = pygame.mixer.Sound("assets/pong.wav")
                hit.play()
            
            if player1.y <= 0:
                player1.y = 0
            elif player1.y >= 720 - 150:
                player1.y = 720 - 150

            player1.y += player1_speed


            if ball.x <= 0:
                player2_score += 1
                placar_player2 = font.render(str(player2_score), True, "white")
                ball.x = 600
                ball_dir_x *= -1
            elif ball.x >= 1280:
                player1_score += 1
                placar_player1 = font.render(str(player1_score), True, "white")
                ball.x = 600
                ball_dir_x *= -1

            if ball.y <= 0 or ball.y >= (720 - 15):
                ball_dir_y *= -1

            ball.x += ball_dir_x 
            ball.y += ball_dir_y 

            # player2.y = ball.y - 75

            # if player2.y <= 0:
            #     player2.y = 0
            # elif player2.y >= 720 - 150:
            #     player2.y = 720 - 150

            if player2.y <= 0:
                player2.y = 0
            elif player2.y >= 720 - 150:
                player2.y = 720 - 150

            player2.y += player2_speed

            display.fill((0,0,0))
            display.blit(campo_img, campo)
            display.blit(p1_img, player1)
            display.blit(p2_img, player2)
            display.blit(ball_img, ball)
            display.blit(placar_player1, (500,50))
            display.blit(placar_player2, (780,50))

        elif cena == "gameover":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        cena = "menu"

            display.fill((107, 100, 189))
            
            if player1_score > player2_score: 
                txt = "O Player 1 é o ganhado!"
            else: 
                txt = "O Player 2 é o ganhador!"
                
            text_win = font.render(txt, True, "black")
            text_rect = text_win.get_rect(center = (1208 // 2, 720 // 2))
            display.blit(text_win, text_rect)

        elif cena == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        player1_score = 0
                        player2_score = 0
                        placar_player1 = font.render(str(player1_score), True, "white")
                        placar_player2 = font.render(str(player2_score), True, "white")
                        cena = "jogo"
                        fade_alpha = 255
                        
                        start = pygame.mixer.Sound("assets/start.wav")
                        start.play()

            fade_alpha -= 1
            fade_img.set_alpha(fade_alpha)

            display.fill((0,0,0))
            title = font.render("Pong Pong", True, "red")
            text = font.render("Precione start para iniciar", True, "white")
            display.blit(title, [(540), 360])    
            display.blit(text, [(440), 460])    
            display.blit(fade_img, [0, 0])
        
        await asyncio.sleep(0) # This line is important
        fps.tick(60)
        pygame.display.flip()

asyncio.run(run())