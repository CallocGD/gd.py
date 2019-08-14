"""Example that shows getting current daily/weekly levels.
Author: NeKitDS.
"""

import gd

client = gd.Client()  # an entry point to gd API

# let's create one coroutine to use
# gd.run() only once.

async def coro():
    # getting daily...
    daily = await client.get_daily()
    # getting weekly...
    weekly = await client.get_weekly()
    # now let's print...
    info = f"""Current daily level: {daily!r};
    Current weekly demon: {weekly!r}.
    """
    print(info)

# run a coroutine
gd.utils.run(coro())
