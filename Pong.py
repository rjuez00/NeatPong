"""
PONG:
  razón: la paleta va mas lenta que la pelota

recibe:
  donde esta la paleta
  
pelota: 
  vector (direccion y velocidad) eje x
  vector (direccion y velocidad) eje y
  localizacion eje x
  localizacion eje y

devuelve:
  mover la paleta arriba o abajo

fitness: 
  tiempo

nota_beni: 
  mira a ver que la pelota no vaya más rapido en diagonal (beni guapo)

"""

"""
eje y
|
|         *
||    
|
|
_______________ eje x

https://www.geeksforgeeks.org/create-pong-game-using-python-turtle/
"""
import random

class Pong():
    #tamaños pares en y
    def __init__(self, sizex:int, sizey:int, vel_paddle:int, vel_ball_x:int, vel_ball_y:int, sizepaddle: int):
        self.sizex = sizex
        self.sizey = sizey
        self.vel_paddle = vel_paddle
        self.vel_ball_x = vel_ball_x
        self.vel_ball_y = vel_ball_y

        self.paddle_position = int(self.sizey/2)
        self.ball_position = [int(self.sizex/2), int(self.sizey/2)]
        self.ball_direction = [random.randint(-1,1) * vel_ball_x,   random.randint(-1, 1) * vel_ball_y]
    
    def paddle_down(self):
        self.paddle_position -= self.vel_paddle

    def paddle_up(self):
        self.paddle_position += self.vel_paddle

    def simulate_ball_position(self):
        self.update_ball_position()
        self.paddle_colision()
        return self.check_borders()

    def update_ball_position(self):
        self.ball_position = [pos+direction for pos, direction in zip(self.ball_position, self.ball_direction)]

    def paddle_colision(self):
        #check if the ball has collisioned with the paddle
        pass

    def check_borders(self):
        #check if the ball has colissioned with the borders or lost
        # if the ball touches bottom wall then reverse y direction
        pass