import pyxel
from dataclasses import dataclass

def check_collisions(rect1, rect2):
    if rect1.x < rect2.x + rect2.width and rect1.x + rect1.width > rect2.x and rect1.y < rect2.y + rect2.height and rect1.y + rect1.height > rect2.y:
        return True
    return False
    

class Fighter:
    def __init__(self, u, v, name, x = 0, y = 0, width = 16, height = 24, controller = "clavier") -> None:
        self.x = x
        self.y = y
        self.previous_y = y
        self.vx = 0
        self.vy = 0
        self.width = 16
        self.height = 24
        self.health = 100
        self.is_dead = False
        self.name = name
        self.gravity = 0.5
        self.jump_power = 4
        self.jump = 0
        self.speed = 2
        self.controller = controller
        self.fireball = False
        self.u = u
        self.v = v
    
    def update(self, fighter, floor, ennemy):

        if self.controller == "clavier":
            self.vy += self.gravity
            if pyxel.btnp(pyxel.KEY_Z):
                self.u = 16
                self.jump += 1
                if not self.jump >= 3:
                    self.vy = -self.jump_power
            elif pyxel.btn(pyxel.KEY_Q):
                self.u = 64
                self.vx = -self.speed

            elif pyxel.btn(pyxel.KEY_D):
                self.u = 48
                self.vx = self.speed
            else:
                self.u = 32
                self.v = 0
            
            
            self.vx = self.vx * 0.8
            
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.attack(ennemy)
            
            for i in range(20):
                previous_y = self.y
                self.y += self.vy / 10
                if check_collisions(fighter, floor) or check_collisions(fighter, ennemy):
                    self.jump = 0
                    self.y = previous_y
                    self.vy = 0
                
                previous_x = self.x
                self.x += self.vx / 10
                if check_collisions(fighter, floor) or check_collisions(fighter, ennemy):
                    self.x = previous_x
                    self.vx = 0

        if self.controller == "fleches":

            self.vy += self.gravity
            if pyxel.btnp(pyxel.KEY_UP):
                self.u = 16
                self.jump += 1
                if not self.jump >= 3:
                    self.vy = -self.jump_power
            
            elif pyxel.btn(pyxel.KEY_LEFT):
                self.u = 64
                self.vx = -self.speed

            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.u = 48
                self.vx = self.speed

            else:
                self.u = 32
                self.v = 24
            self.vx = self.vx * 0.8
            
            if pyxel.btnp(pyxel.KEY_CTRL):
                print("attack")
                self.attack(ennemy)
                
            for i in range(20):
                previous_y = self.y
                self.y += self.vy / 10
                if check_collisions(fighter, floor) or check_collisions(fighter, ennemy):
                    self.jump = 0
                    self.y = previous_y
                    self.vy = 0
                
                previous_x = self.x
                self.x += self.vx / 10
                if check_collisions(fighter, floor) or check_collisions(fighter, ennemy):
                    self.x = previous_x
                    self.vx = 0

        
        if self.y >= 128 or self.health <= 0:
            self.is_dead = True
    
    def attack(self, ennemy):
        if self.controller == "clavier":
            if self.x < ennemy.x :
                self.fireball = Attack(self.x, self.y, 8, 8, 0, 48, "right")
            else:
                self.fireball = Attack(self.x, self.y, 8, 8, 0, 48, "left")

        else:
            if self.x < ennemy.x :
                self.fireball = Attack(self.x, self.y, 8, 8, 8, 48, "right")
            else:
                self.fireball = Attack(self.x, self.y, 8, 8, 8, 48, "left")


        


@dataclass
class Floor:
    x: int
    y: int
    width: int
    height: int
    u: int
    v: int

@dataclass
class Attack:
    x: int
    y: int
    width: int
    height: int
    u: int
    v: int
    direction: str


class App:
    def __init__(self) -> None:
        pyxel.init(128, 128, title="Nuit du C0de")
        pyxres = pyxel.load("theme.pyxres")
        self.fighters = [Fighter(32, 0, "jambon", 20), Fighter(32, 24, "koala", 100, 0, controller="fleches")]
        self.floors = [Floor(16, 75, 90, 5, 0, 0)]
        self.game_over = None
        pyxel.run(self.update, self.draw)

    def update(self):
        ennemie = {1: 0, 0: 1}
        for i in [0, 1]:

            if self.fighters[i].fireball:
                if self.fighters[i].fireball.direction == "right":
                    self.fighters[i].fireball.x += 2
                else:
                    self.fighters[i].fireball.x -= 2



                if check_collisions(self.fighters[ennemie[i]], self.fighters[i].fireball):
                    self.fighters[ennemie[i]].health -= 34
                    if self.fighters[i].fireball.x < self.fighters[ennemie[i]].x:
                        self.fighters[ennemie[i]].vx += 3
                    else :
                        self.fighters[ennemie[i]].vx -= 3
                    self.fighters[i].fireball = None

                
            for floor in self.floors:
                self.fighters[i].update(self.fighters[i], floor, self.fighters[ennemie[i]])
            

        
        
        
        
    def draw(self):
        if self.game_over == None:
            pyxel.cls(0)
            ennemie = {1: 0, 0: 1}
            color = {0: 6, 1: 8}

            # draw life-bar and game over
            for i in [0, 1]:
                if self.fighters[i].is_dead:
                    self.game_over = i
                    pyxel.cls(0)
                    print(f"{self.fighters[i].name} died")
                    pyxel.blt(3.5, 56, 0, 0, 56+i*16, 121, 16, 0)

                zone = {0: 12, 1: 86}
                pyxel.rect(zone[i], 12, self.fighters[i].health*26//100, 6, color[i])
            
                
            pyxel.blt(10, 10, 0, 33, 48, 30, 8, 0)
            pyxel.blt(84, 10, 0, 33, 48, 30, 8, 0)
            

            for fighter in self.fighters:
                if fighter.controller == "clavier":
                    pyxel.blt(fighter.x, fighter.y, 0, fighter.u, fighter.v, 16, 24, 0)
                else:
                    pyxel.blt(fighter.x, fighter.y, 0, fighter.u, fighter.v, 16, 24, 0)
                    
                if fighter.fireball:
                    pyxel.blt(fighter.fireball.x, fighter.fireball.y, 0, fighter.fireball.u, fighter.fireball.v, fighter.fireball.width, fighter.fireball.height, 0)

            
            
                pyxel.text(10, 110, self.fighters[1].name, 6)
                pyxel.text(95, 110, self.fighters[0].name, 8)
            for floor in self.floors:
                pyxel.blt(floor.x, floor.y, 0, 0, 128, 96, 35, 0)
        
        else:
            pyxel.cls(0)
            pyxel.blt(3.5, 56, 0, 0, 56+int(self.game_over)*16, 121, 16, 0)
            pyxel.text(48, 100, f"{self.fighters[self.game_over].name} won !", 11)
        
App()