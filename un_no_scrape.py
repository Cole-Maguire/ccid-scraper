from bs4 import BeautifulSoup
import requests
import re
print("INTIALISING")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

url_base = "https://adrdangerousgoods.com/eng/substances/all/"
print("REQUEST BOILERPLATE")
r = requests.get(url_base,header)
data = r.text
soup_base = BeautifulSoup(data, 'html.parser')

print("UN_Number|Proper Shipping Name|Packing Group|Class")
un_rows = soup_base.find_all("li",itemtype = "http://schema.org/ProductModel")
for row in un_rows:
    r_row = requests.get(row.find("a")["href"],header)
    soup_row = BeautifulSoup(r_row.text,'html.parser')
    
    print(soup_row.find("td",{"headers":"header_un"}).get_text()+"|"+soup_row.find("td",{"headers":"header_name"}).get_text()+"|"+soup_row.find("td",{"headers":"header_packing_group"}).get_text()+"|"+soup_row.find("td",{"headers":"header_class"}).get_text())