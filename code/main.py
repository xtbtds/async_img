import aiohttp
import asyncio
import aiofiles
from time import sleep, time
from typing import Optional, Type, Iterable, List
from types import TracebackType
from aiohttp.client_exceptions import ClientConnectorError, InvalidURL
from bs4 import BeautifulSoup
from aiohttp import web



class AsyncSingletoneDownloader:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._session = aiohttp.ClientSession()
        return cls._instance
    
    def __init__(self):
        self.list_of_htmls = []
        self.html_errors = []
        self.links = []
    
    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._session.close()

    async def shluha_htmls(self, shluha, photo):
        async with self._session.get(f"https://faponic.com/{shluha}/{photo}/", allow_redirects=False) as response:
            if response.status == 200:
                print(photo)
                html_page = await response.text()
                self.list_of_htmls.append(html_page)
            else:
                self.html_errors.append(response)

    def parse_html(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")
        div = soup.find("div", "ui-block features-video")
        img = div.findChildren("img")
        link_to_image = img[0]['src']
        return link_to_image

    async def get_content_from_link(self, link):
        # sleep(0.1)
        # print(f"Photo {link} is being downloaded")
        async with self._session.get(link) as response:
            bytes_image = await response.read()
            photo = link.split('/')[-1]
            await self.write_to_disk(bytes_image, photo)
    
    async def write_to_disk(self, data, photo):
        filename = f'dir/{photo}'
        async with aiofiles.open(filename, 'wb') as file:
            await file.write(data)






async def main():
    async with AsyncSingletoneDownloader() as client_session:

        # 1. Get all htmls Asynchronously
        tasks = []
        for i in range(720):
            task = asyncio.create_task(client_session.shluha_htmls(shluha="donna-loli", photo=i))
            tasks.append(task)
        await asyncio.gather(*tasks)

        print(len(client_session.html_errors))
        print(len(client_session.list_of_htmls))

        # 2. Parse all htmls Synchronously
        print("Parsing started")
        for i in client_session.list_of_htmls:
            link = client_session.parse_html(i)
            client_session.links.append(link)
        print("Parsing finished")
        print(f"There are {len(client_session.links)} links")

        # 3. Download all photos Asynchronously
        tasks = []
        for link in client_session.links:
            task = asyncio.create_task(client_session.get_content_from_link(link))
            tasks.append(task)
        await asyncio.gather(*tasks)



t0 = time()
asyncio.run(main())
print("TIME ASYNC: ", time() - t0)