"""
Group 3 - Tic Tac Toe
Player 1 / server

"""
import socket 
import threading
from tkinter import *

"""
possible = {1,2,3}  # 6
possible2 = {4,5,6} # 10
possible3 = {7,8,9} # 24
possible4 = {1,4,7} # 12
possible5 = {2,5,8} # 15
possible6 = {3,6,9} # 18
possible7 = {1,5,9} # 15
possible8 = {3,5,7} # 15
"""

def logic():
     print(pressed)
     if 1 in pressed and 2 in pressed and 3 in pressed:
         if buttons[0].cget('bg') == buttons[1].cget('bg') and buttons[1].cget('bg') == buttons[2].cget('bg'):
             print("{} WINS!".format(buttons[1].cget('bg')))
             victory(buttons[1].cget('bg'))
            
            
     if 4 in pressed and 5 in pressed and 6 in pressed:
         if buttons[3].cget('bg') == buttons[4].cget('bg') and buttons[4].cget('bg') == buttons[5].cget('bg'):
             print("{} WINS!".format(buttons[4].cget('bg')))
             victory(buttons[4].cget('bg'))
             
     if 7 in pressed and 8 in pressed and 9 in pressed:
         if buttons[6].cget('bg') == buttons[7].cget('bg') and buttons[7].cget('bg') == buttons[8].cget('bg'):
             print("{} WINS!".format(buttons[7].cget('bg')))
             victory(buttons[7].cget('bg'))
             
     if 1 in pressed and 4 in pressed and 7 in pressed:
         if buttons[0].cget('bg') == buttons[3].cget('bg') and buttons[3].cget('bg') == buttons[6].cget('bg'):
             print("{} WINS!".format(buttons[3].cget('bg')))
             victory(buttons[3].cget('bg'))
             
     if 2 in pressed and 5 in pressed and 8 in pressed:
         if buttons[1].cget('bg') == buttons[4].cget('bg') and buttons[4].cget('bg') == buttons[7].cget('bg'):
             print("{} WINS!".format(buttons[4].cget('bg')))
             victory(buttons[4].cget('bg'))
             
     if 3 in pressed and 6 in pressed and 9 in pressed:
         if buttons[2].cget('bg') == buttons[5].cget('bg') and buttons[5].cget('bg') == buttons[8].cget('bg'):
             print("{} WINS!".format(buttons[5].cget('bg')))
             victory(buttons[5].cget('bg'))
             
     if 1 in pressed and 5 in pressed and 9 in pressed:
         if buttons[0].cget('bg') == buttons[4].cget('bg') and buttons[4].cget('bg') == buttons[8].cget('bg'):
             print("{} WINS!".format(buttons[4].cget('bg')))
             victory(buttons[4].cget('bg'))
             
     if 3 in pressed and 5 in pressed and 7 in pressed:
         if buttons[2].cget('bg') == buttons[4].cget('bg') and buttons[4].cget('bg') == buttons[6].cget('bg'):
             print("{} WINS!".format(buttons[4].cget('bg')))
             victory(buttons[4].cget('bg'))

def victory(color):
    global turn
    s.sendto(color.encode("ascii") ,(player2))
    master.config(background = color)
    deadSpace.config(background = color)
    turn = False


def modify(button):
       print("Modify")
       global turn
       buttons[int(button) -1].config(background = "blue",text = "O")
       buttons[int(button) -1].config(state = 'disabled') #disables the buttons
       pressed.append(int(button))
       turn = True
       logic()


def choice(event = None):
   print("Choice")
   global turn
   string = str(event.widget.value) 
   if int(string) not in pressed and turn is True: #makes sure buttons can only be pressed once
       print (int(string))
       buttons[int(string) -1].config(background = "red",text = "X")
       buttons[int(string) -1].config(state = 'disabled') #disables the buttons
       pressed.append(int(string))
       s.sendto(string.encode("ascii") ,(player2))
       turn = False
       logic()

def hosting():
    global player2
    global stop
    global turn
    
    print("SERVER RED")
    while not stop:
        try:
            (msg, addr) = s.recvfrom(1024)
            player2 = addr
            print("Got {} from {}".format(msg, addr))
            
            if turn is False and int(msg) not in pressed:
                modify(msg)
        except:
            if stop:
                print("breaaak")
                return
        continue






#UDP stuff
port = 5555 #  Send to port above 1024
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
s.bind( (host, port) )
player2 = ""

#GUI stuff
master = Tk()
master.title("Tic Tac Toe -  Player 1")
master.config(background = "black")
master.geometry("750x500")
stop = False
game = True


#Space to move buttons to middle
deadSpace= Label(master, text="                                       ")
deadSpace.config(background = "black")
deadSpace.grid(column = 0, row=1)


#The buttons for the game 
turn = False
pressed = []
buttons = []
for n in range(9):
    b = Button(master)
    b.grid(column = (n % 3) + 5, row = int(n / 3 + 1))
    b.config(height = 10 , width = 20)
    b.value = n + 1      
    b.bind('<Button>', choice)
    buttons.append(b)

thread = threading.Thread(target = hosting)
thread.start()


try:
  mainloop()
except:
  pass
stop = True
s.close()

