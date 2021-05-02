# wiz_dual.py is a version with only support for dual mode and no arduino control.

import asyncio

from pywizlight import wizlight, PilotBuilder, discovery

from screen import dual_screen_average_colors


async def main():

    bulbs = await discovery.discover_lights(broadcast_space="10.0.0.255")

    lights = []

    for i in range(len(bulbs)):
        light = wizlight(bulbs[i].ip)
        lights.append(light)

    print(lights)

    while True:
        rgb_vals_left, rgb_vals_right = await dual_screen_average_colors()
        #bright_val = calc_brightness(rgb_vals)
        await lights[0].turn_on(PilotBuilder(rgb=rgb_vals_left))
        await lights[1].turn_on(PilotBuilder(rgb=rgb_vals_right))

def calc_brightness(rgb_vals):
    return max(rgb_vals)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
