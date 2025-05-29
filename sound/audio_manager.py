import pygame
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AudioManager:
    def __init__(self):
        try:
            # Initialize audio channels and sounds
            self.channels = {
                'movement': pygame.mixer.Channel(0),
                'effects': pygame.mixer.Channel(1),
                'ambient1': pygame.mixer.Channel(2),
                'ambient2': pygame.mixer.Channel(3)
            }
            self.sounds = {
                'move': pygame.mixer.Sound('sound/moving.wav'),
                'fall': pygame.mixer.Sound('sound/fall_in_pit.wav')
            }
        except (pygame.error, FileNotFoundError) as e:
            logger.error(f"Failed to load audio: {e}")
            self.sounds = {}
            self.channels = {}

    # Play the specified sound if channels and sounds are available
    def play_sound(self, sound_name):
        if not self.sounds or not self.channels:
            return

        try:
            channel = self.channels['effects']
            if sound_name == 'move':
                channel = self.channels['movement']

            channel.play(self.sounds[sound_name])
            channel.set_volume(1.0)
            channel.fadeout(450)

        except (KeyError, pygame.error) as e:
            logger.warning(f"Failed to play sound {sound_name}: {e}")