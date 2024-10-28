from asyncio.subprocess import Process
from asyncio import create_subprocess_exec
import asyncio
import iperf3
import subprocess
import json


_DEF_DURATION = 5


async def iperf(obj, reverse: bool = False, duration: int = _DEF_DURATION):
    client = iperf3.Client()
    client.duration = duration
    client.server_hostname = obj['host']
    client.reverse = reverse
    return client.run()


async def mtr(obj, count: int = _DEF_DURATION):
    command = ['mtr', '-rjc', str(count), '--', obj["host"]]
    c = await create_subprocess_exec(
        *command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert c.stderr
    assert c.stdout
    stdout, stderr = await c.communicate()
    if c.returncode or stderr:
        raise RuntimeError(stderr)
    return json.loads(stdout)
