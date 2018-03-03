from scrape_lib import cas_class
import time
import random

def main():
    #file_path = input("Enter the folder in which cas_no.txt resides: ")
    f_in = open('cas_no.txt','r')
    cas_array = f_in.readlines()
    f_in.close()
    print(cas_array)

    f_out = open('ccid_scraped_output.csv','w')
    f_out.write("cas-no,full-title,raw-name,lower-limit,upper-limit,class-num,class-abcd,class-route\n")
    for c in cas_array:
        temp_class = cas_class(c)
        print(temp_class.return_csv())
        f_out.write(temp_class.return_csv())
        time.sleep(random.random() * 3)
    f_out.close

    f_read = open('ccid_scraped_output.csv','r')
    print (f_read.readlines())
    f_read.close()
main()
