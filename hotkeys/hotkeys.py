from pynput.keyboard import Key, Listener
import keyboard
import time

message1 = '/play bedwars_eight_one'# 1v1v1v1v1v1v1v1
message2 = '/play bedwars_eight_two'# 2v2v2v2v2v2v2v2
message3 = '/play bedwars_four_three'# 3v3v3v3
message4 = '/play bedwars_four_four'# 4v4v4v4
message5 = '/play bedwars_two_four'# 4v4
message6 = '/afkwarp'#
message7 = '/kickoffline'#
message8 = '/tipall'#
message9 = 'bruh'#
message10 = 'please dont flatbridge'#

def write(message, latency=0.1):
    keyboard.press_and_release('enter')
    time.sleep(latency)
    keyboard.write(message)
    keyboard.press_and_release('enter')
    

check = True
def on_press(key):
    global check
    if check == True:
        if str(key) == 'Key.insert':
            write(message1)
            
        if str(key) == 'Key.end':
            write(message2)

        if str(key) == 'Key.down':
            write(message3)

        if str(key) == 'Key.page_down':
            write(message4)

        if str(key) == 'Key.left':
            write(message5)
        
        if str(key) == '<12>':
            write(message6)

        if str(key) == 'Key.right':
            write(message7)

        if str(key) == 'Key.home':
            write(message8)

        if str(key) == 'Key.up':
            write(message9)

        if str(key) == 'Key.page_up':
            write(message10)
       
        check = False
 
def on_release(key):
    global check
    check = True
 
with Listener(on_press=on_press, on_release=on_release) as listener: listener.join()
