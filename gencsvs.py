# python gencsvs.py 
# run from CMD with anaconda prompt
import pandas as pd
#
def g1():
    df = pd.read_excel('covmenu.xlsx', sheet_name='Hoja1')
    #
    df.to_csv(r'covmenu1.csv', index = False, header=True)
    print("g1")

def g2():
    df = pd.read_excel('covmenu.xlsx', sheet_name='Hoja2')
    #
    df.to_csv(r'covmenu2.csv', index = False, header=True)    
    print("g1")
# - - - - - - - - - - - - - - - - - - - - - 
#
print("ini")
g1()
#  
g2()   
#
print("fin")