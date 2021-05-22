import RPi.GPIO as GPIO
import soco
import threading
import Adafruit_ADS1x15
from rpi_ws281x import *
import time
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
strip = Adafruit_NeoPixel(12,18,800000,10,False,50,0)
strip.begin()
device = soco.discovery.by_name('Baby Room')

last_button_push = int(time.time())
last_volume_level = 2

baris_manco_tracks = ["x-file-cifs://raspberrypi/share/baris_manco/Ayi.mp3",
                      "x-file-cifs://raspberrypi/share/baris_manco/ArkadasimEsek.mp3",
                      "x-file-cifs://raspberrypi/share/baris_manco/DomatesBiberPatlican.mp3",
                      "x-file-cifs://raspberrypi/share/baris_manco/NaneLimonKabugu.mp3"]
mfo_tracks = ["x-file-cifs://raspberrypi/share/mfo/DeliDeli.mp3",
                "x-file-cifs://raspberrypi/share/mfo/VakTheRock.mp3"]
toddler_tune_tracks = ["x-file-cifs://raspberrypi/share/cocuk/CekirdeksizDomates.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/KirmiziBalik.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/KucukKurbaga.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/AliBaba.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/Gunaydin.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/WeAreTheDinosaurs.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/BabyShark.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/TwinkleTwinkleLittle Star.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/KarincaSarkisi.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/ThisIsTheWay.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/SesameStreetElmosSong.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/KermitAlongRainbowConnection.mp3",
                "x-file-cifs://raspberrypi/share/cocuk/OriginalThemeSongTheMuppetShow.mp3"]
sanat_tracks = ["x-file-cifs://raspberrypi/share/sanat/Carmen.mp3",
                "x-file-cifs://raspberrypi/share/sanat/BrahmsHungarianDanceNo5.mp3",
                "x-file-cifs://raspberrypi/share/sanat/VotreToastToreadorCarmen.mp3"]
new_release_tracks = ["x-file-cifs://raspberrypi/share/new_releases/HIP-HOP.mp3",
                      "x-file-cifs://raspberrypi/share/new_releases/BohemianRhapsodyMuppets.mp3",
                      "x-file-cifs://raspberrypi/share/new_releases/MuppetsStayinAlive.mp3",
                      "x-file-cifs://raspberrypi/share/new_releases/OdeToJoyMuppets.mp3",
                      "x-file-cifs://raspberrypi/share/new_releases/SesameStreetFeist1-2-3-4.mp3",
                      "x-file-cifs://raspberrypi/share/new_releases/CantStopTheFeelingTROLLS.mp3"]

def button1_callback(channel):
    play_track(get_random_track(toddler_tune_tracks))
    
def button2_callback(channel):
    play_track(get_random_track(baris_manco_tracks))
    
def button3_callback(channel):
    play_track(get_random_track(sanat_tracks))
    
def button4_callback(channel):
    play_track(get_random_track(mfo_tracks))
    
def button5_callback(channel):
    play_track(get_random_track(new_release_tracks))
    
def get_random_track(tracks):
    track_index = random.randrange(len(tracks))
    return tracks[track_index]

def play_track(track_url):
    global last_button_push
    elapsed_time = int(time.time()) - last_button_push
    if elapsed_time > 1 :
        try:
            print("Playing track: "+ track_url)
            #device.pause()
            last_button_push += elapsed_time
            device.play_uri(track_url)
        except:
            print("Play error:", sys.exc_info()[0])

def update_volume():
    global last_volume_level
    threading.Timer(0.1, update_volume).start()
    volume = read_volume() 
#    print("Volume is at: "+ str(volume))
    first_led = 4
    led_count = 12
    volume_level = int(volume * 11) + 1
    if last_volume_level != volume_level:
        try: 
            last_volume_level = volume_level
            for i in range(volume_level):
                strip.setPixelColor((i+first_led) % led_count, get_volume_color(volume))
            for i in range(volume_level, 12):
                strip.setPixelColor((i+first_led) % led_count, Color(0, 0, 0))
            strip.show()
            device.volume = (volume_level * 3) + 5
        except:
            print("Volume error:", sys.exc_info()[0])

def get_volume_color(volume): 
    color = round(volume * 255)
    return Color(color , 255 - color, 0)

def read_volume():
#    return 5
    analog_value = adc.read_adc(0, gain=GAIN)
    return (analog_value / 33000) if analog_value < 33000 else 1


update_volume()
print("Device ready. Press a button!")
GPIO.setup(13, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, GPIO.PUD_UP)


GPIO.add_event_detect(13,GPIO.FALLING,callback=button1_callback)
GPIO.add_event_detect(15,GPIO.FALLING,callback=button2_callback)
GPIO.add_event_detect(16,GPIO.FALLING,callback=button3_callback)
GPIO.add_event_detect(18,GPIO.FALLING,callback=button4_callback)
GPIO.add_event_detect(22,GPIO.FALLING,callback=button5_callback)


#message = input("Press enter to quit\n\n") # Run until someone presses enter
while True:
    update_volume()
    time.sleep(800)
GPIO.cleanup() # Clean up
