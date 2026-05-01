import game, db
import pygame

def main():
    result = game.menu()
    if result is not None:
        score, nickname = result
        db.launch(2, nickname, score)
        print(f"Saved: {nickname} - {score}")
    pygame.quit()

if __name__ == '__main__':
    main()