from bs4 import BeautifulSoup
import requests
import re
import time



def ClassdataMaker(classlink):

    #get webpage
    page = requests.get(classlink)
    #put into beautiful soup
    soup = bs4.BeautifulSoup(page.content)
    ClassData = ClassExtractor(soup)
    return ClassData

def ClassExtractor(soup):
    
    Classname = soup.find('h1', attrs={'class': 'api-title'}).text
    print(Classname)
    table1 = TableExtractor(soup , "pubmethods")
    table2 = TableExtractor(soup , "promethods")
    pub_methods=[] 
    pro_methods=[] 
    if(table1!="empty"):
        pub_methods = ClassInsiderExtractor(table1)
    if(table2!="empty") :
        pro_methods = ClassInsiderExtractor(table2)
    ClassData = [Classname , pub_methods , []]
    return ClassData
    
    
    
    
    
def TableExtractor(soup , id1) :
    table = soup.find('table', attrs={'id': id1})
    if(table != None):
        children = table.findChildren()
        codearr = []
        for child in children :
            if (child.name=="td") :
                codearr.append(child)
        return codearr
    else : 
        return "empty"


def ClassInsiderExtractor(codearr) :
    Classarray= []
    for i in range(0,len(codearr),2) :
        
       # The methods
        children = codearr[i+1].findChildren()
        for  child in children :
            if(child.name=="code"):
                name = child.text
                name = re.sub(r"\s+", "", name, flags=re.UNICODE)
                break
                
        # ReturnType
        returntype = codearr[i].text
        returntype = re.sub(r"\s+", "", returntype, flags=re.UNICODE)
        method= [returntype , name]
        Classarray.append(method)  
        
    return Classarray


start = time.time()
classdata = ClassdataMaker("https://developer.android.com/reference/android/widget/AbsListView.html")
stop = time.time()
tt = stop-start
print(tt)
