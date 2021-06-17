"""
Group 3 - Tic Tac Toe
Player 2 

"""
import socket
import threading
from tkinter import *



def victory(color):
    global turn
    print(color)
    master.config(background = color)
    deadSpace.config(background = color)
    turn = False


#Event when button is pressed
def modify(button):
       print("modify")
       global turn
       buttons[int(button) -1].config(background = "red",text = "X")
       buttons[int(button) -1].config(state = 'disabled') #disables the buttons
       pressed.append(int(button))
       turn = True

def choice(event = None):
   print("choice")
   global turn
   string = str(event.widget.value) 
   if int(string) not in pressed and turn is True: #makes sure buttons can only be pressed once
       print (int(string))
       buttons[int(string) -1].config(background = "blue",text = "O")
       buttons[int(string) -1].config(state = 'disabled') #disables the buttons
       pressed.append(int(string))
       s.sendto(string.encode("ascii") ,(host, port))
       turn = False

def listen():
    global stop
    s.sendto("Player2_connecting".encode("ascii") ,(host, port))
    print("Client Blue")
    while not stop:
        try:
            (msg, addr) = s.recvfrom(1024)
            print("Got {} from {}".format(msg, addr))
            if msg.isdigit() == False:
                victory(msg)
            
            if turn is False and int(msg) not in pressed:
                modify(msg)
                
        except:
            if stop:
                print("breaaak")
                return
        continue



#Gui stuff 
master = Tk()
master.title("Tic Tac Toe  -  Player 2")
master.config(background = "black")
master.geometry("750x500")
stop = False
game = True


#Host connection
port = 5555 #  Send to port above 1024
host = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
thread = threading.Thread(target = listen)
thread.start()



#Space to move buttons to middle
deadSpace= Label(master, text="                                       ")
deadSpace.config(background = "black")
deadSpace.grid(column = 0, row=1)


#The buttons for the game 
turn = True
pressed = []
buttons = []
for n in range(9):
    b = Button(master)
    b.grid(column = (n % 3) + 5, row = int(n / 3 + 1))
    b.config(height = 10 , width = 20)
    b.value = n + 1      
    b.bind('<Button>', choice)
    buttons.append(b)



try:
  mainloop()
except:
  pass
stop = True