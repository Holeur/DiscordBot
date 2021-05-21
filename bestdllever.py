# -*- coding: utf-8 -*-
import selenium
from selenium.common.exceptions import NoSuchElementException

def deleten(line):
    return line[:len(line)-1]
    
def filereplace(filename,markname,search,resultstr): #
    flag1 = 0
    flag2 = 0
    with open(filename,'r',encoding='utf-8') as file:
        linenum = 0
        filemas = file.readlines()
        file.seek(0)    
        for line in file:
            linenum += 1
            if markname in line:
                flag1 = 1
            if flag1 and search in line:
                if '\n' in line:
                    flag2 = 1
                break
        filemas[linenum-1] = resultstr
        if flag2:
            filemas[linenum-1] += '\n'
    with open(filename,'w',encoding='utf-8') as file:
        for line in filemas:
            file.write(line)

def getip(browser,testbut):
    try:
        browser.find_element_by_xpath(testbut).click
    except NoSuchElementException:
        getip(browser,testbut)
