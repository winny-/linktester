import click
import asyncio
import socket


from .probes import iperf, mtr


@click.command()
@click.argument('host', nargs=1)
@click.pass_context
def main(ctx, host):
    o = ctx.obj = {}
    o['host'] = host
    loop = asyncio.get_event_loop()
    async def collect():
        async def info():
            addrinfo = await loop.getaddrinfo(host, 1)
            canonip = addrinfo[2][4][0]
            canonhost, *_ = socket.gethostbyaddr(canonip)
            click.echo(f'{host} ({canonhost} -> {canonip})')
        await asyncio.gather(info())
        mtr_report = await mtr(o)
        last_hub = mtr_report['report']['hubs'][-1]
        def g(key):
            return round(float(last_hub[key]), 2)
        click.echo(f'MTR PING best/avg/worst/stddev {g("Best")}/{g("Avg")}/{g("Wrst")}/{g("StDev")} ms')
        async def iperf_bits_per_second(reverse=False):
            report = await iperf(o, reverse)
            if reverse:
                return round(report.received_Mbps)
            else:
                return round(report.sent_Mbps)
        click.echo(f'IPERF    Up/Down {await iperf_bits_per_second()}/{await iperf_bits_per_second(True)} Mbps')
    g = asyncio.gather(collect())
    loop.run_until_complete(g)
    loop.close()
