import interaction
import player
import screen
import werewolf


def main():
    # The line of code below loads the default map at the beginning of the game.
    # Using a similar function in the interaction module, replace this function call with a different
    # function call that will load gameSlot0.txt (or the default map if it cannot load gameSlot0.txt).

    interaction.doLoadGame(gameSlot='0', loadDefaultMapOnFailure=True)

    while True:
        screen.clearScreen()
        screen.printScreen()
        interaction.lastMessage = ""
        inputFromKeyboard = interaction.readCharacterInput()
        if inputFromKeyboard == interaction.KEYBOARD_QUIT:
            break
        if not player.playerIsAlive():
            interaction.lastMessage = "You have died."
        interaction.doCommand(inputFromKeyboard)
        werewolf.doWerewolfNextMove(player.playerX, player.playerY)
        interaction.doCheckForPlayerDamage()


if __name__ == '__main__':
    # This if statement causes the game to start.
    main()

