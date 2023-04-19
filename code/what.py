import aiohttp
import asyncio
import aiofiles

url = "https://picsum.photos/v2/list"
base_url = 'from ENV'
alg='static'
asyncio.run(main())

async def main()-> None:
    links = []
    alg_for_discover_likns:baseAbstraction = getattr(object,alg)
    if not links:
        links = alg_for_discover_likns.discover(base_url)
    AsyncSingletoneDownloader.download(urls=links,method='post',auth='token;ldsflds;')
    ...