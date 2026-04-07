import pygame, sys, os, math
print(os.listdir(r"C:\Users\Lenovo\Desktop\Practice\9\music_player\music"))

_cached_fonts = {}

def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names 
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            print("available font found:", choice)
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)

def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font

_cached_text = {}
def create_text(text, fonts, size, color):
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    print("key: ", key)
    image = _cached_text.get(key, None)
    if image == None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image

class MusicPlayer:
    def __init__(self):
        self.song = ""
    def progress(self):
        return math.ceil(pygame.mixer.music.get_pos() / 1000)
    def length(self):
        return math.ceil(pygame.mixer.Sound(self.song).get_length())

    def play_song(self, song):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
    def pause_song(self):
        pygame.mixer.music.pause()
    def unpause_song(self):
        pygame.mixer.music.unpause()
        
    
list_of_songs = os.listdir(r"C:\Users\Lenovo\Desktop\Practice\9\music_player\music")
music_player = MusicPlayer()
length = 0
for song in list_of_songs:
    list_of_songs[list_of_songs.index(song)] = r"C:\Users\Lenovo\Desktop\Practice\9\music_player\music\\" + song
def run():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    pygame.display.set_caption("Music Player")
    k = 0
    length = 0
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_p:
                    music_player.song = list_of_songs[k]
                    music_player.play_song(list_of_songs[k])
                    length = str(music_player.length()//60) + ":" + str(music_player.length()%60).zfill(2)
                elif event.key == pygame.K_s:
                    if pygame.mixer.music.get_busy():
                        music_player.pause_song()
                    else:
                        music_player.unpause_song()
                elif event.key == pygame.K_n:
                    k = (k + 1) % len(list_of_songs)
                    music_player.play_song(list_of_songs[k])
                    length = str(music_player.length()//60) + ":" + str(music_player.length()%60).zfill(2)

                elif event.key == pygame.K_b:
                    k = (k - 1) % len(list_of_songs)
                    music_player.play_song(list_of_songs[k])
                    length = str(music_player.length()//60) + ":" + str(music_player.length()%60).zfill(2)

                elif event.key == pygame.K_q:
                    pygame.quit()
        prog = music_player.progress()
        text = create_text(f"{list_of_songs.index(list_of_songs[k])+1}. {str(list_of_songs[k].split('\\')[-1])}", ["Arial", "Comic Sans MS"], 50, (0, 0, 0)).convert_alpha()
        screen.blit(text, (10, 10))

        status = f"Playing" if pygame.mixer.music.get_busy() else "Paused"
        text = create_text(status, ["Arial", "Comic Sans MS"], 30, (0, 0, 0)).convert_alpha()
        screen.blit(text, (10, 70))

        j = create_text(f"{prog} / {length}", ["Arial", "Comic Sans MS"], 30, (0, 0, 0)).convert_alpha()
        screen.blit(j, (10, 110))

        pygame.draw.line(screen, (255, 0, 0), (0, 535), (prog, 535), 5)
        pygame.draw.line(screen, (0, 0, 0), (0, 540), (1920, 540), 5)
        pygame.display.flip()
    



run()