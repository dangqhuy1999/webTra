import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector

async def fetch(url, proxy):
    connector = ProxyConnector.from_url(proxy)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }
        
        try:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return f"Error: {response.status}"
        except Exception as e:
            return f"Request failed: {str(e)}"

async def main():
    url = "https://www.tratencongty.com/thanh-pho-ho-chi-minh/quan-thu-duc/phuong-linh-dong/"
    proxy = "socks4://47.119.22.92:8443"
    
    result = await fetch(url, proxy)
    print(result)

# Chạy chương trình
asyncio.run(main())