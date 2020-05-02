import pygame
import random
import time

pygame.init() # запускаем pygame 

# записываем цвета в переменные для удобства
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (237, 1, 36)
green = (9, 194, 7)
blue = (185, 136, 103)

screen_width = 600 # ширина экрана
screen_height  = 400 # высота экрана

screen = pygame.display.set_mode((screen_width, screen_height)) # окно программы, которое создается, когда мы задаем его размер в настройках  
pygame.display.set_caption("Snake game by Kseniya") # Текст подписи в верхней части экрана диспле

clock = pygame.time.Clock()
 
snake_block = 10 # размер шаблона, из которого состоит змейка
snake_speed = 10 # скорость змейки
 
# задаем шрифт и размер
font_style = pygame.font.SysFont("bahnschrift", 25) 
score_font = pygame.font.SysFont("comicsansms", 25) 

def Your_score(score): # функция, которая рисует счет
    value = score_font.render("Score: " + str(score), True, yellow)
    screen.blit(value, [0, 0]) 

def our_snake(snake_block, snake_list): # функция, которая рисует змейку
    for x in snake_list: 
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block]) # rect - функция для отрисовки прямоугольника, в которую передаем основную поверхность screen, на которой отрисовываем его, цвет прямоугольника, координаты, ширину и длину прямоугольника 
        # x[0], x[1] - координаты верхнего левого угла

def message(msg,color): # функция, которая выводит сообщение на экран
    mesg = font_style.render(msg, True, color) # вызываем функцию, в которую передаем текст сообщения, аргумент сглаживания (0-нет, 1-есть), цвет текста, (4-ым аргументом можно указать цвет фона текста)
    screen.blit(mesg, [screen_width/8, screen_height/2.2]) # на основную поверхность screen в координате (screen_width/6) * (screen_height/3) накладываем текст mesg

def gameLoop():  # главная функция, в которой происходит цикл игры
    game_over = False
    game_close = False
 
    # задаем начальные координаты
    x1 = screen_width / 2
    y1 = screen_height / 2
 
    # координаты изменения траектории движения
    x1_change = 0
    y1_change = 0
 
    # список размера змейки 
    snake_List = []
    # задаем начальную длину змейки
    Length_of_snake = 1
 
    # координаты еды 
    foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
    # в random.randrange передаем начало и и конец, т.е. диапазон значений из которых выбирается случайное число
    # round округляет значение 
    # /10 и *10 - это преобразование нашегочисла к типу float
 

    while not game_over: # игровой цикл 
        
        while game_close == True:  # если игра окончена
            screen.fill(blue) # отрисовываем цвет экрана
            message("You Lost! Press Q-Quit or C-Play Again", yellow) # выводим сообщение о проигрыше

            Your_score((Length_of_snake - 1)*10) #вывод конечного счета на экран
         
            pygame.display.update() # обновление экрана
 
            for event in pygame.event.get(): #цикл, в котором 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: # если нажали q - выходим из игры
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c: # если нажали c - начинаем новую игру
                        gameLoop()
 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # если нажали на кнопку закрытия окна - игра окончена
                game_over = True
            if event.type == pygame.KEYDOWN: # управление змейкой с клавиатуры  
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block # меняем координату изменения траектории двиения
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
 
        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0: # если столкнулись со стенками окна - игра окончена
            game_close = True

        # меняем координаты головы
        x1 += x1_change
        y1 += y1_change

        screen.fill(blue) # отрисовываем цвет фона экрана
        pygame.draw.rect(screen, red, [foodx, foody, snake_block, snake_block]) # отрисовываем еду 

        snake_Head = [] #  создаем пустой список с координатами головы змейки

        snake_Head.append(x1) #  добавляем элемент в конец списка
        snake_Head.append(y1)

        snake_List.append(snake_Head) # добавляем список "голова змейки" в конец списка "змейка", тем самым создаем вложенный список 

        if len(snake_List) > Length_of_snake: # если длина списка больше длины змейки - удаляем самый первый элемент (он больше не нужен, т.к. для нас актуальны только последние координаты)
            del snake_List[0]
 
        for x in snake_List[:-1]: # проходим из конца массива в начало
            if x == snake_Head: # если столкнулись с головой - игра окончена
                game_close = True
 
        our_snake(snake_block, snake_List) # перерисовываем нашу змейку
        Your_score((Length_of_snake - 1)*10) #текущий счет
 
        pygame.display.update() # обновляем экран
 
        if x1 == foodx and y1 == foody: # если координаты головы змейки совпали с координатами еды - обновляем координаты еды и увеличиваем длину змейки
            foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed) # чтобы придать плавности нашей игре задаем скорость смены кадров

    pygame.quit()    
    raise Exception('Exit')

gameLoop()
