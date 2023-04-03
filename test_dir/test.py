import asyncio

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

domain = "https://www.dtek-kem.com.ua/"


async def request_site(url: str) -> None:
    async with ClientSession() as session:
        session.cookie_jar.update_cookies(
            {"incap_ses_471_2224657": "mS29Z4IQJRQpozYH3FSJBnMRB2QAAAAAT/SaSFMZsJ2eApKNf499gQ=="})

        print(f"req {0} cookies:")
        for cookie in session.cookie_jar:
            print(cookie)
        print("\n")

        resp = await session.get(url)
        await print_request(session, resp, 0)


async def print_request(session: aiohttp.ClientSession, resp: aiohttp.ClientResponse, i) -> None:
    print(f"req {i}:")
    print(resp.request_info, end="\n\n")
    print(f"resp {i}:")
    print(resp, end="\n\n")
    print(f"resp {i} headers:")
    print("headers count: ", len(resp.headers))
    print(resp.headers, end="\n\n")
    print(f"resp {i} cookies:")
    print(resp.cookies, end="\n\n")
    print(f"session cookies on req {i}:")
    for cookie in session.cookie_jar:
        print(cookie)
    print("\n")
    print(f"resp {i} content:")
    print(BeautifulSoup(await resp.text(), "html.parser").prettify(), end=f"\n{'.' * 20}\n\n")
    print('#' * 10, "\n\n")


if __name__ == "__main__":
    path = ["/ua/shutdowns", "/ua/ajax"][0]
    asyncio.run(request_site("https://www.dtek-kem.com.ua/ua/shutdowns"))
