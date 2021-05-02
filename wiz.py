# wiz.py is a version with only support for solo mode and no arduino control.

import asyncio

from pywizlight import wizlight, PilotBuilder, discovery

from screen import screen_average_colors


async def main():

    bulbs = await discovery.discover_lights(broadcast_space="10.0.0.255")

    lights = []

    for i in range(len(bulbs)):
        light = wizlight(bulbs[i].ip)
        lights.append(light)

    print(len(lights), "lights found.")


    while True:
        rgb_vals = await screen_average_colors()
        #bright_val = calc_brightness(rgb_vals)
        for light in lights:
            await light.turn_on(PilotBuilder(rgb=rgb_vals))

def calc_brightness(rgb_vals):
    return max(rgb_vals)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
