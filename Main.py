import pygame
from settings import Settings
import sys
from random import *


def end(data):
    if data.human_score == 15 or data.ai_score == 15:
        data.game_running = False


def draw_button(data, screen):
    image = pygame.image.load("images/graphic.png")
    screen.blit(image, [400, 200])
    name = data.myfont.render('PONG', False, (255, 255, 255))
    screen.blit(name, (50, 50))
    subname = data.myfont.render('AI - NO WALLS', False, (255, 255, 255))
    screen.blit(subname, (50, 100))
    key = data.myfont.render('Press Any Key To Begin', False, (255, 255, 255))
    screen.blit(key, (50, 200))
    if data.human_score == 15:
        victory = data.myfont.render(data.VICTORY, False, (0, 255, 0))
        screen.blit(victory, (50, 300))
    elif data.ai_score == 15:
        victory = data.myfont.render(data.DEFEAT, False, data.RED)
        screen.blit(victory, (50, 300))
    pygame.display.update()


def check_events(data):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, data)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, data)


def check_keyup_events(event, data):
    if event.key == pygame.K_UP:
        data.player_moving_up = False
    if event.key == pygame.K_DOWN:
        data.player_moving_down = False
    if event.key == pygame.K_LEFT:
        data.player_moving_left = False
    if event.key == pygame.K_RIGHT:
        data.player_moving_right = False


def check_keydown_events(event, data):
    if not data.game_running:
        data.game_running = True
        data.human_score = 0
        data.ai_score = 0
        return
    if event.key == pygame.K_q:
        pygame.quit()
        sys.exit()
    if event.key == pygame.K_UP:
        data.player_moving_up = True
    if event.key == pygame.K_DOWN:
        data.player_moving_down = True
    if event.key == pygame.K_LEFT:
        data.player_moving_left = True
    if event.key == pygame.K_RIGHT:
        data.player_moving_right = True


def checkedgecollision(ball, data):
    if ball.top == data.LINETHICKNESS or ball.bottom == (data.HEIGHT - data.LINETHICKNESS):
        hit_sound()
        data.ballDirY = data.ballDirY * -1
    if ball.left == data.LINETHICKNESS or ball.right == (data.WIDTH - data.LINETHICKNESS):
        hit_sound()
        data.ballDirX = data.ballDirX * -1
    return data.ballDirX, data.ballDirY


def hit_ball(ball, paddle1, paddle1_top, paddle1_bot, paddle2, data):
    if data.ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        hit_sound()
        data.ballDirX *= -1
        return
    elif data.ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        hit_sound()
        data.ballDirX *= -1
        return
    if paddle1_top.bottom == ball.top and paddle1_top.left < ball.left and paddle1_top.right > ball.right:
        data.ballDirY *= -1
        hit_sound()
        return
    if paddle1_bot.top == ball.bottom and paddle1_bot.left < ball.left and paddle1_bot.right > ball.right:
        data.ballDirY *= -1
        hit_sound()
        return
    else:
        return 1


def score_sound():
    pygame.mixer.music.load('sound/score.ogg')
    pygame.mixer.music.play(0)


def hit_sound():
    pygame.mixer.music.load('sound/pong.ogg')
    pygame.mixer.music.play(0)


def reset_ball(ball, data):
    seed1 = randint(0, 1)
    if seed1 == 0:
        data.ballDirX = -1
    elif seed1 == 1:
        data.ballDirX = 1
    seed1 = randint(0, 1)
    if seed1 == 0:
        data.ballDirY = -1
    elif seed == 1:
        data.ballDirY = 1
    ball.x = (data.WIDTH // 2)
    ball.y = (data.HEIGHT // 2)
    return


def move_ball(ball, data):
    ball.x += data.ballDirX * data.velocity
    ball.y += data.ballDirY * data.velocity
    return ball


def check_score(data, ball):
    if ball.left == data.LINETHICKNESS:
        score_sound()
        reset_ball(ball, data)
        data.ai_score += 1
        return
    elif ball.centerx < data.HALFSCREEN and ball.top == data.LINETHICKNESS:
        score_sound()
        reset_ball(ball, data)
        data.ai_score += 1
        return
    elif ball.centerx < data.HALFSCREEN and ball.bottom == (data.HEIGHT - data.LINETHICKNESS):
        score_sound()
        reset_ball(ball, data)
        data.ai_score += 1
        return
    elif ball.right == data.WIDTH - data.LINETHICKNESS:
        score_sound()
        data.human_score += 1
        reset_ball(ball, data)
        return
    else:
        return


def displayscore(screen, data):
    player_score = data.BASICFONT.render('Player = %s' % data.human_score, True, data.WHITE)
    resultrect = player_score.get_rect()
    resultrect.topleft = (150, 45)

    ai_score = data.BASICFONT.render('AI = %s' % data.ai_score, True, data.WHITE)
    result_ai = ai_score.get_rect()
    result_ai.topleft = ((data.WIDTH - 150), 45)
    screen.blit(player_score, resultrect)
    screen.blit(ai_score, result_ai)
    notice = data.BASICFONT.render('15 Points To Win', True, data.RED)
    notice_param = notice.get_rect()
    notice_param.center = ((data.HALFSCREEN - 6), (data.HEIGHT/2))
    screen.blit(notice, notice_param)


def cpu(ball, data, paddle2, screen):
    if data.ballDirX == 1 and ball.centerx > data.AI_detection:
        if paddle2.centery < ball.centery:
            paddle2.y = paddle2.y + 1
        elif paddle2.centery > ball.centery:
            paddle2.y = paddle2.y - 1
    pygame.draw.rect(screen, data.WHITE, paddle2)
    return paddle2


def drawpaddle(paddle, data, screen):
    if data.player_moving_down and paddle.bottom < (data.HEIGHT - data.LINETHICKNESS):
        paddle.y += 1
    elif data.player_moving_up and paddle.top > data.LINETHICKNESS:
        paddle.y -= 1
    pygame.draw.rect(screen, data.WHITE, paddle)


def drawpaddle_h(paddle, data, screen):
    if data.player_moving_left and paddle.left > data.LINETHICKNESS:
        paddle.x -= 1
    elif data.player_moving_right and paddle.right < data.HALFSCREEN:
        paddle.x += 1
    pygame.draw.rect(screen, data.WHITE, paddle)


def draw_ball(ball, screen, data):
    pygame.draw.rect(screen, data.WHITE,  ball)


def draw_board(screen, data):
    screen.fill(data.BLACK)
    pygame.draw.rect(screen, data.RED, ((0, 0), (data.WIDTH, data.HEIGHT)), data.LINETHICKNESS*2)
    pygame.draw.line(screen, data.WHITE, ((data.WIDTH // 2), 0),
                     ((data.WIDTH // 2), data.HEIGHT), (data.LINETHICKNESS // 4))


def run_game():
    pygame.init()
    pygame.font.init()
    data = Settings()
    fpsclock = pygame.time.Clock()
    screen = pygame.display.set_mode((data.WIDTH, data.HEIGHT))
    pygame.display.set_caption("Pong")
    ball_x = data.WIDTH//2 - data.LINETHICKNESS//2
    ball_y = data.HEIGHT//2 - data.LINETHICKNESS//2
    player_one_pos = (data.HEIGHT - data.PADDLESIZE) // 2
    player_two_pos = (data.HEIGHT - data.PADDLESIZE) // 2
    paddle1 = pygame.Rect(data.PADDLEOFFSET, player_one_pos, data.LINETHICKNESS, data.PADDLESIZE)
    paddle2 = pygame.Rect(data.WIDTH - data.PADDLEOFFSET - data.LINETHICKNESS, player_two_pos,
                          data.LINETHICKNESS, data.PADDLESIZE)

    ball = pygame.Rect(ball_x, ball_y, 10, 10)

    paddle1_top = pygame.Rect((data.HALFSCREEN//2), data.PADDLEOFFSET, data.PADDLESIZE, data.LINETHICKNESS)
    paddle1_bot = pygame.Rect((data.HALFSCREEN//2), (data.HEIGHT - (data.PADDLEOFFSET + 10)),
                              data.PADDLESIZE, data.LINETHICKNESS)

    draw_board(screen, data)

    drawpaddle(paddle1, data, screen)
    drawpaddle(paddle2, data, screen)
    draw_ball(ball, screen, data)
    pygame.mouse.set_visible(1)

    while True:
        if not data.game_running:
            draw_button(data, screen)
        check_events(data)
        draw_board(screen, data)
        if data.game_running:
            drawpaddle(paddle1, data, screen)
            drawpaddle_h(paddle1_top, data, screen)
            drawpaddle_h(paddle1_bot, data, screen)
            draw_ball(ball, screen, data)
            ball = move_ball(ball, data)

            pygame.draw.rect(screen, data.WHITE, paddle1_top)
            pygame.draw.rect(screen, data.WHITE, paddle1_bot)

            check_score(data, ball)
            data.ballDirX, data.ballDirY = checkedgecollision(ball, data)
            paddle2 = cpu(ball, data, paddle2, screen)
            hit_ball(ball, paddle1, paddle1_top, paddle1_bot, paddle2, data)
            displayscore(screen, data)
            end(data)
            pygame.display.update()
            fpsclock.tick(data.FPS)


run_game()
