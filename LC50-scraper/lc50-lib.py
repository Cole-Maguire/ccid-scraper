from bs4 import BeautifulSoup
import requests
import time
import re
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
class cas_class:
    def __init__(self,cas_in,):
        self.cas_no = cas_in.replace('\n','')
        self.test_arr = []
        self.get_tox(0)
        self.error_code = 0
        

    def get_tox(self,time_to_sleep):
        url_base = 'https://chem.nlm.nih.gov/chemidplus/rn/' + self.cas_no
        r = requests.get(url_base)
        data = r.text
        soup_base = BeautifulSoup(data, 'html.parser')

        print  (self.cas_no + ' - ' +str(r.status_code))
    #ERROR CHECKING
        if r.status_code == 200:
            pass
        elif r.status_code == 404:
            self.error_code = 404
            return
        else:
            if time_to_sleep > 30:
                self.error_code = r.status_code 
                return
            print ("WAITING FOR " + str(time_to_sleep) + " SECS - " +url_base)
            time.sleep(time_to_sleep)
            self.get_tox(time_to_sleep+10)
        if soup_base.find('div',text = "No results for Registry Number starts with") is not None:
               self.error_code = r.status_code
               print("Page not found")
               return
    #END ERROR CHECKING
        h1Text = soup_base.find('h1')
        h1Text = h1Text.contents[0].replace(u'\xa0', u' ')
        re_result = re.search(r'Substance Name:\s([\w\s\-\.]*)',h1Text)
        self.sub_name = re_result.group(1)
        print (self.sub_name)
        tox_table = soup_base.find('table',class_ = "prop")
        if tox_table is None: return
        if tox_table.parent.parent['id'] != 'toxicity': return
        tox_rows = tox_table.find_all('tr')
        
        for row in tox_rows:
            cols = row.find_all('td')
            if cols != []:
                self.test_arr.append(test_class(cols[0].get_text(),cols[1].get_text(),cols[2].get_text(),cols[3].get_text(),cols[4].get_text(),cols[5].get_text()))
    def print_all(self):
        for test in self.test_arr:
            print(test.return_test())
    def print_csv(self):
        str_out = ''
        for test in self.test_arr:
            str_out += self.cas_no + "|" + self.sub_name + "|" + test.return_test_csv() + "\n"
        return str_out
class test_class:
    def __init__(self,org_in,test_type_in,route_in,dose_in,effect_in,source_in):
        self.org = org_in
        self.test_type = test_type_in
        self.route = route_in
        self.dose = dose_in
        self.effect = effect_in
        self.source = source_in
    def return_test(self):
        return(self.org,self.test_type,self.dose)
    def return_test_csv(self):
        return self.org+'|'+self.test_type+'|'+self.route+'|'+self.dose+'|'+self.effect+'|'+self.source
    