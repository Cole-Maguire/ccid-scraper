import mechanicalsoup
import re

class Cas_class:
    browser = mechanicalsoup.StatefulBrowser()

    def __init__(self, cas_in):
        self.r_s_statements = {}
        self.chem_name = ''
        self. cas_no = ''

        self.status_code = self.browser.open('http://chemsub.online.fr/').status_code
        self.browser.select_form('form[id=FormChemsearch01]')
        self.browser['what'] = "regnum"
        self.browser['which'] = cas_in

        self.browser.submit_selected()
        page = self.browser.get_current_page()
        chem_name = page.find('span',class_='S18px fat subst_name')
        if chem_name is not None:
            self.chem_name = chem_name.get_text()
        else:
            self.chem_name = "CAS Number not found "
            return
        self.cas_no = cas_in
        self.get_risk_phrases(page)
        self.get_safety_phrases(page)

    def return_header(self):
        return '-'*16 + '\n' + self.cas_no +' - ' + self.chem_name + str(self.status_code)
    def return_csv(self):
        str_out = ''
        for i in self.r_s_statements.keys():
            str_out += self.cas_no +'|' + self.chem_name +'|'+ i +'|' + self.r_s_statements[i] + '\n'
        return str_out
    def get_risk_phrases(self, page):
        risk_phrases =page.find('td',text='Risk Phrases')
        if risk_phrases is not None:
            for i in risk_phrases.find_next_siblings('td'):
                for j in i.find_all('a',class_='normal'):
                        reg = re.search(r'(R[\d\/]*)\s*:\s*([\w\s]*)',j.get_text().replace(u'\xa0', ' '))
                        if reg is not None:
                            self.r_s_statements[reg.group(1)] = reg.group(2)
    def get_safety_phrases(self, page):
        safety_phrases =page.find('td',text='Safety Phrases')
        if safety_phrases is not None:
            for i in safety_phrases.find_next_siblings('td'):
                for j in i.find_all('a',class_='normal'):
                        reg = re.search(r'(S[\d\/]*)\s*:\s*([\w\s]*)',j.get_text().replace(u'\xa0', ' '))
                        if reg is not None:
                            self.r_s_statements[reg.group(1)] = reg.group(2)