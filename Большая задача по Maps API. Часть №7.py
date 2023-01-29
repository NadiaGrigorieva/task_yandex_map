import pygame, requests, sys, os, math
 
    
class MapParams(object):
    def __init__(self):
        self.lat = 55.789482
        self.lon = 49.138726
        self.zoom = 16 
        self.type = b[0]
        self.s = ""

    def ll(self):
        return str(self.lon)+","+str(self.lat)

    def change(self):
        self.type = b[m]

    def upp(self, event):
        if event.unicode == "\x08":
            self.s = self.s[:-1]
            return ""
        elif event.unicode == "\r":
            pass
        else:
            self.s += event.unicode
            return event.unicode

    def cen(self):
        global coords
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
                            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                            "geocode": self.s,
                            "format": "json",
                           }

        response = requests.get(geocoder_api_server, params=geocoder_params)
        if response:
            json_response = response.json()
            features = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = features["Point"]["pos"]
        toponym_coodrinates = toponym_coodrinates.split(" ")
        self.lat = float(toponym_coodrinates[1])
        self.lon = float(toponym_coodrinates[0])
        coords = (self.lon, self.lat)

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
    global fl, coords
    if not fl:
        map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
        response = requests.get(map_request)
    else:
        map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}&pt={co}".format(ll=mp.ll(),
                                                                                                z=mp.zoom, type=mp.type,
                                                                                                co=str(coords[0]) + ',' + str(coords[1]))
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
    global b, m, fl, coords
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
    text3 = smallfont.render("Сброс поискового результата", True, color)
    x3, y3 = 650, 180
    text1 = smallfont.render("", True, color)
    x1, y1 = 650, 80
    text2 = smallfont.render("Искать", True, color)
    s = ""
    x2, y2 = 650, 130
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
            if event.key in [1073741899, 1073741902, 1073741904, 1073741903, 1073741906, 1073741905]:
                mp.update(event)
            else:
                d = mp.upp(event)
                if d:
                    s += d
                else:
                    s = s[:-1]
                text1 = smallfont.render(s, True, color)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if x <= mouse[0] <= x + 140 and y <= mouse[1] <= y + 40:
                m = (m + 1) % 3
                text = smallfont.render(a[m], True, color)
                mp.change()
            if x2 <= mouse[0] <= x2 + 140 and y2 <= mouse[1] <= y2 + 40:
                mp.cen()
                fl = True
            if x3 <= mouse[0] <= x3 + 140 and y3 <= mouse[1] <= y3 + 40:
                mp.cen()
                fl = False
        map_file = load_map(mp)
        screen.fill(pygame.Color("black"))
        screen.blit(pygame.image.load(map_file), (0, 0))
        if x <= mouse[0] <= x + 140 and y <= mouse[1] <= y + 40:
            pygame.draw.rect(screen, color_light, [x, y, 140, 40])
        else:
            pygame.draw.rect(screen, color_dark, [x, y, 140, 40])
        if x2 <= mouse[0] <= x2 + 140 and y2 <= mouse[1] <= y2 + 40:
            pygame.draw.rect(screen, color_light, [x2, y2, 140, 40])
        else:
            pygame.draw.rect(screen, color_dark, [x2, y2, 140, 40])
        if x3 <= mouse[0] <= x3 + 140 and y3 <= mouse[1] <= y3 + 40:
            pygame.draw.rect(screen, color_light, [x3, y3, 140, 40])
        else:
            pygame.draw.rect(screen, color_dark, [x3, y3, 140, 40])
        screen.blit(text, (x, y))
        screen.blit(text1, (x1, y1))
        screen.blit(text2, (x2, y2))
        screen.blit(text3, (x3, y3))
        pygame.display.flip()
    os.remove(map_file)
    
   
if __name__ == "__main__":
    b = ['map', 'sat', 'sat,skl']
    m = 0
    coords =()
    fl = False
    main()
