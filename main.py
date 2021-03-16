#Імпорт бібліотек
import pygame, time, random
pygame.init()

#константи: параметри вікна, швидкість ворожих мобів(вони ходять раз у певну кількість ітерацій головного циклу), час, що залишився у гравця та режим гри: меню, опції та гра
worldWidth = 700
worldHeight = 700
fire_speed = 5
timer = 120
game_mode = 1

#Створення вікна
win = pygame.display.set_mode([worldWidth,worldHeight])
pygame.display.set_caption("Maze Without The Sun")

#Клас меню
class Menu:
#   Фотографії з кнопками 
    buttons = {"start":[pygame.image.load("start.png")],"options":[pygame.image.load("options.png")],"exit":[pygame.image.load("exit.png")]}
    bgimg = pygame.image.load("background.png")
#Ініціалізація класу
    def init(self):
        pass
#Вивід основного меню
    def drawmenu(self):
        win.blit(self.bgimg,(0,0))
        win.blit(self.buttons["start"][0],(worldWidth /2-112,300))
        win.blit(self.buttons["options"][0],(worldWidth /2-112,400))
        win.blit(self.buttons["exit"][0],(worldWidth /2-112,500))
        pygame.display.update()
#Вивід налаштувань: там можна вибрати одну з трьох варіантів складності:легкий - монстри рухаються повільно, середній - монстри швидші, і складний - монстри так само швикі як гравець
    def drawoptions(self):
        win.blit(pygame.image.load("backgroundOptions.png"),(0,0))
        win.blit(pygame.image.load("easy.png"),(20,300))
        print(fire_speed)
        if fire_speed == 5:
            win.blit(pygame.image.load("chosen.png"),(300,300))
        win.blit(pygame.image.load("medium.png"),(20,373))
        if fire_speed == 3:
            win.blit(pygame.image.load("chosen.png"),(300,373))
        win.blit(pygame.image.load("hard.png"),(20,446))
        if fire_speed == 1:
            win.blit(pygame.image.load("chosen.png"),(300,446))
        win.blit(pygame.image.load("menu.png"),(20,519))
        pygame.display.update()
        

#1-камінь
#2-дерево
#3-гравець
#4-скриня
#5-вихід
#6-вогник
#7-рубін

#Функція відновлення ігрового поля. Воно зберігається в двовимірному масиві. Пояснення до цифр - вище.
def restore():
    fld =  [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,1,1,1,1,1],
[1,2,3,2,2,2,2,1,1,1,1,1,2,1,1,2,2,2,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1],
[1,2,2,2,2,2,2,1,1,1,2,1,2,1,1,1,1,2,2,2,2,2,2,2,2,2,1,1,1,2,2,2,1,1,1],
[1,2,2,2,2,2,2,1,1,1,2,2,2,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,2,1,2,1,1,1],
[1,2,2,2,2,2,2,1,1,1,1,2,1,1,1,1,1,2,1,2,2,2,1,1,1,2,2,2,2,2,2,2,1,1,1],
[1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,2,2,2,1,1,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1],
[1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,2,1,2,1,1,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
[1,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,2,2,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1],
[1,2,2,2,2,2,2,1,1,1,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,2,2,1,1,1,1,1,1,1],
[1,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,2,1,1,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1],
[1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1],
[1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,2,1,2,2,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,1,2,1,2,1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,2,1,1,1,1,2,2,2,1,1,1],
[1,1,2,1,2,1,2,1,1,1,1,1,1,2,2,2,2,2,1,2,2,1,2,2,2,1,1,1,1,1,1,2,1,1,1],
[1,1,2,2,2,2,2,1,1,1,1,1,1,2,2,2,2,2,1,2,2,1,1,1,1,1,1,1,1,1,1,2,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,2,2,2,2,2,2,2,1,1,1,1,1,2,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1],
[1,1,1,1,1,1,2,2,2,2,2,2,1,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1],
[1,1,1,1,2,2,2,1,1,1,2,2,1,1,2,1,1,2,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1],
[1,1,1,1,2,1,2,2,2,1,2,2,1,1,2,1,1,2,1,1,2,2,2,2,2,2,1,1,1,1,1,2,1,1,1],
[1,1,1,2,2,1,1,2,2,1,2,2,1,1,2,1,1,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1],
[1,2,2,2,2,1,1,2,2,1,2,2,2,2,2,2,2,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1],
[1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1],
[1,2,2,2,1,1,2,2,1,1,1,2,2,2,1,2,1,1,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1,1,1],
[1,1,2,1,1,1,2,2,1,1,1,2,1,2,1,2,2,2,2,2,2,1,1,1,2,1,1,1,1,1,1,1,1,1,1],
[1,1,2,1,1,1,2,2,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1],
[1,1,2,1,1,1,2,2,2,2,2,2,2,2,1,1,5,1,1,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1],
[1,1,2,2,2,2,2,2,1,1,2,1,1,1,1,1,2,2,2,2,1,1,1,1,2,2,2,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    #Генерація рубіна. Він може з'явитися в будь-якій точці карти. Щоб він точно згенерувався, при переборі нижньої частини карти ймовірність його появи я збільшив у 10 разів
    #ruby generation
    for i in range(6,27):
            f = False
            for j in range(1,33):
                if fld[i][j] == 2:
                    r = random.random()
                    if (r < 0.07 and (i-6)*33 + j< 440) or (r<0.7 and j>440):
                        fld[i][j] = 7
                        f = True
                        break
            if f:
                break
    #chest generation
    #Генерація скриньок. Це буде щось типу підзарядки для ліхтарика гравця.
    #Принцип їх генерування такий самий, але їх може бути від 0 до 6.
    k = 0
    for i in range(5,28):
        for j in range(1,33):
            if fld[i][j] == 2:
                r = random.random()
                if (r < 0.05) and k<6:
                    fld[i][j] = 4
                    k+=1
                if k==6:
                    break
    return fld
    
#Клас гри
class game:
    #Основні об'єкти гри field - лабіринт, blocks - масив з текстурами блоків,  man_x,man_y,man_dir - координати гравця та його напрямок
    #dark_rad - видимий радіус гравця, get_rub - чи взяв гравець рубін,  fire - масив з координатами та напрямом руху вогників, man_images - текстурки з гравцем по одній на сторону
    field =  restore()
    blocks = {1: pygame.image.load("stone.png"),2:pygame.image.load("wood.png"),4:pygame.image.load("chest.png"),5:pygame.image.load("finish.png"),6:pygame.image.load("fire.png"),7:pygame.image.load("ruby.png"),8:pygame.image.load("monster.png")}
    man_x,man_y,man_dir = 1,1,"down"
    dark_rad = 4
    get_rub = 0
    fire = [(9,11,"down"),(23,10,"down")]
    man_images = {"up":pygame.image.load("up.png"),"down":pygame.image.load("down.png"),"left":pygame.image.load("left.png"),"right":pygame.image.load("right.png")}
    #Ініціалізація класу(в ній нічого не відбувається)
    def init(self):
        pass
    #Функція обчислення нової координати для вогника. В неї передається кортеж із списку вогників
    def fire_new(self,i):
        #словник із напрямами та змінами координат при русі у матриці. Того спочатку там у- координата, і при русі вгору вона зменшується
        ways = {"left":(0,-1),"right":(0,1),"up":(-1,0),"down":(1,0)}
        #Якщо наступна клітинка в напрямку руху вогника доступна, то вогник переміщується туди 
        if self.field[i[0] + ways[i[2]][0]][i[1] + ways[i[2]][1]]!=1:
            i = (i[0] + ways[i[2]][0],i[1] + ways[i[2]][1],i[2])
            return i
        else:
            #Інакше в масив avi додаються всі доступні клітинки по сусідству з вогником, з них вибирається якась випадкова і вогник рухається туди
            avi = [j for j in ways if self.field[i[0] + ways[j][0]][i[1] + ways[j][1]]!=1]
            rs = random.randint(0,len(avi) - 1)
            i = (i[0],i[1],avi[rs])
            return Gm.fire_new(i)
    #Функція ходу вогників
    def fire_move(self):
        #Обчислення нових їхніх координат
        for i in range(2):
            self.fire[i] = self.fire_new(self.fire[i])
        #Та перевірка на кінець гри. Якщо вогник на одній клітинці з гравцем, то гра викидає повідомлення про поразку та повертається до головного меню
        for i in Gm.fire:
            if Gm.man_y==i[0] and Gm.man_x==i[1]:
                win.blit(pygame.image.load("backgroundGameOver1.png"),(0,0))
                pygame.display.update()
                time.sleep(3)
                global game_mode
                game_mode = 1
    #Функція showback. Вона вимальовує всю гру
    def showback(self,monster):
        #Заповнення вікна чорним кольором
        win.fill((0,0,0))
        #Вивід кнопок меню та "туману"
        win.blit(pygame.image.load("menu.png"),(5,5))
        win.blit(pygame.image.load("smoke.png"),(0,40))
        #Цикл, що проходить по матриці поля
        for i in range(31):
            for j in range(35):
                #Якщо відстань від гравця до клітинки менша за радіус видимості, то вона вимальовуєтся  
                if ((j-self.man_x)**2+(i - self.man_y)**2)**0.5<=self.dark_rad :
                    if self.field[i][j] == 3:
                        win.blit(self.man_images[self.man_dir],(j*20,40+i*20))
                    else:
                        win.blit(self.blocks[self.field[i][j]],(j*20,40+i*20))
        #Вимальовування вогника та монстра. Вони вимальовуются поверх карти
        for i in self.fire:
            if ((i[1]-self.man_x)**2 + (i[0] - self.man_y)**2)**0.5<=self.dark_rad:
                win.blit(self.blocks[6],(i[1]*20,40+i[0]*20))
        #А монстр вимальовуєтся тільки тоді, коли він живий
        if monster.died == 0:
            if ((monster.x-self.man_x)**2 + (monster.y - self.man_y)**2)**0.5<=self.dark_rad:
                win.blit(self.blocks[8],(monster.x*20,40+monster.y*20))
        #Вивід заряду батарейки
        win.blit(pygame.image.load("battery.png"),(10,650))
        for i in range(self.dark_rad - 2):
            win.blit(pygame.image.load("battery_cell.png"),(35 * i + 12  ,653))
    #Вивід часу
    def echotime(self,seconds):
        font = pygame.font.SysFont('Comic Sans MS', 15)
        text = font.render("You have " + str(timer - int(seconds) ) + " seconds to escape", True, (255,255,255))
        win.blit(text, [470, 650] )
    #Функція ходу персонажа. Я назвав її так через те, що вона спочатку мала перевіряти доступні клітинки персонажа.
    def check(self,pos,menu):
        #Якщо клітинка не стіна
        if self.field[pos[0]][pos[1]]!=1:
            #Якщо гравець досягнув фінішу, то з'являється одне з двох повідомлень про перемогу.
            if self.field[pos[0]][pos[1]]==5:
                if self.get_rub == 1:
                    win.blit(pygame.image.load("backgroundGameOver3.png"),(0,0))
                else:
                    win.blit(pygame.image.load("backgroundGameOver2.png"),(0,0))
                pygame.display.update()
                time.sleep(3)
                print("You win")
                global game_mode
                game_mode = 1
            #Якщо гравець став на ящик, то збільшується радіус видимості та зникає ящик
            if self.field[pos[0]][pos[1]]==4:
                self.dark_rad = (Gm.dark_rad + 2 if Gm.dark_rad<=3 else 5)
            #Хід персонажа
            self.field[self.man_y][self.man_x] = 2
            self.man_x = pos[1]
            self.man_y = pos[0]
            self.field[pos[0]][pos[1]] = 3
            self.man_dir = pos[2]
            
#Клас гри і меню            
            
Gm = game()
menu = Menu()
#Клас монстра
class Monster:
    #Координати спрайта, напрям його руху та його "живість"
    x,y,d,died = 5,9,"down",0
    #Рух монстра
    def move(self):
    #Словник з змінами координат під час ходу, та масив зміни напрямів при втечі(escape) та погоні(chase). chase та escape показують напрям погоні чи втечі
        ways = {"left":(0,-1),"right":(0,1),"up":(-1,0),"down":(1,0)}
        esc = {-1:"right",1:"left",-2:"down",2:"up"}
        chs = {-1:"left",1:"right",-2:"up",2:"down"}
        escape = 0
        chase = 0
        #Цикли, що перевіряє 4 клітинки у всі напрямки. Якщо він знайде героя то chase стане -1, якщо герой зліва, 1 - якщо він справа, - 2 - зверху, 2 - знизу.
        #З escape стане те саме, тільки для цього треба, щоб вогник був на якійсь із ліній.
        for i in range(self.x,self.x-5,-1):
            if Gm.field[self.y][i] == 1:
                break
            if Gm.field[self.y][i] == 6:
                escapeh = -1
            if Gm.field[self.y][i] == 3:
                chase = -1
        for i in range(self.x,self.x + 5,1):
            if Gm.field[self.y][i] == 1:
                break
            if Gm.field[self.y][i] == 6:
                escape = 1
            if Gm.field[self.y][i] == 3:
                chase = 1
        for i in range(self.y,self.y-5,-1):
            if Gm.field[i][self.x] == 1:
                break
            if Gm.field[i][self.x] == 6:
                escape = -2
            if Gm.field[i][self.x] == 3:
                chase = -2
        for i in range(self.y,self.y+5,1):
            if Gm.field[i][self.x] == 1:
                break
            if Gm.field[i][self.x] == 6:
                escape = 2
            if Gm.field[i][self.x] == 3:
                chase = 2
        #Якщо монстр помітив героя, то його напрям змінюється в його сторону та  chase стає нулем
        if chase!=0:
            self.d = chs[chase]
            chase = 0
        #Якщо монстр помітив вогника, то він вже приймає певні рішення.
        #Cпочатку відбувається пошук сусідніх доступних клітинок по боках(вогник рухається тільки по прямих). Якщо вони є, то монстр йде в якусь із них.Інакше він йде в 
        #єдину доступну та  escape стає нулем
        elif escape!=0:
            avi = [j for j in ways if Gm.field[self.y + ways[j][0]][self.x + ways[j][1]]!=1 and j!=esc[escape] and j!=self.d]
            if len(avi) == 0:
                self.d = esc[escape]
            elif len(avi)<=2:
                self.d = avi[random.randint(0,len(avi) - 1 )]
            escape = 0
        else:
            #Тут обраховується напрям руху монстра, якщо він близько до гравця
            if ((self.x-Gm.man_x)**2 + (self.y - Gm.man_y)**2)**0.5<=3:
                if self.x>Gm.man_x:
                    self.d = "left"
                elif self.x<Gm.man_x:
                    self.d = "right"
        #Тут обчислюється його напрям, якщо він впреться в стіну.
        if Gm.field[self.y + ways[self.d][0]][self.x + ways[self.d][1]]==1:
            avi = [j for j in ways if Gm.field[self.y + ways[j][0]][self.x + ways[j][1]]!=1 and j!=self.d]
            self.d = avi[random.randint(0,len(avi) - 1) ]
        #Його хід
        self.x = self.x + ways[self.d][1]
        self.y = self.y + ways[self.d][0]
        #Якщо монстр став на клітинку з гравцем, то гравець програє
        if self.x == Gm.man_x and self.y == Gm.man_y and self.died == 0:
            win.blit(pygame.image.load("backgroundGameOver1.png"),(0,0))
            pygame.display.update()
            time.sleep(3)
            game_mode = 1
        #Якщо він став на вогник, то помирає він сам
        for i in Gm.fire:
            if i[1] == self.x and i[0] == self.y:
                self.died = 1
#Cтворення монстра, вимальовування гри, bat_timer - таймер для батарейки, fire_time - таймер для ворогів
monster = Monster()
menu.drawmenu()
Run = True
bat_timer = 0
fire_time = 0
while Run:
 
    #Цикл відбувається кожну секунду
    pygame. time.delay(50)
    #Відслідкування натискань клавіш та інших подій гри
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
    #Обробка виходу
        if event.type == pygame.QUIT:
            Run = False
        #Обробка кліків
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = event.pos
            #Обробка натискань на кнопку старт
            if worldWidth /2-112<=click[0]<=worldWidth /2-112+244 and 300<=click[1]<=348:
                start_ticks=pygame.time.get_ticks()
                game_mode = 3
                Gm.field  = restore()
                Gm.man_x,Gm.man_y,Gm.man_dir,Gm.dark_rad,Gm.get_rub= 2,2,"down",4,0
                Gm.fire = [(9,11,"down"),(23,10,"down")]
                monster.x,monster.y,monster.d,monster.died = 5,9,"down",0
                bat_timer = 0
            #Натискання на кнопку меню
            if worldWidth /2-112<=click[0]<=worldWidth /2-112+244 and 400<=click[1]<=448:
                game_mode = 2
                menu.drawoptions()
            #Вимальовування налаштувань та вибір складності
            if game_mode == 2:
                     if 20<=click[0]<=20+262 and 300<=click[1]<=361:
                        fire_speed = 5
                        fire_speed = 3
                        timer = 90
                     if 20<=click[0]<=20+262 and 446<=click[1]<=446+63:
                        fire_speed = 1
                        timer = 60
                     menu.drawoptions()
                     if 20<=click[0]<=167 and 519<=click[1]<=549:
                        game_mode = 1
                     pygame.display.update()
            #Кнопка виходу з гри
            if worldWidth /2-112<=click[0]<=worldWidth /2-112+244 and 500<=click[1]<=548:
                Run = False
            #Кнопка виходу в меню
            if 5<=click[0]<=172 and 5<=click[1]<=35 and game_mode == 3:
                game_mode = 1
    #Сама гра
    if game_mode == 3:
        #Таймер 
        seconds=(pygame.time.get_ticks()-start_ticks)//1000
        #Якщо гравець має заряджену батарейку, то таймеру батарейки присвоюється поточний час
        if Gm.dark_rad>2 and bat_timer == 0:
            bat_timer = seconds
        #Вивід гри 
        Gm.showback(monster)
        Gm.echotime(seconds)
        pygame.display.update()
        #Обробка натискань кнопок
        neighbs = {pygame.K_LEFT:(Gm.man_y,Gm.man_x-1,"left"),pygame.K_RIGHT:(Gm.man_y,Gm.man_x+1,"right"),pygame.K_DOWN:(Gm.man_y+1,Gm.man_x,"down"),pygame.K_UP:(Gm.man_y-1,Gm.man_x,"up")}
        
        if keys[pygame.K_LEFT]:
                Gm.check(neighbs[pygame.K_LEFT],menu)
        if keys[pygame.K_RIGHT]:
                Gm.check(neighbs[pygame.K_RIGHT],menu)
        if keys[pygame.K_UP]:
                Gm.check(neighbs[pygame.K_UP],menu)
        if keys[pygame.K_DOWN]:
                Gm.check(neighbs[pygame.K_DOWN],menu)
        #Обробка зіткнень гравця з мобами та мобів між собою
        for i in Gm.fire:
            if Gm.man_y==i[0] and Gm.man_x==i[1]:
                win.blit(pygame.image.load("backgroundGameOver1.png"),(0,0))
                pygame.display.update()
                time.sleep(3)
                game_mode = 1
            if monster.y==i[0] and monster.x==i[1]:
                monster.died = 1
        if monster.x == Gm.man_x and monster.y == Gm.man_y and monster.died == 0:
            win.blit(pygame.image.load("backgroundGameOver1.png"),(0,0))
            pygame.display.update()
            time.sleep(3)
            game_mode = 1
        #Збільшення таймеру мобів
        fire_time+=1
        
        #Забирання заряду батарейки кожні 7 секунд
        if seconds -  bat_timer == 7:
            
            Gm.dark_rad-=(1 if Gm.dark_rad > 2 else 0)
            bat_timer = 0
        #Поразка в разі закінчення таймера
        if seconds == timer:
            win.blit(pygame.image.load("backgroundGameOver1.png"),(0,0))
            pygame.display.update()
            time.sleep(5)
            game_mode = 1
        #Вимальовування гри 
        Gm.showback(monster)
        Gm.echotime(seconds)
        if fire_time % fire_speed==0:
            Gm.fire_move()
            monster.move()
            fire_time = 0
    #Вимальовування меню
    elif game_mode==1:
        menu.drawmenu()
        pygame.display.update()

    
pygame.quit()
