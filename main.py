import game
import game.constants as constants
import util

if __name__ == "__main__":
    window = util.Window(constants.SCREEN_SIZE, "Mini Golf", force_quit=True)
    game = game.Game(window.screen)

    while True:
        game.update()
        window.update()
        if game.is_over:
            break
