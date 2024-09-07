import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))

def getKey(keyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    """"
     FOR THE ABOVE LINE: if we say that our key name is Left,
     It will write it in as K_Left - switching out the curly braces
    """
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans

def main():
    print(getKey("a"))

if __name__ == '__main__':
    init()
    while True:
        main()