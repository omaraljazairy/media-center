import logging
logger = logging.getLogger('player')
import pygame

class Player:

    def playsound(self,soundfile):
        """Play sound through default mixer channel in blocking manner.
           This will load the whole sound into memory before playback
        """

        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound(soundfile)
        clock = pygame.time.Clock()
        sound.play()
        while pygame.mixer.get_busy():
            print("Playing...",clock.tick(1000))


    def play(self,song):
        """
        This function receives a song dict with name and file with complete path.
        it plays it and returns the eventtype it get while playing.
        """
        logger.debug("song received: %s", song)
        play = True #setting the play variable to True
        SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(SONG_END)
        """ initializing the pygame and mixer """
        pygame.init()
        pygame.mixer.init()

        try:
            pygame.mixer.music.load(song['file'])
            pygame.mixer.music.play()
            logger.info("playing: %s", song['name'])

            while play:
                for event in pygame.event.get(): #pygame has many events and I want to know if it's song_end or another one
                    if event.type == SONG_END: #if event is 25 then
                        logger.info("Song %s has finished", song['name'])
                        play = False
                        return event.type
                    else:
                        logger.debug("eventtype: %s and song has not finished", str(event.type))
                        play = False
                        return event.type

        except Exception as e:
            logger.error("couldn't play song: %s", song['name'])
