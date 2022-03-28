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
from os import system, name

class Pong():
    #tamaños pares en y
    #la paleta tiene que tener un tamaño impar o se suma +1
    def __init__(self, sizex:int, sizey:int, vel_paddle:int, vel_ball_x:int, vel_ball_y:int, size_paddle: int):
        self.size_paddle = size_paddle if size_paddle % 2 != 0 else size_paddle +1 
        self.limits = [sizex-1,sizey-1]
        self.vel_paddle = vel_paddle
        self.vel_ball = [vel_ball_x, vel_ball_y]

        self.init_game()
        
      
    def init_game(self):
      self.paddle_position = int(self.limits[1]/2)
      self.ball_position = [int(self.limits[0]/2), int(self.limits[1]/2)]

      #self.ball_direction = [random.choice([-1,2]) * self.vel_ball[0],   random.choice([-1,2]) * self.vel_ball[1]]
      self.ball_direction = [-1, 0]
    
    def paddle_down(self):
        if self.paddle_position == self.limits[1]:
          return
        
        self.paddle_position += self.vel_paddle

    def paddle_up(self):
        if self.paddle_position == 0:
          return

        self.paddle_position -= self.vel_paddle

    def simulate_ball_position(self):
        self.update_ball_position()
        self.paddle_colision()
        return self.check_borders()

    def update_ball_position(self):
        self.ball_position = [pos+direction for pos, direction in zip(self.ball_position, self.ball_direction)]

    def paddle_colision(self):
        #check if the ball has collisioned with the paddle
        if self.ball_position[0] == 0 and self.ball_position[1] >= self.paddle_position-self.size_paddle/2 and self.ball_position[1] <= self.paddle_position+self.size_paddle/2:
          self.ball_direction[0] *= -1
            
        
    
    def check_borders(self):
        #check if the ball has colissioned with the borders or lost
        # if the ball touches bottom wall then reverse y direction

        if (self.ball_position[0] >= self.limits[0]):
          self.ball_position[0] = self.limits[0] - ((self.ball_position[0] + self.vel_ball[0]) % self.limits[0])
          self.ball_direction[0] *= -1
        
        if (self.ball_position[0] < 0):
            return True

        if(self.ball_position[1] >= self.limits[1]):
          self.ball_position[1] = self.limits[1] - ((self.ball_position[1] + self.vel_ball[1]) % self.limits[1])
          self.ball_direction[1] *= -1
          
        if (self.ball_position[1] < 0):
          self.ball_position[1] = 0 - ((self.ball_position[1] + self.vel_ball[1]))
          self.ball_direction[1] *= -1

        return False


    def clear():
      system('cls') if name == 'nt' else system('clear')


    def print_game_state_info(self):
      info = [  f"PADDLE_POSITION: {self.paddle_position}",
                f"BALL_POSITION: {self.ball_position}",
                f"BALL_DIRECTION, {self.ball_direction}",
                f"SIZE_PADDLE: {self.size_paddle}"
              ]
      
      print("; ".join(info), end = "")
      print("")

    def visual(self):
      Pong.clear()
      self.print_game_state_info()

      print("# "*(self.limits[0] + 3))
      for y in range(self.limits[1]+1):
        print("# ", end = "")
        is_paddle = False
        if y >= self.paddle_position-self.size_paddle/2 and y <= self.paddle_position+self.size_paddle/2:
          print("| ", end = "")
          is_paddle = True

 
        
        for x in range(self.limits[0]+1):
          if x == self.ball_position[0] and y == self.ball_position[1]:
            print("O ", end = "")
          elif is_paddle == True:
            is_paddle = False
          else:
            print("  ", end = "")

          
          
        print("# ")
      print("# "*(self.limits[0] + 3))


if __name__ == "__main__":
    #TODO las colisiones con las paredes no estan bien echas
    pong = Pong(sizex = 40, sizey = 40, vel_paddle = 1, vel_ball_x = 1, vel_ball_y = 1, size_paddle = 4)

    while True:
      pong.visual()
      direction = input()
      if direction in ["s", "S", "2"]:
        pong.paddle_down()
      elif direction in ["w", "W", "8"]:
        pong.paddle_up()
      
      
      if pong.simulate_ball_position():
          exit()
