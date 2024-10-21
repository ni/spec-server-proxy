"""NI SCM Proxy Server is a Python server used for getting SLE Products information using \
    SCM End points."""

import asyncio

from ni_spec_server_proxy.main import run

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(run())
