#!/usr/bin/env python3.7
import click
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
# from setuptools import setup


@click.command()
@click.option('--count', default="hi", help='number of greetings')
@click.argument('name')
def main(count, name):
    website = "http://overapi.com/"
    dlpage = website+name
    content = urllib.request.urlopen(dlpage).read()
    soup = BeautifulSoup(content, 'lxml')
    title = soup.title.string
    a = soup.find_all("a", href=True)
    i = 1
    for value in a:
        if value['href'].endswith(".pdf"):
            p = re.compile('^(?!http://.*$).*')
            if p.match(value['href']):
                print("[ "+str(i)+" ] http://overapi.com"+value['href'])
                i+=1
            else:
                print("["+str(i)+"] "+ value['href'])
                i+=1
# TODO: user should can download the links 
# TODO: show all avalible cheetsheets
# TODO: add other sources - optional-
# TODO: convert pdf to text file - optional -

if __name__ == "__main__":
    main()
