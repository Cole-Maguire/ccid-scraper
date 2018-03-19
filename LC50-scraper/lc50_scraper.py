from lc50-lib import cas_class
import time
import random

def main():
    f_in = open('combined_cas.txt','r')
    cas_array = f_in.readlines()
    f_in.close()
    unique_cas = {}
    cas_error = {}
    f_out = open('tox_scraped_output.txt','w')

    for c in cas_array:
        print("---------------------------")
        if not c in unique_cas:
            temp_class = cas_class(c)
            if temp_class.error_code == 0:
                unique_cas[c] = temp_class
                print(unique_cas[c].print_all())
                f_out.write(unique_cas[c].print_csv())
            else:
                cas_error[c] = temp_class
                print(c + "Failed with code - " +str( temp_class.error_code))
    print("Failed cas_numbers")
    for c in cas_error.keys():
        print(c)

    f_out.close()
main()
print('done')
