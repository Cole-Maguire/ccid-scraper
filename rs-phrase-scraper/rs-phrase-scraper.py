from scrape_lib import Cas_class
def main():
    
    f_in = open('combined_cas.txt','r')
    cas_array = f_in.readlines()
    f_in.close()
    unique_cas = {}
    f_out = open('rs_scraped_output.txt','w')

    for c in cas_array:
        if c not in unique_cas:
            print(c)
            unique_cas[c] = Cas_class(c)
            print(unique_cas[c].return_header())
            print(unique_cas[c].return_csv())
    f_out.close()
main()