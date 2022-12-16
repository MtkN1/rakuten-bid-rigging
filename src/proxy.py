import asyncio

import httpx
from dotenv import dotenv_values
from rich.pretty import pprint


async def main():
    ids = ("ENV/a.env", "ENV/b.env")

    for path in ids:
        pprint(path)
        env = dotenv_values(path)
        proxy_url = httpx.URL(env.get("PROXY_URL"))
        pprint(proxy_url)
        async with httpx.AsyncClient(proxies=proxy_url) as client:
            r = await client.get("https://httpbin.org/get")
        content = r.json()
        pprint(r.request.headers)
        pprint(r.headers)
        pprint(content)
        pprint(
            f"{proxy_url.host} {'==' if proxy_url.host == content['origin'] else '!='} {content['origin']}"  # noqa
        )
        print()


if __name__ == "__main__":
    asyncio.run(main())
