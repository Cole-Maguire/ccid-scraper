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
        for title in self.conc_urls.keys():
            self.conc_objects[title] = conc_class(self.conc_urls[title],title)
            time.sleep(0.25)

    def get_conc_urls(self):
        url_base = 'https://www.epa.govt.nz/database-search/chemical-classification-and-information-database-ccid/DatabaseSearchForm?SiteDatabaseSearchFilters=35&Keyword='+ self.cas_no +'&DatabaseType=CCID'
        r = requests.get(url_base,header)
        data = r.text
        soup_base = BeautifulSoup(data, 'html.parser')

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
               str_out += self.cas_no + ',' + self.conc_objects[i].raw_name + ',' 
               str_out += str(self.conc_objects[i].lower_conc) + ',' + str(self.conc_objects[i].upper_conc) + ',' + str(self.conc_objects[i].haz_dict[j].class_num) + ','  + self.conc_objects[i].haz_dict[j].class_abc + ',' + self.conc_objects[i].haz_dict[j].route + '\n'
        
        return str_out
class conc_class:
    def __init__(self, url_in,title_in):
        self.page_url = url_in
        self.haz_dict = {}
        self.title = title_in
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
        reg = re.search(r'([\w\s,]*)([><][\d\s-]*%)?(.*)',self.title)
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
        reg_range = re.search(r'^[<>]?([\d\.]{1,3})[\s\-]*([\d\.]{1,3})?%$',range_in_str) #Damn do I hate regex
        self.lower_conc  = reg_range.group(1) if reg_range.group(1) is not None else 0
        self.upper_conc  = reg_range.group(2) if reg_range.group(2) is not None else 100

    def parse_title_OLD(self):
        #Kept around until regex is working 100%
        str_shrink = self.title.replace(" ", '')
        comma_coord =str_shrink.find(",")
        percent_coord = str_shrink.find("%")
        dash_coord = str_shrink.find("-")
        less_coord = str_shrink.find("<")
        great_coord = str_shrink.find(">")

        if percent_coord == -1 and comma_coord == -1:
            upper = 100
            lower = 0
        elif dash_coord == -1:
            if less_coord >= 0:
                lower = 0
                upper = str_shrink[less_coord+1:percent_coord]
            elif great_coord >= 0:
                lower = str_shrink[great_coord+1:percent_coord]
                upper = 100
            else:
                lower = "What unholy sorcery"
                upper = " is this?"
        else:
            lower = str_shrink[comma_coord+1:dash_coord]
            upper = str_shrink[dash_coord+1:percent_coord]

        (self.lower_conc, self.upper_conc) = lower, upper
        if comma_coord == -1:
            self.raw_name = self.title
            self.solu_type = 'n/a'
        else:
            self.raw_name = self.title[:self.title.find(',')]
            self.solu_type = self.title[self.title.find('%'):]

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
