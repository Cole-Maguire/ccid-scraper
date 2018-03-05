from scrape_lib import cas_class
import time
import random

def main():
    #file_path = input("Enter the folder in which cas_no.txt resides: ")
    f_in = open('cas_no4.txt','r')
    cas_array = f_in.readlines()
    cas_size = len(cas_array)
    i = 0
    f_in.close()
    unique_cas = {}

    f_out = open('ccid_scraped_output.txt','w')
    f_out.write("cas-no|full-title|raw-name|lower-limit|upper-limit|class-num|class-abcd|class-route|title\n")
    for c in cas_array:
        print("-------------------")
        i+=1
        print(str(i)+"/"+str(cas_size)+' - '+str(i/cas_size*100) + '%')
        if c not in unique_cas:
            temp_class = cas_class(c)
            print( c + ' CAS_Found: ' + str(temp_class.cas_found))
            
            if temp_class.cas_found:
                print(temp_class.return_csv())
                f_out.write(temp_class.return_csv())
                time.sleep(1 + random.random() * 5)
                unique_cas[c] = True

                
        else:
            print("Duplicate of :" + c)
        if len(unique_cas) % 10 == 0:
            print("WAITING FOR 15 SECONDS")
            time.sleep(15)
    f_out.close
    print("DONE")
main()
