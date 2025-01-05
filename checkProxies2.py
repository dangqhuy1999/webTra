import requests

# Đọc danh sách proxy từ tệp
with open('Free_Proxy_List.txt', 'r', encoding='utf-8') as file:
    proxies = file.readlines()

# Chuyển đổi danh sách proxy thành định dạng (IP, port)
proxy_list = [line.strip() for line in proxies if line.strip()]

# Gửi yêu cầu đến localhost qua từng proxy
for proxy in proxy_list:
    ip = proxy.split(',')[0].strip('"')
    port = proxy.split(',')[7].strip('"')
    protocol = proxy.split(',')[8].strip('"')
    proxy_dict = {
        "http": f"{protocol}://{ip}:{port}",
        "https": f"{protocol}://{ip}:{port}",
    }
    
    try:
        response = requests.get("http://localhost/ip", proxies=proxy_dict, timeout=5)
        print(f"Proxy {proxy} is working: {response.json()}")
    except Exception as e:
        print(f"Proxy {proxy} failed: {e}")
