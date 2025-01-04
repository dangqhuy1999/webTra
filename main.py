from lxml import etree
import aiohttp
import asyncio
from lxml import html
import dbConnect
import json 
import time
from PIL import Image
import pytesseract
import io
import base64
import traceback
import random
import openpyxl

# Tạo một workbook mới
workbook = openpyxl.Workbook()

# Chọn sheet hiện tại
sheet = workbook.active

# Đặt tiêu đề cho các cột (nếu cần)
sheet.append(["Tên Công Ty", "Địa Chỉ", "Số Điện Thoại", "Đại Diện Pháp Luật", "Ngày Cấp Giấy Phép", "Link", "NumPage"])


def is_numeric_string(s, allowed_chars='0123456789'):
    # Loại bỏ các ký tự trắng
    stripped = s.strip()
    
    # Thêm các ký tự cho phép vào danh sách
    allowed_chars += '\n\t '
    
    # Kiểm tra nếu chuỗi chỉ chứa số và các ký tự cho phép
    for char in stripped:
        if char not in allowed_chars:
            return False
            
    return True 
values = [0.7, 1, 1.3, 1.6, 1.9,2.5]
async def xulyData(data):
    daidienpl = None
    ngaycapgp = None
    ngayhd = None
    if "Đại diện pháp luật" in data:
        if "Ngày cấp giấy phép:" in data:
          daidienpl = data.split("Ngày cấp giấy phép:")[0].split(':')[1].strip()
          data = data.split("Ngày cấp giấy phép:")[1]
          if "Ngày hoạt động:" in data:
            ngaycapgp = data.split("Ngày hoạt động:")[0].strip()
            data = data.split("Ngày hoạt động:")[1]
            if "Điện thoại trụ sở:" in data:
              ngayhd = data.split("Điện thoại trụ sở:")[0].strip()
              data = data.split("Điện thoại trụ sở:")[1]
            if "Trạng thái:" in data:
              ngayhd = data.split("Trạng thái:")[0].strip()
              data = data.split("Trạng thái:")[1]
    else:
        daidienpl="NoName"
        if "Ngày cấp giấy phép:" in data:
          
          if "Ngày hoạt động:" in data:
            ngaycapgp = data.split("Ngày hoạt động:")[0].strip()
            data = data.split("Ngày hoạt động:")[1]
            if "Điện thoại trụ sở:" in data:
              ngayhd = data.split("Điện thoại trụ sở:")[0].strip()
              data = data.split("Điện thoại trụ sở:")[1]
            if "Trạng thái:" in data:
              ngayhd = data.split("Trạng thái:")[0].strip()
              data = data.split("Trạng thái:")[1]    
    return daidienpl, ngaycapgp, ngayhd

async def image_to_text(base64_data):
  # Đường dẫn đến tệp thực thi Tesseract
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  # Tách chuỗi base64 để lấy phần dữ liệu
  base64_str = base64_data.split(",")[1]

  # Chuyển đổi từ base64 sang hình ảnh
  image_data = base64.b64decode(base64_str)
  image = Image.open(io.BytesIO(image_data))
  
  custom_config = r'--psm 6'
  # Nhận diện văn bản
  #custom_config = r'--psm 7 -c tessedit_char_whitelist=0123456789'  # Thay đổi psm theo nhu cầu của bạn
  text = pytesseract.image_to_string(image,config=custom_config)

  return text

# db link cty, dia chi, sdt nguoi dai dien, ngay thanh lap.

# cache khong lap lai link

#cautruc tu Province/City

db = dbConnect.Database('localhost', 'huyne', 'Aa@12345', 'web2')  # Thay thế thông tin kết nối

columns = ['detail', 'description', 'yturn']

#values = ['Detail example', 'Description example', 10]

#db.insert('infop', columns, values)
#db.close()


async def fetch(session, url):
    '''
    headers = {
    "Host": "googleads.g.doubleclick.net",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Referer": "https://tratencongty.com/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "iframe",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Priority": "u=6"
    }
    '''
    async with session.get(url) as response:
        return await response.text()  # Hoặc response.json() nếu bạn mong đợi JSON

async def fetch_province_url(base_url):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session,base_url)
        content = html.fromstring(response)
        provinces  = content.xpath("//a[@class='list-group-item']")
        mapVN = []
        for province in provinces:
          proLink = province.get('href')
          proText = province.text_content()
          print(proLink)
          print(proText)
          mapVN.append({proText: proLink})

        with open('mapVN.json', 'w', encoding='utf-8' ) as file:
          json.dump(mapVN,file,ensure_ascii=False, indent=4)

async def fetch_hcm(url):
    async with aiohttp.ClientSession() as session:
      response = await fetch(session,url)
      content = html.fromstring(response)
      provinces = content.xpath("//a[@class='list-group-item']")
      mapHCM = []
      for province in provinces:
        proLink = province.get('href')
        proText = province.text_content()
        print(proLink)
        print(proText)
        mapHCM.append({proText: proLink})
      
      with open('mapVN.json', 'r', encoding='utf-8') as file:
        mapVN = json.load(file)
      for item in mapVN:
          if "Thành phố Hồ Chí Minh" in item:
            currentValue = item["Thành phố Hồ Chí Minh"]
            item["Thành phố Hồ Chí Minh"] = [
    currentValue,
    mapHCM
    ]

      with open('mapVN.json', 'w', encoding='utf-8') as file:
        json.dump(mapVN, file, ensure_ascii=False, indent=4)

async def fetch_xa(url):
    async with aiohttp.ClientSession() as session:
      response = await fetch(session,url)
      content = html.fromstring(response)
      provinces = content.xpath("//a[@class='list-group-item']")
      mapTD = []
      for province in provinces:
        proLink = province.get('href')
        proText = province.text_content()
        print(proLink)
        print(proText)
        mapTD.append({proText: proLink})
      with open('mapVN.json' , 'r', encoding='utf-8') as file:
          mapVN = json.load(file)
      for item in mapVN:
          if "Thành phố Hồ Chí Minh" in item:
            quan = item["Thành phố Hồ Chí Minh"][1]
            for item2 in quan:
                if "Quận Thủ Đức" in item2:
                    linkTD = item2["Quận Thủ Đức"]
                    item2["Quận Thủ Đức"] = [
        linkTD,
        mapTD
        ]
      with open('mapVN.json' , 'w', encoding='utf-8') as file:
          json.dump(mapVN, file, ensure_ascii=False, indent=4)
            

async def fetch_urls(base_url, start, end):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(start, end + 1):
            url = f"{base_url}?page={page}"
            tasks.append(fetch(session, url))
        
        # Chạy tất cả các tác vụ
        responses = await asyncio.gather(*tasks)
        return responses
async def getInfo(url,province,district):
  async with aiohttp.ClientSession() as session:
    with open('mapVN.json', 'r', encoding='utf-8') as file:
      mapVN = json.load(file)
    for item in mapVN:
      if "Thành phố Hồ Chí Minh" in item:
        quan = item["Thành phố Hồ Chí Minh"][1]
        for item2 in quan:
          if "Quận Thủ Đức" in item2:
            xa = item2["Quận Thủ Đức"][1]
            if xa:
              for item3 in xa:
                pageNum = 1
                gut = 0
                slTD = 0
                while True:
                  try:
                    for key,value in item3.items():
                     print(str(key).strip())
                     print(str(value).strip())
                     url = str(value).strip() + f"?page={pageNum}"
                     print(url)
                     
                     response = await fetch(session,url)
                     content = html.fromstring(response)
                     

                     ctyLinkp = content.xpath("//div[@class='search-results']/a")
                     print(len(ctyLinkp))
                     for ctyLink in ctyLinkp:
                         url2 = ctyLink.get('href')
                         laplai = 1
                         while True:
                           laplai+=1
                           response2 = await fetch(session,url2)
                           content2 = html.fromstring(response2)
                           infoCTYpp = content2.xpath("//div[@class='jumbotron']")
                           sendContinue =0
                           if infoCTYpp[0] or laplai >5:
                             infoCTYp = infoCTYpp[0]
                             break
                           elif laplai > 6:
                               sendContinue = 1
                               break
                           else:
                             time.sleep(3)
                           if sendContinue ==1:
                             continue                               
                         outer_html = etree.tostring(infoCTYp, pretty_print=True, encoding='unicode')
                         #print(outer_html)
                         imgp = html.fromstring(outer_html)
                         sdt = "Non"
                         try:
                           base64_datap = imgp.xpath('(//img)[2]')
                           base64_data = base64_datap[0].get('src')
                           sdt = await image_to_text(base64_data)
                         except Exception as e:
                            pass
                         infoCTY = infoCTYp.text_content()
                         print(f'Info: \n{infoCTY}')
                         lines = infoCTY.splitlines()
                         tenCTY = lines[1].strip()
                         diachiCTY = lines[4].split(":")[1].strip()
                         data5 = lines[5].strip()
                         daidienpl, ngaycapgp, ngayhd = await xulyData(data5)
                         
                         print(f"{tenCTY}\n{diachiCTY}\n{sdt.strip()}\n{daidienpl}\n{ngaycapgp}\n")
                         time.sleep(random.choice(values))
                         if sdt is not None and is_numeric_string(sdt) == True:
                            # Ghi dữ liệu vào sheet
                            sheet.append([tenCTY, diachiCTY, sdt, daidienpl, ngaycapgp, url2,pageNum ])

                            # Lưu tệp Excel
                            workbook.save("thuduc.xlsx")
                         #with open('ctyInfo.txt', 'a' , encoding='utf-8') as file:
                         #    file.write(infoCTY)
                         #n=input('newcty_\n')
                         #time.sleep(0.5)
                     
                     slTD += len(ctyLinkp)

                     print(f'Len: {slTD}')
                     linkPaging1 = content.xpath("//ul[@class='pagination']/li")
                     print(len(linkPaging1))
                     lenLi = len(linkPaging1)
                     print(linkPaging1[lenLi-1].text_content())
                     pageLi = linkPaging1[lenLi-1].text_content()
                     pageNumstr = str(pageNum)
                     print(pageNumstr)
                     if pageNumstr == pageLi:
                         gut=1
                     #if linkPaging[0].text_content() == lenLi:
                     #    gut=1
                     #n=input(f'sss: {gut}')
                     
                     #for i in ctyLinkp:
                     #    linkCTY = i.get('href')
                     #    response = await fetch(session,linkCTY)
                    pageNum+=1
                    if gut == 1:
                      print("gutchop!!")

                      break
                  except Exception as e:
                    print(str(traceback.print_exc()))
                    n=input('Fail e!!!')
                    break
async def main():
    #base_url = "https://www.tratencongty.com" 
    #base_url = "https://www.tratencongty.com/thanh-pho-ho-chi-minh/"  # Thay đổi thành URL gốc của bạn
    base_url = "https://www.tratencongty.com/thanh-pho-ho-chi-minh/quan-thu-duc/" 
    #await fetch_province_url(base_url) 
    #await fetch_hcm(base_url)
    #await fetch_xa(base_url)
    await getInfo("", "","")
    page = '?page='
    

    n=input('_Test')
    '''
    responses = await fetch_urls(base_url, start_page, end_page)
    
    # In ra một số phản hồi
    for i, response in enumerate(responses):
        print(f"Response for page {i + 1}: {response[:100]}")  # In ra 100 ký tự đầu tiên
    '''
# Chạy chương trình
asyncio.run(main())
