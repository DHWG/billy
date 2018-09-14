import logging
import os
import hashlib
import time
from google.cloud import texttospeech
import pygame

_log = logging.getLogger(__name__)

_client = texttospeech.TextToSpeechClient()

_voice = texttospeech.types.VoiceSelectionParams(language_code='en-US', name='en-US-Standard-B')

_audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

pygame.init()
pygame.mixer.init()

def say(text):
    """Synthesises and outputs the given text."""
    _log.info('Speaking: {}'.format(text))
    hash_v = hashlib.md5(text.encode('utf8')).hexdigest()
    file_name = os.path.join('/tmp/tts-{}.mp3'.format(hash_v))
    if not os.path.isfile(file_name):
        _log.info('Synthesising because not cached.')
        synthesis_input = texttospeech.types.SynthesisInput(text=text)
        response = _client.synthesize_speech(synthesis_input, _voice, _audio_config)
        with open(file_name, 'wb') as out:
            out.write(response.audio_content)

    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
