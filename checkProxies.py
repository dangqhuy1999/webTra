import aiohttp
import asyncio

async def check_proxy(proxy):
    url = "http://httpbin.org/ip"  # URL để kiểm tra proxy
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, proxy=proxy, timeout=5) as response:
                if response.status == 200:
                    #with  open ('proxiesWorking.txt' ,'a', encoding='utf-8') as file:
                      #file.write(f"{proxy}\n")
                    return f"{proxy} is working"
                else:
                    return f"{proxy} returned status {response.status}"
    except Exception as e:
        return f"{proxy} failed: {str(e)}"

async def main():
    # Đọc danh sách proxy từ file
    with open('Free_Proxy_List.txt', 'r') as file:
        proxies = [line.strip() for line in file.readlines()]

    tasks = [check_proxy(proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)

# Chạy chương trình
asyncio.run(main())