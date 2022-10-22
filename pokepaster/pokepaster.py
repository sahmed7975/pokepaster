import urllib.request
from bs4 import BeautifulSoup as bs
import re
import os


# input stuff
form = input('Enter format/tier: ')
openfile = input('Enter directory + file name with extension: ') 
readfile = open(openfile, encoding="utf8")
urllist = list()

for line in readfile:
    urls = re.findall('https:\/\/pokepast\.es\/[a-z0-9]{16}',line)
    for link in urls:
        urllist.append(link)

print(str(len(urllist)) + ' URLs found.')

writename = os.getcwd() + "\\importables\\import" + "_" + form + "_" + ".txt"
os.makedirs(os.path.dirname(writename),exist_ok=True)
with open(writename, 'w',encoding='utf-8') as writefile:

    # each URL
    filecount = 0
    for line in urllist: 
        filecount = filecount + 1

        # remove html
        html = urllib.request.urlopen(line)
        soup = bs(html, "html.parser")
        text = soup.get_text() 
    
        splittext = text.splitlines()
    
        # remove items on webpage that aren't part of the paste
        online = 0 
        for sub_line in splittext:
            if sub_line.startswith('Columns Mode'):
                del splittext[online-4:online+6]
            online = online+1
    
        # remove beginning and ending items, including paste titles
        del splittext[1:5] 
        del splittext[len(splittext)-4:len(splittext)+2]

        # remove beginning and ending items
        beginning = 0 
        while beginning == 0:
            if len(splittext[0])==0:
                del splittext[0]
            elif len(splittext[len(splittext)-1])==0:
                del splittext[len(splittext)-1]
        
            else:
                beginning = 1
    
        # remove extra lines between mons
        counter = 0 
        while counter < len(splittext):
            if len(splittext[counter])==0 and len(splittext[counter+1])==0:

                del splittext[counter]
                counter = counter - 1
            
            counter = counter + 1
    
        # add team separation at beginning and space separation at end
        splittext.insert(0,'')
        splittext.insert(0,'=== [' + form + '] Team ' +str(filecount) + ' ===')
        splittext.append('')
        splittext.append('')

        # write to file
        for lines in splittext:
            print(lines)
            writefile.write(lines + '\n')
