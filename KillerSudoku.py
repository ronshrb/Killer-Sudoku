
import GameSetup, Game

def main(user=''):
    setup = GameSetup.GameSetup(user)
    game_number, level, user = setup.run()
    game = Game.Game(game_number, level, user)
    game.run()

if __name__ == "__main__":
    main()