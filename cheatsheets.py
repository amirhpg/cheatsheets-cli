#!/usr/bin/env python3.7
import sys
import os.path
import click
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
# from setuptools import setup


@click.command()
@click.option('--link', default=1, help='which cheatsheet link to download')
@click.argument('name')
def main(link, name):
    website = "http://overapi.com/"
    dlpage = website+name
    content = urllib.request.urlopen(dlpage).read()
    soup = BeautifulSoup(content, 'lxml')
    title = soup.title.string
    a = soup.find_all("a", href=True)
    i = 1
    othercheatsheetsindicator = 0
    downloadcompleteindicator = 0
    for value in a:
        if value['href'].endswith(".pdf"):
            p = re.compile('^(?!http://.*$).*')
            if p.match(value['href']):
                fileurl = "http://overapi.com"+value['href']
                filename = value['href'].rsplit('/')[-1]
                if os.path.isfile(filename):
                    print(filename+" already exist! ☉")
                    i+=1
                else:
                    if i == link :
                         print("[ "+str(i)+" ] "+fileurl+" [Downloading] ⌛")
                         download(fileurl,filename)
                         if os.path.isfile(filename):
                             print("\nDownload completed successfully ✓")
                             downloadcompleteindicator+=1
                         else:
                            print("error ✗")

                         i+=1
                    else:
                        if downloadcompleteindicator != 0:
                            if othercheatsheetsindicator == 0:
                                print("\n")
                                print("+----------------------------------------------------+")
                                print("|            Other availble cheetsheets              |")
                                print("+----------------------------------------------------+")
                                othercheatsheetsindicator+=1;

                            print("[ "+str(i)+" ] "+fileurl)
                            
                        i+=1
            else:
                fileurl = value['href']
                filename = value['href'].rsplit('/')[-1]
                if os.path.isfile(filename):
                    print(filename+" already exist! ☉")
                    i+=1
                else:
                    if i == link :
                         print("[ "+str(i)+" ] "+fileurl+" [Downloading] ⌛")
                         download(fileurl,filename)
                         if os.path.isfile(filename):
                             print("\nDownload completed successfully ✓")
                             downloadcompleteindicator+=1
                         else:
                            print("error ✗")
                         i+=1
                    else:
                        if downloadcompleteindicator != 0:
                            if othercheatsheetsindicator == 0:
                                print("\n")
                                print("+----------------------------------------------------+")
                                print("|            Other availble cheetsheets              |")
                                print("+----------------------------------------------------+")
                                othercheatsheetsindicator+=1;

                            print("[ "+str(i)+" ] "+fileurl)
                        
                        i+=1



def download(url, filename):
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                sys.stdout.flush()
    sys.stdout.write('\n')


# TODO: user should can download the links 
# TODO: show all avalible cheetsheets
# TODO: add other sources - optional-
# TODO: convert pdf to text file - optional -

if __name__ == "__main__":
    main()
