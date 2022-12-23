import asyncio
import aiohttp
from aiohttp import ClientSession

from yarl import URL
from bs4 import BeautifulSoup

import codecs

urls = ["https://www.dtek-kem.com.ua/ua/shutdowns",
        "http://httpbin.org/get",
        "http://httpbin.org/headers"]


async def request_site(url: str):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en,ru;q=0.9,uk;q=0.8,en-US;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    }
    async with ClientSession() as session:
        session.cookie_jar.update_cookies(
            {
                "incap_ses_1104_2224657": "DVpBMoNU0h29iMP37jJSDzMNnmMAAAAABzwNXRJu4Zxq4zUx+P9r0w==",
                "incap_ses_7228_2224657": "ebbhdQ/JmySsXBPAQgRPZKv2nmMAAAAAqjR1Lxg1imuqS9YYV+i/dw==",
                "nlbi_2224657": "Qmm6TLtUpBs7aJ3i8ri73wAAAADO//I5BJOabhu1Zs+FHsot",
                "nlbi_2224657_2147483392": "qTpvXX/T4zvJhEwz8ri73wAAAAC4YgxeW6CWS1ANyKJ7SDrn",
                "visid_incap_2224657": "EjV70lEZRneN7HJIljbnFkQLnmMAAAAAQUIPAAAAAABAwOiAB/JzxvV8xCtKcLqV",

            },
            URL(url))
        await request(session, url, headers, 0)


async def request(session: ClientSession, url: str, headers: {}, i) -> aiohttp.ClientResponse:
    print(f"req {i} cookies:")
    print(session.cookie_jar.filter_cookies(URL(url)), end="\n\n")
    resp = await session.get(url, headers=headers)
    print(f"req {i}:")
    print(resp.request_info, end="\n\n")
    print(f"resp {i}:")
    print(resp, end="\n\n")
    print(f"resp {i} status:")
    print(resp.status, end="\n\n")
    print(f"resp {i} headers:")
    print("headers count: ", len(resp.headers))
    print(resp.headers, end="\n\n")
    print(f"resp {i} cookies:")
    print(resp.cookies, end="\n\n")
    print(f"session cookies on req {i}:")
    print(session.cookie_jar.filter_cookies(URL(url)), end="\n\n")

    with open(f"resp_{i}_text.txt", "w", encoding="utf-8") as file:
        text = BeautifulSoup(await resp.text(), "html.parser").prettify()
        # text = text.encode("utf-8").decode("unicode-escape")
        file.writelines(text)
        print(f"resp {i} text:")
        print(text)

    print('#' * 10, "\n\n")
    return resp


if __name__ == "__main__":
    asyncio.run(request_site(urls[0]))
