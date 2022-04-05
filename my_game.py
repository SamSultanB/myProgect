from tkinter import *
from random import randint


class Game:
    def __init__(self, c, n, m, width, height):
        self.c = c
        self.a = []
        self.n = n + 2
        self.m = m + 2
        self.width = width
        self.height = height
        self.button = False
        for i in range(self.n):
            self.a.append([])
            for j in range(self.m):
                if i == 1 or i == self.n-2:
                    self.a[i].append(4)
                elif j == 1 or j == self.m-2:
                    self.a[i].append(4)
                # self.a[i].append(choice([0, 1]))
                else:
                    self.a[i].append(0)
        self.c.bind('<Button>', self.__location_of_doctor)
        for i in range(randint(2, self.n-2)):
            self.a[randint(3, self.n-3)][randint(3, self.n-3)] = 1

        for i in range(randint(2, self.n-2)):
            self.a[randint(3, self.n-3)][randint(3, self.m-3)] = 5
        self.draw()

    def __location_of_doctor(self, event):
        x, y = event.x//23, event.y//23
        print(x, y)
        self.a[x+1][y+1] = 3

    def start(self):
        self.button = True

    def stop(self):
        self.button = False

    def __movement(self):
        if self.button is True:
            Doctor.move(self)
            Virus.move_of_virus(self)
            People.move_of_people(self)
            self.colisions()
        else:
            pass

    def colisions(self):
        Virus.virus_collide_doctor(self)
        People.people_collide_virus(self)
        Doctor.doctor_collide(self)
        Doctor.wall_collide_doctor(self)
        Virus.wall_collide_virus(self)
        People.wall_collide_people(self)

    def print_field(self):
        for i in range(self.n):
            for j in range(self.m):
                print(self.a[i][j], end="")
            print()

    def draw(self):

        clr = "grey"
        s = self.width // (self.n - 2)
        d = self.height // (self.m - 2)
        for i in range(1, self.n - 1):
            for j in range(1, self.m - 1):
                if (self.a[i][j] == 3):
                    clr = 'BLUE'
                elif (self.a[i][j] == 1):
                    clr = 'GREY'
                elif (self.a[i][j] == 5):
                    clr = 'RED'
                elif (self.a[i][j] == 4):
                    clr = "BLACK"
                else:
                    clr = "WHITE"
                self.c.create_oval((i-1)*s, (j-1)*d, i*s, j*d, fill=clr)
        self.__movement()
        self.c.after(100, self.draw)


class Doctor(Game):
    def move(self):
        for i in range(self.n-2):
            for j in range(self.m-2):
                if self.a[i][j] == 3:
                    if self.a[i+1][j] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 0)][j-1] = 3
                    elif self.a[i+1][j+1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 0)][j+randint(-1, 0)] = 3
                    elif self.a[i+1][j-1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 0)][j+randint(0, 1)] = 3
                    elif self.a[i-1][j+1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(0, 1)][j+randint(-1, 0)] = 3
                    elif self.a[i-1][j-1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(0, 1)][j+randint(0, 1)] = 3
                    elif self.a[i][j+1] != 0:
                        self.a[i][j] = 0
                        self.a[i-1][j+randint(-1, 0)] = 3
                    elif self.a[i-1][j] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(0, 1)][j-1] = 3
                    elif self.a[i][j-1] != 0:
                        self.a[i][j] = 0
                        self.a[i-1][j+randint(0, 1)] = 3
                    elif self.a[i+1][j] != 0 and self.a[i-1][j] != 0:
                        self.a[i][j] = 0
                        if self.a[i][j+1] != 0:
                            self.a[i][j-1] = 3
                        elif self.a[i][j-1] != 0:
                            self.a[i][j+1] = 3
                        else:
                            pass
                    s0 = self.a[i][j-1]+self.a[i-1][j+1]+self.a[i+1][j-1]
                    s = self.a[i+1][j]+self.a[i+1][j+1]+s0
                    if self.a[i-1][j-1]+self.a[i-1][j]+self.a[i-1][j+1]+s == 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 1)][j+randint(-1, 1)] = 3
                    else:
                        pass
                else:
                    pass

    def doctor_collide(self):
        for i in range(self.n-2):
            for j in range(self.m-2):
                if self.a[i][j] == 3:
                    nb = self.a[i+1][j-1]+self.a[i+1][j]+self.a[i+1][j+1]
                    nb2 = self.a[i-1][j+1]+self.a[i][j-1]+self.a[i-1][j+1]+nb
                    if self.a[i-1][j-1]+self.a[i-1][j]+nb2 >= 10:
                        self.a[i][j] = 5
                    else:
                        pass

    def wall_collide_doctor(self):
        for i in range(self.n-2):
            for j in range(self.m-2):
                if self.a[i][j] == 3:
                    if self.a[i+1][j] == 4:
                        self.a[i][j] = 0
                        self.a[i-1][j] = 3
                    elif self.a[i][j+1] == 4:
                        self.a[i][j] = 0
                        self.a[i][j-1] = 3
                    elif self.a[i-1][j] == 4:
                        self.a[i][j] = 0
                        self.a[i+1][j] = 3
                    elif self.a[i][j-1] == 4:
                        self.a[i][j] = 0
                        self.a[i][j+1] = 3
                    elif self.a[i+1][j+1] == 4:
                        self.a[i][j] = 0
                        self.a[i-1][j-1] = 3
                    elif self.a[i+1][j-1] == 4:
                        self.a[i][j] = 0
                        self.a[i-1][j+1] = 3
                    elif self.a[i-1][j-1] == 4:
                        self.a[i][j] = 0
                        self.a[i+1][j+1] = 3
                    elif self.a[i-1][j+1] == 4:
                        self.a[i][j] = 0
                        self.a[i+1][j-1] = 3
                    else:
                        self.a[i][j] = 3
                else:
                    pass


class Virus(Doctor):

    def move_of_virus(self):
        for i in range(self.n-2):
            for j in range(self.m-2):
                if self.a[i][j] == 5:
                    if self.a[i+1][j] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 0)][j-1] = 5
                    elif self.a[i+1][j+1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 0)][j+randint(-1, 0)] = 5
                    elif self.a[i+1][j-1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 0)][j+randint(0, 1)] = 5
                    elif self.a[i-1][j+1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(0, 1)][j+randint(-1, 0)] = 5
                    elif self.a[i-1][j-1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(0, 1)][j+randint(0, 1)] = 5
                    elif self.a[i][j+1] != 0:
                        self.a[i][j] = 0
                        self.a[i-1][j+randint(-1, 0)] = 5
                    elif self.a[i-1][j] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(0, 1)][j-1] = 5
                    elif self.a[i][j-1] != 0:
                        self.a[i][j] = 0
                        self.a[i-1][j+randint(0, 1)] = 5
                    elif self.a[i+1][j] != 0 and self.a[i-1][j] != 0:
                        self.a[i][j] = 0
                        if self.a[i][j+1] != 0:
                            self.a[i][j-1] = 5
                        elif self.a[i][j-1] != 0:
                            self.a[i][j+1] = 5
                        else:
                            pass
                    s0 = self.a[i][j-1]+self.a[i-1][j+1]+self.a[i+1][j-1]
                    s = self.a[i+1][j]+self.a[i+1][j+1]+s0
                    if self.a[i-1][j-1]+self.a[i-1][j]+self.a[i-1][j+1]+s == 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 1)][j+randint(-1, 1)] = 5
                    else:
                        pass
                else:
                    pass

    def virus_collide_doctor(self):
        for i in range(self.n-2):
            for j in range(self.m-2):
                if self.a[i][j] == 5:
                    if self.a[i+1][j] == 3:
                        self.a[i][j] = 1
                    elif self.a[i+1][j+1] == 3:
                        self.a[i][j] = 1
                    elif self.a[i+1][j-1] == 3:
                        self.a[i][j] = 1
                    elif self.a[i-1][j+1] == 3:
                        self.a[i][j] = 1
                    elif self.a[i-1][j-1] == 3:
                        self.a[i][j] = 1
                    elif self.a[i][j+1] == 3:
                        self.a[i][j] = 1
                    elif self.a[i-1][j] == 3:
                        self.a[i][j] = 1
                    elif self.a[i][j-1] == 3:
                        self.a[i][j] = 1
                    else:
                        pass
                else:
                    pass

    def wall_collide_virus(self):
        for i in range(self.n-2):
            for j in range(self.m-2):
                if self.a[i][j] == 5:
                    if self.a[i+1][j] == 4:
                        self.a[i][j] = 0
                        self.a[i-1][j] = 5
                    elif self.a[i][j+1] == 4:
                        self.a[i][j] = 0
                        self.a[i][j-1] = 5
                    elif self.a[i-1][j] == 4:
                        self.a[i][j] = 0
                        self.a[i+1][j] = 5
                    elif self.a[i][j-1] == 4:
                        self.a[i][j] = 0
                        self.a[i][j+1] = 5
                    elif self.a[i+1][j+1] == 4:
                        self.a[i][j] = 0
                        self.a[i-1][j-1] = 5
                    elif self.a[i+1][j-1] == 4:
                        self.a[i][j] = 0
                        self.a[i-1][j+1] = 5
                    elif self.a[i-1][j-1] == 4:
                        self.a[i][j] = 0
                        self.a[i+1][j+1] = 5
                    elif self.a[i-1][j+1] == 4:
                        self.a[i][j] = 0
                        self.a[i+1][j-1] = 5
                    else:
                        self.a[i][j] = 5
                else:
                    pass


class People(Virus):

    def move_of_people(self):
        for i in range(self.n-2):
            for j in range(self.m-2):
                if self.a[i][j] == 1:
                    if self.a[i+1][j] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 0)][j-1] = 1
                    elif self.a[i+1][j+1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 0)][j+randint(-1, 0)] = 1
                    elif self.a[i+1][j-1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 0)][j+randint(0, 1)] = 1
                    elif self.a[i-1][j+1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(0, 1)][j+randint(-1, 0)] = 1
                    elif self.a[i-1][j-1] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(0, 1)][j+randint(0, 1)] = 1
                    elif self.a[i][j+1] != 0:
                        self.a[i][j] = 0
                        self.a[i-1][j+randint(-1, 0)] = 1
                    elif self.a[i-1][j] != 0:
                        self.a[i][j] = 0
                        self.a[i+randint(0, 1)][j-1] = 1
                    elif self.a[i][j-1] != 0:
                        self.a[i][j] = 0
                        self.a[i-1][j+randint(0, 1)] = 1
                    elif self.a[i+1][j] != 0 and self.a[i-1][j] != 0:
                        self.a[i][j] = 0
                        if self.a[i][j+1] != 0:
                            self.a[i][j-1] = 1
                        elif self.a[i][j-1] != 0:
                            self.a[i][j+1] = 1
                        else:
                            pass
                    s0 = self.a[i][j-1]+self.a[i-1][j+1]+self.a[i+1][j-1]
                    s = self.a[i+1][j]+self.a[i+1][j+1]+s0
                    if self.a[i-1][j-1]+self.a[i-1][j]+self.a[i-1][j+1]+s == 0:
                        self.a[i][j] = 0
                        self.a[i+randint(-1, 1)][j+randint(-1, 1)] = 1
                    else:
                        pass
                else:
                    pass

    def people_collide_virus(self):
        for i in range(self.n-2):
            for j in range(self.m-2):
                if self.a[i][j] == 1:
                    if self.a[i+1][j] == 5:
                        self.a[i][j] = 5
                    elif self.a[i+1][j+1] == 5:
                        self.a[i][j] = 5
                    elif self.a[i+1][j-1] == 5:
                        self.a[i][j] = 5
                    elif self.a[i-1][j+1] == 5:
                        self.a[i][j] = 5
                    elif self.a[i-1][j-1] == 5:
                        self.a[i][j] = 5
                    elif self.a[i][j+1] == 5:
                        self.a[i][j] = 5
                    elif self.a[i-1][j] == 5:
                        self.a[i][j] = 5
                    elif self.a[i][j-1] == 5:
                        self.a[i][j] = 5
                    else:
                        pass
                else:
                    pass

    def wall_collide_people(self):
        for i in range(self.n-2):
            for j in range(self.m-2):
                if self.a[i][j] == 1:
                    if self.a[i+1][j] == 4:
                        self.a[i][j] = 0
                        self.a[i-1][j] = 1
                    elif self.a[i][j+1] == 4:
                        self.a[i][j] = 0
                        self.a[i][j-1] = 1
                    elif self.a[i-1][j] == 4:
                        self.a[i][j] = 0
                        self.a[i+1][j] = 1
                    elif self.a[i][j-1] == 4:
                        self.a[i][j] = 0
                        self.a[i][j+1] = 1
                    elif self.a[i+1][j+1] == 4:
                        self.a[i][j] = 0
                        self.a[i-1][j-1] = 1
                    elif self.a[i+1][j-1] == 4:
                        self.a[i][j] = 0
                        self.a[i-1][j+1] = 1
                    elif self.a[i-1][j-1] == 4:
                        self.a[i][j] = 0
                        self.a[i+1][j+1] = 1
                    elif self.a[i-1][j+1] == 4:
                        self.a[i][j] = 0
                        self.a[i+1][j-1] = 1
                    else:
                        self.a[i][j] = 1
                else:
                    pass

root = Tk()
root.geometry("700x750")
c = Canvas(root, width=700, height=700)
c.pack()

g = Game(c, 30, 30, 700, 700)
b1 = Button(root, text='Start', command=g.start)
b2 = Button(root, text='Stop', command=g.stop)
b1.pack()
b2.pack()
g.print_field()
root.mainloop()
