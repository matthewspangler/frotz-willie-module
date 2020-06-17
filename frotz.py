from willie import module
import pexpect
import os

#This is the trigger that will allow you to interact with the game:
game_trigger = ">>>"

class IFGame:
    def __init__(self, bot, game):
        self.tweak = ["zork.z5", "hhgg.z5"] #these games need tweaked to work correctly
        self.game = game
        self.playing = pexpect.spawn('./dfrotz -h 2000 ./games/%s' % self.game)
        self.prompts = [">", "#", "\$", "}", '%', pexpect.TIMEOUT]
        self.divider = "\x02============================================================================|"
        self.playing.expect(self.prompts)
        bot.say(self.divider)
        for line in self.playing.before.decode().split('\n'):
            bot.say(line)
        bot.say(self.divider)
        if not self.game in self.tweak:
            self.playing.expect(self.prompts)

    def action(self, bot, command):
        bot.say(self.divider)
        self.playing.sendline(command)
        self.playing.expect(self.prompts)
        for line in self.playing.before.decode().split('\n'):
            bot.say(line)
        bot.say(self.divider)
        if not self.game in self.tweak:
            self.playing.expect(self.prompts)

    def endgame(self):
        self.playing.close()

@module.rule(game_trigger)
def action(bot, trigger):
    if not bot.memory.contains(trigger.sender):
        bot.say('\x02You must start a game first. To start a game, type ".startgame <game>" (without quotes).')
        bot.say('\x02For example: .startgame adventure.z5')
        return
    command = trigger.split(game_trigger, 1)[1]
    bot.memory[trigger.sender].action(bot, command)

@module.commands('endgame')
def end(bot, trigger):
    if not bot.memory.contains(trigger.sender):
        bot.say("\x02No games are running at the moment.")
        return
    bot.memory[trigger.sender].endgame()
    bot.memory.pop(trigger.sender, None)
    bot.say("\x02The interactive fiction game has been terminated.")

@module.commands('startgame')
def start(bot, trigger):
    if not bot.memory.contains(trigger.sender):
        if trigger.group(2) == None:
            bot.say("\x02Please specifiy a game! To get a list of games, type .listgames")
        else:
            bot.say('\x02To interact with the game, type "%s action" (without quotes), for example: %slook around'
                    % (game_trigger, game_trigger))
            bot.say('\x02If you would like to end the game, type ".endgame" (without quotes)')
            bot.say('\x02Starting a new interactive fiction game, please wait...')
            try:
                bot.memory[trigger.sender] = IFGame(bot, trigger.group(2).split()[0])
            except:
                bot.say("\x02The game failed to start! Maybe you typed the name incorrectly?")
    else:
        bot.say("\x02A game is already in progress.")
        bot.say('\x02If you would like to end the game, type ".endgame" (without quotes)')

@module.commands('listgames')
def listgames(bot, trigger):
    valid_extensions = [".z1", ".z2", ".z3", ".z4", ".z5", ".z6", ".z7", ".z8", ]
    files = os.listdir("games")
    valid_files = []
    for file in files:
        for extension in valid_extensions:
            if file.endswith(extension):
                valid_files.append(file)
    bot.say("\x02Availible games: %s" % ', '.join(valid_files))
    bot.say('\x02To start a game, type ".startgame <game>" (without quotes)')
    bot.say('\x02For example: .startgame adventure.z5')