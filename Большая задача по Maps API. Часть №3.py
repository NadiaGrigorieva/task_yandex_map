import pygame, requests, sys, os, math
 
 
class MapParams(object):
    def __init__(self):
        self.lat = 55.789482
        self.lon = 49.138726
        self.zoom = 16 
        self.type = "map" 

    def ll(self):
        return str(self.lon)+","+str(self.lat)

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
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapParams()
    running = True
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
           running = False
           pygame.quit()
           break
        elif event.type == pygame.KEYUP:
            mp.update(event)
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    os.remove(map_file)
    
   
if __name__ == "__main__":
    main()
