import pygame
import time
import json

pygame.init()

starttime = time.time()
done = False
displayGameOver = False
screen = pygame.display.set_mode((1400, 800), pygame.NOFRAME)
pygame.display.set_caption("Riven Fast Q Combo Practice")

gameOverText = pygame.font.SysFont('arial', 40).render('You Failed Something. Press Anything to Try Again', True, (200, 200, 200))
gameOverTextRect = gameOverText.get_rect()
gameOverTextRect.center = (700, 400)

escRect = pygame.Rect(1300, 50, 50, 50)

escText = pygame.font.SysFont('arial', 24).render('ESC', True, (0, 0, 0))
escTextRect = escText.get_rect()
escTextRect.center = (escRect.x + escRect.w // 2, escRect.y + escRect.h // 2)

f = open("settings.json")
j = json.load(f)
f.close()

boxes = [
    pygame.Rect(j["boxPosition"]["AutoBox"]),
    pygame.Rect(j["boxPosition"]["QBox"]),
    pygame.Rect(j["boxPosition"]["MoveBox"])
]

boxcol = [
    j["boxCols"]["AutoBox"],
    j["boxCols"]["QBox"],
    j["boxCols"]["MoveBox"]
]

timings = [
    j["Timings"]["QTime"],
    j["Timings"]["MoveTime"],
    j["Timings"]["AutoTime"]
]

currentbox = 0

def update():
    global currentbox
    if currentbox > 2:
        currentbox = 0
    if currentbox == 2:
        if not getTimings:
            global displayGameOver
            displayGameOver = True
    
def handleEvent(e):
    global currentbox, boxes, starttime, displayGameOver
    if abs(e - 1) == abs(currentbox - 1):
        if getTimings() and boxes[currentbox].collidepoint(pygame.mouse.get_pos()):
            currentbox += 1
            starttime = time.time()
        else:
            displayGameOver = True
    else:
        displayGameOver = True
        
def getTimings():
    global currentbox, starttime
    currenttime = time.time()
    if currentbox == 2:
        return currenttime - starttime < timings[currentbox]
    else:
        return currenttime - starttime > timings[currentbox]

def updateDisplay():
    global displayGameOver
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (200, 20, 20), escRect)
    screen.blit(escText, escTextRect)
    if displayGameOver:
        global gameOverText, gameOverTextRect
        screen.blit(gameOverText, gameOverTextRect)
    elif getTimings():
        pygame.draw.rect(screen, boxcol[currentbox], boxes[currentbox])
    pygame.display.flip()

def handleEvents():
    global done, displayGameOver, currentbox
    event = pygame.event.poll()
    while event.type != pygame.NOEVENT:
        if event.type == pygame.QUIT:
            done = True
        elif displayGameOver and event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
            displayGameOver = False
            currentbox = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_q:
                handleEvent(1)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if escRect.collidepoint(event.pos):
                done = True
            else:
                handleEvent(0)
        event = pygame.event.poll()

while not done:
    update()
    updateDisplay()
    handleEvents()

pygame.quit()
