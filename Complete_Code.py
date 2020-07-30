
# coding: utf-8

# In[1]:

#from IPython import get_ipython
#Extraction of tags of four regions
from bs4 import BeautifulSoup
import requests
url1='http://dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=3&RegionName=Mumbai'
url2='http://dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=6&RegionName=Pune'
url3='http://dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=1&RegionName=Amravati'
url4='http://dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=2&RegionName=Aurangabad'
lst=[url1,url2,url3,url4]
link=[]
for urls in lst:
    
    html_content = requests.get(urls).text
    soup = BeautifulSoup(html_content, "lxml")
    t= soup.find("table", attrs={"class": "DataGrid"})
    #print(t.prettify())
    tags=t('a')
    for tag in tags:
        link.append(tag.get('href'))
links=list(filter(None,link))


# In[2]:

print(len(links))


# In[4]:

#Extraction of the required data from dtemaharashtra's website for four regions
region,name,address,officeno,personalno,emailid,website,dir_pri,reg,status,auto,mino=([] for i in range(12))
for link in links:
    b='http://www.dtemaharashtra.gov.in/'
    c=b+link
    html=requests.get(c).text
    soup = BeautifulSoup(html, "lxml")
    r=soup.find('span',attrs={"id":"ctl00_ContentPlaceHolder1_lblRegion"}).text
    region.append(r)
    n=soup.find('span',attrs={"id":"ctl00_ContentPlaceHolder1_lblInstituteNameEnglish"}).text
    name.append(n)
    add=soup.find('span',attrs={"id":"ctl00_ContentPlaceHolder1_lblAddressEnglish"}).text
    address.append(add)
    offno=soup.find('span',attrs={"id":"ctl00_ContentPlaceHolder1_lblOfficePhoneNo"}).text
    pos=offno.find('E')
    offno=offno[:pos]
    officeno.append(offno)
    perno=soup.find('span',attrs={"id":"ctl00_ContentPlaceHolder1_lblPersonalPhoneNo"}).text[:-7]
    pos1=perno.find('E')
    offno=perno[:pos1]
    personalno.append(perno)
    email=soup.find('span', attrs={"id":"ctl00_ContentPlaceHolder1_lblEMailAddress"}).text
    emailid.append(email)
    webadd=soup.find('span',attrs={"id":"ctl00_ContentPlaceHolder1_lblWebAddress"}).text
    website.append(webadd)
    dipi=soup.find('span',attrs={"id":"ctl00_ContentPlaceHolder1_lblPrincipalNameEnglish"}).text
    dir_pri.append(dipi)
    regname=soup.find('span', attrs={"id":"ctl00_ContentPlaceHolder1_lblRegistrarNameEnglish"}).text
    reg.append(regname)
    stat=soup.find('span',attrs={"id":"ctl00_ContentPlaceHolder1_lblStatus1"}).text
    status.append(stat)
    aut_stat=soup.find('span',attrs={"id":"ctl00_ContentPlaceHolder1_lblStatus2"}).text
    auto.append(aut_stat)
    min_stat=soup.find('span',attrs={"id":"ctl00_ContentPlaceHolder1_lblStatus3"}).text
    mino.append(min_stat)
print("data extracted")


# In[13]:


#get_ipython().run_cell_magic('HTML', '', '<style type="text/css">\n    table.dataframe td, table.dataframe th {\n        border-style: solid;\n    }\n</style>')


# In[14]:


import pandas as pd
import numpy as np
df=pd.DataFrame(list(zip(region,name,address,officeno,personalno,emailid,website,dir_pri,reg,status,auto,mino)), columns=["Region","College Name","Address","Office Number","Personal Number","Email-id","Website Link","Director/Principal Name","Registrar Name","Status","Autonomous Status","Minority Status"])
df = df.apply(lambda x: x.str.strip()).replace('', None)
df['Contact for placement/ TPO contact']=None
df['Email for placement/TPO email']=None



# In[19]:
#Scraping the phone numbers and email ids available on all the websites of all four regions

import requests
import re
for i in range(len(website)):
    a=website[i]
    b='https://' 
    url=b+a
    pdata=[]
    emails=[]
    if(region[i]=='Mumbai'):
        try:
            req = requests.get(url).text
            pdata=re.findall("[Phone:]?([(]?[0][2][2][)/s-]?\d{4}[/s-]?\d{4})",req)
            if(pdata==[]):
                pdata = re.findall("[Phone:]?([(]?[0][2][3][0-9][0-9][)/s-]?\d{3}[/s-]?\d{3})", req)
            if(pdata==[]):
                pdata = re.findall("[Phone:]?([(]?[0][2][5][0-9][0-9][)/s-]?\d{3}[/s-]?\d{3})", req)
            if(pdata==[]):
                pdata = re.findall("[Phone:]?([(]?[0][2][1][0-9][0-9][)/s-]?\d{3}[/s-]?\d{3})", req)
            if(pdata==[]):
                pdata = re.findall("\d{5} \d{5}", req)
            if(pdata==[]):
                pdata=re.findall("[PhoneM:(]?([+][9][1][/s-]?\d{10})",req)
            if(pdata==[]):
                pdata=re.findall("[7-9]{1}[0-9]{9}",req)
            if(pdata==[]):
                pdata=re.findall("\d{3} \d{8}", req)
                
            emails=re.findall("([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",req)
            
            if(url=='https://www.imcost.edu.in'):
                pdata=['022 25832452','25829318' ,' 25832466','9820816932','7045944373']
            if(url=='https://www.fcrims.com'):
                pdata=['022-27771000']
            if(url=='https://www.mpcoa.in'):
                pdata=['+9122 20847229', '+91 9819-595-861']
            if(url=='https://www.timscdrmumbai.in'):
                pdata=['022 - 2884 0484/91','022 - 67308301/02']
                emails=['timscdr@thakureducation.org']
            if(url=='https://www.sce.edu.in'):
                pdata=['(022) 27743703','27743704','27743705','27743706','27743707','27743708','9320299474']
                emails=['registrarsaraswati@gmail.com']
            pdata = list(dict.fromkeys(pdata))
            emails = list(dict.fromkeys(emails))
        except:
            pass
        
    elif(region[i]=='Pune'):
        try:
            req = requests.get(url).text
            pdata=re.findall("[Phone:(]?([0][2][3][0-9][0-9][)/s-]?\d{6})",req)
            if(pdata==[]):
                pdata = re.findall("[Phone:(]?([0][2][0][)/s-]?\d{4}[/s-]?\d{4})", req)
            if(pdata==[]):
                pdata = re.findall("[Phone:(]?([0][2][0][)/s-]?\d{4}[/s-]?\d{4}.\d{4})", req)
            if(pdata==[]):
                pdata=re.findall("[Phone:(]?([0][2][1][0-9][0-9][)/s-]?\d{6})",req)
            if(pdata==[]):
                pdata=re.findall("[PhoneM:(]?([+][9][1][/s-]?[0-9]{10})",req)
            if(pdata==[]):
                pdata=re.findall("\d{3} \d{8}", req)
            pdata = list(dict.fromkeys(pdata))
            emails=re.findall("([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",req)
            emails = list(dict.fromkeys(emails))
        except:
            pass
    elif(region[i]=='Amravati'):
        try:
            req = requests.get(url).text 
            pdata=re.findall("[Phone:]?([(]?[0][7][2][0-9][0-9][)\s-]?\d{6})",req)
            if (pdata==[]):
                pdata=re.findall("[Phone:]?([(]?{1}[0][7][0-9][0-9][)\s-]?\d{7})",req)
            if (pdata==[]):
                pdata=re.findall("[+][9][1].[0-9]{10}",req)
            pdata = list(dict.fromkeys(pdata))
            emails=re.findall("([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",req)
            emails = list(dict.fromkeys(emails))
        except:
            pass
    elif(region[i]=='Aurangabad'):
        try:
            req = requests.get(url).text 
            pdata=re.findall("[Phone:]?([(]?[0][2][4][0][)/s-]?\d{7})",req)
            if(pdata==[]):
                pdata=re.findall("[Phone:]?([(]?[0][2][4][0-9][0-9][)/s-]?\d{3}[/s-]?\d{3})",req)
            if (pdata==[]):
                pdata=re.findall("[Phone:]?([(]?[0][2][3][8][0-9][)/s-]?\d{3}[/s-]?\d{3})",req)
            if (pdata==[]):
                pdata=re.findall("[PhoneM:]?([(]?[+][9][1][)/s-]?\d{5}[/s-]?\d{5})",req)
            if(pdata==[]):
                pdata=re.findall("[Phone:]?([(]?[0][)/s-]?[7]\d{4}[/s-]?\d{5})",req)
            pdata = list(dict.fromkeys(pdata))
            emails=re.findall("([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",req)
            emails = list(dict.fromkeys(emails))
            if (url=='https://www.svspm.org'):
                pdata=[]
                emails=['svspmindia@gmail.com']
        except:
            pass
        
    df.loc[i,'Contact for placement/ TPO contact']=pdata
    df.loc[i,'Email for placement/TPO email']=emails
    
for i in range(len(website)):
    if df.loc[i,'Contact for placement/ TPO contact']==[]:
        df.loc[i,'Contact for placement/ TPO contact']=None
    if df.loc[i,'Email for placement/TPO email']==[]:
        df.loc[i,'Email for placement/TPO email']=None
print("Phone number and emails from websites extracted")


# In[128]:


print(df)


# In[120]:


x=list(df['Region'].unique())
a=[]
na=[]
t=[]
for r in x:
    count1=0
    count2=0
    for i in range (len(region)):
        if (df.loc[i,"Region"]==r):
            if(df.loc[i,"Autonomous Status"]=="Autonomous"):
                count1+=1
            else:
                count2+=1
    a.append(count1)
    na.append(count2)
for i in range(len(a)):
    t.append(a[i]+na[i])


# In[130]:

#Graphical representation of the data
#get_ipython().run_line_magic('matplotlib', 'notebook')
import matplotlib.pyplot as plt
index1=np.arange(len(x))
plt.figure()
bars=plt.bar(index1,a,width=0.5,align='center',linewidth=0,color='#1F77B4')
plt.xticks(index1,x)
plt.title('Number of Autonomous Colleges per Region', alpha=0.8)
plt.tick_params(top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=True)
for bar in bars:
    plt.gca().text(bar.get_x() + bar.get_width()/2, bar.get_height()-1, str(int(bar.get_height())), ha='center', color='w', fontsize=11)
plt.show()

plt.figure()
bars=plt.bar(index1,na,width=0.5,align='center',linewidth=0,color='#1F77B4')
plt.xticks(index1,x)
plt.title('Number of Non-Autonomous Colleges per Region', alpha=0.8)
plt.tick_params(top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=True)
for bar in bars:
    plt.gca().text(bar.get_x() + bar.get_width()/2, bar.get_height()-30, str(int(bar.get_height())), ha='center', color='w', fontsize=11)
plt.show()

plt.figure()
bars=plt.bar(index1,t,width=0.5,align='center',linewidth=0,color='#1F77B4')
plt.xticks(index1,x)
plt.title('Number of Colleges per Region', alpha=0.8)
plt.tick_params(top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=True)
for bar in bars:
    plt.gca().text(bar.get_x() + bar.get_width()/2, bar.get_height()-30, str(int(bar.get_height())), ha='center', color='w', fontsize=11)
plt.show()


# In[129]:

#converting the dataframe to .csv which is added in the folder "Codes"
df.to_csv("College_Information.csv")

