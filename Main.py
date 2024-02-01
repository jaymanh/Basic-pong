import pygame as py
import sys
import os
import random
import time
import math
import numpy as np




width = 1200
height = 800
white = (255,255,255)
black = (0,0,0)
yellow = (255,255,0)

paddel_width = 10
paddel_height = 130
paddel1Loc = 0
paddel2Loc = 0
paddelSpeed = 1

ballSpeed = 0.5
ballX = width/2
ballY = height/2
ballRadius = 10
ballVelX = 0
ballVelY = 0

player1Score = 0
player2Score = 0

AI = False

screen = (py.display.set_mode((width, height)))

py.init()
py.display.set_caption("Pong")

clock = py.time.Clock()


def draw():
    
    py.draw.rect(screen, white, (0, paddel1Loc, paddel_width, paddel_height), 0)
    py.draw.rect(screen, white, (width - paddel_width, paddel2Loc, paddel_width, paddel_height), 0)
    py.draw.circle(screen, white, (ballX, ballY), ballRadius, 0)

    draw_text(str(player1Score), py.font.SysFont('comicsans', 100), yellow, screen, width/2 - 100, 10)
    #py.draw.rect(screen, white, (width/2, 30, 5, 100), 0)
    draw_text(str(player2Score), py.font.SysFont('comicsans', 100), yellow, screen, width/2 + 100, 10)
    draw_text("Press r to toggle the AI", py.font.SysFont('comicsans', 30), white, screen, 20, 0)

    py.display.flip()
    

def check_collision():

    global ballX, ballY, ballVelX, ballVelY, ballSpeed
    if (ballX <= paddel_width and ballY >= paddel1Loc and ballY <= paddel1Loc + paddel_height):
        ballVelX *= -1
        ballSpeed += 0.1
    if (ballX >= width - paddel_width and ballY >= paddel2Loc and ballY <= paddel2Loc + paddel_height):
        ballVelX *= -1
        ballSpeed += 0.1

def reset_ball():
    global ballX, ballY, ballVelX, ballVelY, ballSpeed, count
    ballX = width/2
    ballY = height/2
    ballSpeed = 0.5
    ballVelX = random.randint(-1,1)
    ballVelY = random.randint(-1,1)

    if (ballVelX == 0):
        ballVelX = 1
    if (ballVelY == 0):
        ballVelY = 1

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    


if __name__ == "__main__":
    
    reset_ball()

    while True:
        
        mspt = time.time()

        screen.fill((black))
        
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            keys = py.key.get_pressed()
            if keys[py.K_ESCAPE]:
                py.quit()
                sys.exit()


        if (keys[py.K_w] and paddel1Loc > 0):
            paddel1Loc -= paddelSpeed
        if (keys[py.K_s] and paddel1Loc < height - paddel_height):
            paddel1Loc += paddelSpeed

        if (keys[py.K_UP] and paddel2Loc > 0 and not AI):
            paddel2Loc -= paddelSpeed
        if (keys[py.K_DOWN] and paddel2Loc < height - paddel_height and not AI):
            paddel2Loc += paddelSpeed
        
        if (keys[py.K_r]):
            AI = not AI
            reset_ball()
            py.event.wait(1)
            player1Score = 0
            player2Score = 0

        if (AI):
            if (paddel2Loc + paddel_height/2 > ballY):
                if (paddel2Loc > 0):
                    paddel2Loc -= paddelSpeed
            if (paddel2Loc + paddel_height/2 < ballY):
                if (paddel2Loc < height - paddel_height):
                    paddel2Loc += paddelSpeed
        


        ballX += ballVelX * ballSpeed
        ballY += ballVelY * ballSpeed
        
        if (ballX <= 0 or ballX >= width):
            ballVelX *= -1
        if (ballY <= 0 or ballY >= height):
            ballVelY *= -1

        if (keys[py.K_SPACE]):
            paddel1Loc = ballY - paddel_height/2
            paddel2Loc = ballY - paddel_height/2
            print(ballSpeed)
            #colision breaks over 10 speed

        start_time = time.time()
        check_collision()
        end_time = time.time()
        print("Collision check time: ", (end_time - start_time) * 1000)

        if (ballX <= 0):
            player2Score += 1
            reset_ball()

        if (ballX >= width):
            player1Score += 1
            reset_ball()


        start_time = time.time()
        draw()
        end_time = time.time()
        print("Draw time: ", (end_time - start_time) * 1000)
        print("Total time: ", (time.time() - mspt) * 1000) #print the time it took to run the loop in ms
        
        fps = clock.get_fps()
        print("FPS: ", fps)
        clock.tick(200)
        