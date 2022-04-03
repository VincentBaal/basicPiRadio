import signal
import time

import RPi.GPIO as GPIO
import vlc

# Setup channels and their corresponding led pins
CHANNELS = [["http://direct.fipradio.fr/live/fip-midfi.mp3", 21],
            ["https://broadcast.miami/proxy/salsoul?mp=/stream/;", 20],
            ["http://node-32.zeno.fm/1p1xshe85wquv?zs=1cH5mhEURSKOO1DvA1_jsQ&zs=SUS9ydjCTt-"
             "QCpgu5rRljg&rj-ttl=5&rj-tok=AAABf-cnblQAawWI0YlFxm086A", 16],
            ["https://22323.live.streamtheworld.com/WEB10_MP3_SC", 12]]

player = None
currentChannel = 0


def previous_callback(c):
    print("Previous")
    global currentChannel
    if currentChannel == 0:
        currentChannel = len(CHANNELS) - 1
    else:
        currentChannel -= 1
    print("current channel is " + str(currentChannel + 1))
    setup_channel()


def next_callback(c):
    print("Next")
    global currentChannel
    if currentChannel == len(CHANNELS) - 1:
        currentChannel = 0
    else:
        currentChannel += 1
    print("current channel is " + str(currentChannel + 1))
    setup_channel()


# Prepare pins. Output for led and input for buttons
def setup_pins():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)

    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def setup_button_callbacks():
    GPIO.add_event_detect(6, GPIO.FALLING, callback=previous_callback, bouncetime=100)
    GPIO.add_event_detect(5, GPIO.FALLING, callback=next_callback, bouncetime=100)


def setup_channel():
    global player
    if player is not None:
        print("Stopping old player")
        player.stop()

    for channel in CHANNELS:
        GPIO.output(channel[1], GPIO.LOW)
    GPIO.output(CHANNELS[currentChannel][1], GPIO.HIGH)

    player = vlc.MediaPlayer(CHANNELS[currentChannel][0])
    player.play()


def flash_lights():
    i = 1
    while i < 5:
        if i % 2 != 0:
            for channel in CHANNELS:
                GPIO.output(channel[1], GPIO.HIGH)
        else:
            for channel in CHANNELS:
                GPIO.output(channel[1], GPIO.LOW)
        time.sleep(0.25)
        i += 1


def main():
    print("Starting piRadio.")
    GPIO.setwarnings(False)
    setup_pins()
    flash_lights()
    setup_button_callbacks()
    setup_channel()

    # pause the program until SIGINT
    signal.pause()


if __name__ == "__main__":
    main()
