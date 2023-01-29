import pygame, requests, sys, os, math
 
    
class MapParams(object):
    def __init__(self):
        self.lat = 55.789482
        self.lon = 49.138726
        self.zoom = 16 
        self.type = b[0] 

    def ll(self):
        return str(self.lon)+","+str(self.lat)

    def change(self):
        self.type = b[m] 

    def update(self, event):
        my_step = 0.008
        if event.key == 1073741899 and self.zoom < 19: 
            self.zoom += 1
        elif event.key == 1073741902 and self.zoom > 2:
            self.zoom -= 1
        elif event.key == 1073741904: 
            self.lon -= my_step * math.pow(2, 15 - self.zoom)
            if not(-180 <= self.lon <= 180):
                self.lon = 180 - abs(180 + self.lon)
        elif event.key == 1073741903:  
            self.lon += my_step * math.pow(2, 15 - self.zoom)
            if not(-180 <= self.lon <= 180):
                self.lon = -180 + abs(180 - self.lon)
        elif event.key == 1073741906 and self.lat + my_step * math.pow(2, 15 - self.zoom) < 85: 
            self.lat += my_step * math.pow(2, 15 - self.zoom)
        elif event.key == 1073741905 and self.lat - my_step * math.pow(2, 15 - self.zoom) > -85:  
            self.lat -= my_step * math.pow(2, 15 - self.zoom)
 

def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file


def main():
    global b, m
    pygame.init()
    screen = pygame.display.set_mode((800, 450))
    a = ['схема', 'спутник', 'гибрид']
    b = ['map', 'sat', 'sat,skl']
    m = 0
    color = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)

    smallfont = pygame.font.SysFont('Corbel', 35)
    text = smallfont.render(a[m], True, color)
    x, y = 650, 30
    
    mp = MapParams()
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
           running = False
           pygame.quit()
           break
        elif event.type == pygame.KEYUP:
            mp.update(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if x <= mouse[0] <= x + 140 and y <= mouse[1] <= y + 40:
                m = (m + 1) % 3
                text = smallfont.render(a[m], True, color)
                mp.change()
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        if x <= mouse[0] <= x + 140 and y <= mouse[1] <= y + 40:
            pygame.draw.rect(screen, color_light, [x, y, 140, 40])
        else:
            pygame.draw.rect(screen, color_dark, [x, y, 140, 40])
        screen.blit(text, (x, y))
        
        pygame.display.flip()
    os.remove(map_file)
    
   
if __name__ == "__main__":
    b = ['map', 'sat', 'sat,skl']
    m = 0
    main()
