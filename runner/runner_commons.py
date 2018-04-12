from pygame import mixer
from time import sleep
from os.path import join


def sound_notification():
    mixer.init()
    mixer.music.load(join("runner", "sounds", "slow-spring-board.mp3"))
    mixer.music.play(0)
    while mixer.music.get_busy():
        sleep(0.1)
        pass


def sound_notification_and_quit(onQuit):
    sound_notification()
    onQuit()
    import sys
    sys.exit(0)
