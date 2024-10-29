import click
import asyncio
import socket


from .probes import iperf, mtr


@click.command()
@click.argument('host', nargs=1)
@click.option('--comment', '-c')
@click.pass_context
def main(ctx, host, comment):
    o = ctx.obj = {}
    o['host'] = host
    loop = asyncio.get_event_loop()

    async def collect():
        async def info():
            addrinfo = await loop.getaddrinfo(host, 1)
            o['canonip'] = canonip = addrinfo[2][4][0]
            canonhost, *_ = socket.gethostbyaddr(canonip)
            o['canonhost'] = canonhost
            o['comment'] = comment
            L = [host, f'({canonhost} -> {canonip})']
            if comment:
                L.append(comment)
            click.echo(' '.join(L))
        await asyncio.gather(info())
        mtr_report = await mtr(o)
        last_hub = mtr_report['report']['hubs'][-1]

        def g(key):
            return round(float(last_hub[key]), 2)
        o['best'] = g('Best')
        o['avg'] = g('Avg')
        o['worst'] = g('Wrst')
        o['stddev'] = g('StDev')
        keys = 'best avg worst stddev'.split(' ')
        L = [
            'MTR PING',
            '/'.join(k for k in keys),
            '/'.join(str(o[k]) for k in keys),
            'ms',
        ]
        click.echo(' '.join(L))

        async def iperf_bits_per_second(reverse=False):
            report = await iperf(o, reverse)
            attr = 'received_Mbps' if reverse else 'sent_Mbps'
            return round(getattr(report, attr), 1)
        o['up'] = await iperf_bits_per_second()
        o['down'] = await iperf_bits_per_second(True)
        s = f'IPERF    up/down               {o["up"]}/{o["down"]} Mbps'
        click.echo(s)
    g = asyncio.gather(collect())
    loop.run_until_complete(g)
    loop.close()
