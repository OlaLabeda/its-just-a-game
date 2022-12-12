from classes import Game, Player, Enemy, DragonHydra

def main():
    player = Player('Zenek Blazenek', 20)
    enemies = [
        Enemy('orc', 15),
        Enemy('Dwarf', 10),
        DragonHydra('Green hydra', 20, 3)
    ]
    game = Game(player, enemies)
    game.play(10)

if __name__ == "__main__":
    main()