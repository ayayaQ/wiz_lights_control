# arduino_wiz.py is a version with support for dual and solo light modes, 
# solo being all lights use the same colors and dual meaning that 2 lights 
# will split the screen and each take half for their colors. An arduino using
# port COM4 can control the on/off state of all lights. 
# 
# Available arguments are either dual or solo or none with solo being default. 
# Usage example: arduino_wiz.py dual

import asyncio
import serial
import sys

from pywizlight import wizlight, PilotBuilder, discovery

from screen import screen_average_colors, dual_screen_average_colors


async def main():

    dual = get_mode_from_args()

    # find lights
    bulbs = await discovery.discover_lights(broadcast_space="10.0.0.255")

    ser = serial.Serial(timeout=0, baudrate=9600,
                        port='COM4', bytesize=serial.EIGHTBITS)

    lights = []

    for i in range(len(bulbs)):
        light = wizlight(bulbs[i].ip)
        lights.append(light)

    print(len(lights), "lights found.")

    # block until serial is ready
    while ser.in_waiting != 7:
        continue
    print("Serial Ready")
    ser.read_all()

    on = lights[0] or lights[1]

    while True:

        if(ser.in_waiting and ser.in_waiting != 7):
            received = ser.read_all()
            if(received == b'1'):

                for light in lights:
                    await light.updateState()
                    on = on or light.status

                if(on):
                    for light in lights:
                        await light.turn_off()
                on = not on

        if(on):
            if (not dual):

                rgb_vals = await screen_average_colors()
                bright_val = calc_brightness(rgb_vals)

                for light in lights:
                    await light.turn_on(PilotBuilder(rgb=rgb_vals, brightness=255))
            else:

                rgb_vals_left, rgb_vals_right = await dual_screen_average_colors()
                bright_val_left, bright_val_right = calc_brightness(
                    rgb_vals_left), calc_brightness(rgb_vals_right)

                await lights[0].turn_on(PilotBuilder(rgb=rgb_vals_left, brightness=bright_val_left))
                await lights[1].turn_on(PilotBuilder(rgb=rgb_vals_right, brightness=bright_val_right))


def calc_brightness(rgb_vals):
    """Get brightness based on the max average from rgb"""
    return max(rgb_vals)


def get_mode_from_args():
    """Gather either dual mode or solo mode from command argument, if invalid exit."""
    if(len(sys.argv) == 2):
        # get mode dual or solo
        arg = sys.argv[1]
        if(arg == 'solo' or arg == 'dual'):
            if(arg == 'dual'):
                return True
        else:
            sys.exit("Invalid argument" + arg +
                     "The value should either be dual or solo. eg. 'arduino_wiz.py dual'")
    elif(len(sys.argv) > 2):
        sys.exit(
            "Only 1 argument allowed maximum. The value should either be dual or solo. eg. 'arduino_wiz.py dual'")

    return False


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
