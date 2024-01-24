import pygame
import random

#tamanho da janela do jogo
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720     

#cores do jogo
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

def main():
    #setup do jogo
    
    #inicia o pygame
    pygame.init()
    
    #cria a janela do jogo
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    #nome da janela
    pygame.display.set_caption("Pong")
    
    #relógio para acompanhar o tempo
    clock = pygame.time.Clock()
    
    #checa se move ou não a bola, checa a cada 3 segundos
    started = False
    
    #paddle de cada jogador
    paddle_1_rect = pygame.Rect(30, 0, 7, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, 0, 7, 100)
    
    #acompanha quanto cada paddle se move
    paddle_1_move = 0
    paddle_2_move = 0
    
    #bola
    ball_rect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 25, 25)
    
    #determina a velocidade da bola
    ball_accel_x = random.randint(2, 4) * 0.1
    ball_accel_y = random.randint(2, 4) * 0.1
    
    #randomiza a direção da bola
    if random.randint(1, 2) == 1:
        ball_accel_x *= -1
    if random.randint(1, 2) == 1:
        ball_accel_y *= -1
    
    #loop do jogo
    while True:
        
        #coloca a cor do background pra preto e é chamado sempre que o jogo atualiza
        screen.fill(COLOR_BLACK)
        
        #faz a bola se mover
        if not started:
            
            #usa a fonte consolas
            font = pygame.font.SysFont('Consolas', 30)
            
            #cria o texto no meio da tela
            text = font.render("Aperte espaço para começar", True, COLOR_WHITE)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, text_rect)
            
            #atualiza o display
            pygame.display.flip()
            clock.tick(60)
            
            #para fechar o jogo
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                #para iniciar o jogo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        started = True
                        
            continue
        
        #obtem o tempo entre agora e o ultimo frame(60 FPS)
        delta_time = clock.tick(60)
        
        #checando eventos
        for event in pygame.event.get():
            
            #se o jogador fecha a janela
            if event.type == pygame.QUIT:
                
                #sai da função e finaliza o jogo
                return
            
            #se o jogador estiver presiionando uma tecla
            if event.type == pygame.KEYDOWN:
                
                #player 1
                #W vai para cima
                if event.key == pygame.K_w:
                    paddle_1_move = -0.5
                
                #S vai para baixo
                if event.key == pygame.K_s:
                    paddle_1_move = 0.5
                
                #player 2
                #Up vai para cima
                if event.key == pygame.K_UP:
                    paddle_2_move = -0.5
                
                #Down vai para baixo 
                if event.key == pygame.K_DOWN:
                    paddle_2_move = 0.5
                    
            #se o jogaor para de pressionar a tecla
            if event.type == pygame.KEYUP:
                
                #se W ou S movimenta o paddle_1
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    paddle_1_move = 0.0
                
                #se Up ou Down movimenta o paddle_2
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle_2_move = 0.0
                    
        #move os paddles de acordo com as variaveis
        paddle_1_rect.top += paddle_1_move * delta_time
        paddle_2_rect.top += paddle_2_move * delta_time
        
        #previne o player 1 de sair do limite de seu paddle
        if paddle_1_rect.top < 0:
            paddle_1_rect.top = 0
        if paddle_1_rect.bottom > SCREEN_HEIGHT:
            paddle_1_rect.bottom = SCREEN_HEIGHT
            
        #previne o player 2 de sair do limite de seu paddle
        if paddle_2_rect.top < 0:
            paddle_2_rect.top = 0 
        if paddle_2_rect.bottom > SCREEN_HEIGHT:
            paddle_2_rect.bottom = SCREEN_HEIGHT
            
        #se a bola toca no parte superior da tela
        if ball_rect.top < 0:
            
            #inverte a velocidade vertical
            ball_accel_y *= -1
            
            #para não ativar o codigo acima novamente
            ball_rect.top = 0 
            
        #se a bola tocar na parte inferior da tela
        if ball_rect.bottom > SCREEN_HEIGHT:
            ball_accel_y *= -1
            ball_rect.top = SCREEN_HEIGHT - ball_rect.height
            
        #se a bola sair dos limites ela reaparece no meio da tela
        if ball_rect.left <= 0 or ball_rect.left >= SCREEN_WIDTH:
            
            ball_rect.x = SCREEN_WIDTH // 2 - ball_rect.width // 2
            ball_rect.y = SCREEN_HEIGHT // 2 - ball_rect.height // 2
            ball_accel_x *= -1
            
        if ball_rect.right >= SCREEN_WIDTH:
        
            ball_rect.x = SCREEN_WIDTH // 2 - ball_rect.width // 2
            ball_rect.y = SCREEN_HEIGHT // 2 - ball_rect.height // 2
            ball_accel_x *= -1
        
        #se o paddle_1 colidir com a bola muda sua direção e velocidade
        if paddle_1_rect.colliderect(ball_rect) and paddle_1_rect.left < ball_rect.left:
            ball_accel_x *= -1
            ball_rect.left = paddle_1_rect.right
        
        #se o paddle_2 colidir com a bola muda sua direção e velocidade
        if paddle_2_rect.colliderect(ball_rect) and paddle_2_rect.left > ball_rect.left:
            ball_accel_x *= -1
            ball_rect.left = paddle_2_rect.left - ball_rect.width
        
        #se o jogo tiver iniciado
        if started:
            
            #move a bola
            ball_rect.left += ball_accel_x * delta_time
            ball_rect.top += ball_accel_y * delta_time
        
        #paddles da cor branca
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)
        
        #faz a bola branca
        pygame.draw.rect(screen, COLOR_WHITE, ball_rect)
        
        #atualiza o display
        pygame.display.update()
    
#executa o jogo
if __name__ == '__main__':
    main()