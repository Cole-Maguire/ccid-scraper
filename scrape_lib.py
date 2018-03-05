from bs4 import BeautifulSoup
import requests
import time
import re
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
class cas_class:
    def __init__(self,cas_in):
        self.cas_no = cas_in.replace('\n','')
        self.conc_urls = self.get_conc_urls()
        self.conc_objects = {}
        if self.cas_found == False:
            return
        for title in self.conc_urls.keys():
            self.conc_objects[title] = conc_class(self.conc_urls[title],title)
            time.sleep(0.25)

    def get_conc_urls(self):
        url_base = 'https://www.epa.govt.nz/database-search/chemical-classification-and-information-database-ccid/DatabaseSearchForm?SiteDatabaseSearchFilters=35&Keyword='+ self.cas_no +'&DatabaseType=CCID'
        r = requests.get(url_base,header)
        data = r.text
        soup_base = BeautifulSoup(data, 'html.parser')

        for f in soup_base.find_all('p'):
            if f.get_text() == "Sorry, your search query did not return any results.":
                self.cas_found = False
                return
            else:
                self.cas_found = True

        titles = soup_base.find_all('h5',class_='result__title')
        link_dict = {}
        for t in titles:
            link_dict[t.a["title"]] = 'https://www.epa.govt.nz/' + t.a["href"]
        return link_dict
    def return_pretty(self):
        str_out = self.cas_no + '\n'
        for i in self.conc_objects.keys():
            str_out += '\t' + i 
            str_out += '\t Name: ' + self.conc_objects[i].raw_name +'Lower: ' + str(self.conc_objects[i].lower_conc) +' Upper: ' + str(self.conc_objects[i].upper_conc)
            str_out += '\t' + self.conc_objects[i].return_all_haz() + '\n'
        return str_out
    def return_csv(self):
        str_out= ''
        for i in self.conc_objects.keys():
           for j in self.conc_objects[i].haz_dict.keys():
               str_out += self.cas_no + '|'+ self.conc_objects[i].raw_name + '|'
               str_out += str(self.conc_objects[i].lower_conc) + '|'+ str(self.conc_objects[i].upper_conc) + '|'+ str(self.conc_objects[i].haz_dict[j].class_num) + '|' + self.conc_objects[i].haz_dict[j].class_abc + '|'+ self.conc_objects[i].haz_dict[j].route + '|' + self.conc_objects[i].title +  '\n'
        
        return str_out
class conc_class:
    def __init__(self, url_in,title_in):
        self.page_url = url_in
        self.haz_dict = {}
        self.title = title_in.replace('≤','<').replace('≥','>')
        r = requests.get(self.page_url,header)
        data = r.text
        soup_conc = BeautifulSoup(data,'html.parser')
        hsno_classes = soup_conc.find_all('h5',class_='accordion__title')
        for h in hsno_classes:
            class_str = h.get_text().replace('\n','').replace('Plus','')
            if class_str.find("Classification") == 0:
                self.haz_dict[class_str] = haz_class(class_str,h.find_next('dd').get_text())
        self.parse_title()

    def parse_title(self):
        #This is probably clunky as hell, but I'm learnt regex an hour ago
        #and I'm aiming for readability here, mmmkay?
        reg = re.search(r'([\w\s,\-\[\]]*)([><][\d\s\-]*%)?(.*)',self.title.replace("(","").replace(")",""))
        if reg.group(2) is None:
            self.lower_conc, self.upper_conc = (0,100)
        else:
            self.parse_range(reg.group(2))
        self.solu_type = reg.group(3)
        if reg.group(1)[-2:] == ', ':
            self.raw_name = reg.group(1)[0:-2]
        else:
            self.raw_name = reg.group(1)

    def parse_range(self,range_in_str):
        reg_range = re.search(r'^[<>]? ?([\d\.]{1,4})[\s\-]*([\d\.]{1,4})?%$',range_in_str) #Damn do I hate regex
        if reg_range.group(2) is None:
            if range_in_str[0] == ">":
                self.lower_conc = reg_range.group(1)
                self.upper_conc = 100
            elif range_in_str[0] == "<":
                self.lower_conc = 0
                self.upper_conc = reg_range.group(1)
            else:
                self.lower_conc = "error:"
                self.upper_conc = "unknown range"
        else:
            self.lower_conc = reg_range.group(1)
            self.upper_conc = reg_range.group(2)

    def return_all_haz(self):
        str_out = ' '
        for i in self.haz_dict.keys():
            str_out += self.haz_dict[i].out_str() + ', '
        return str_out[:-2]


class haz_class:
        def __init__(self,full_name,route):
            reg_haz = re.search(r'Classification (\d\.\d\.?\d?)([A-F])', full_name)
            #self.full_name = full_name.replace('\n','').replace('Plus','')
            self.class_abc = reg_haz.group(2)
            self.class_num = reg_haz.group(1)
            self.route = route.replace('(','').replace(')','').replace('\n','')
        def __str__(self):
            return self.class_num  +self.class_abc
        def out_str(self):
            return self.class_num +self.class_abc
