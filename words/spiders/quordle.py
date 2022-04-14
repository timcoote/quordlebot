import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from candidates import candidates
from enum import Enum, auto
from collections import defaultdict

import logging
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
from urllib3.connectionpool import log as urllibLogger
from protego import logger as protegoLogger

urllibLogger.setLevel(logging.WARNING)
seleniumLogger.setLevel(logging.WARNING)
protegoLogger.setLevel(logging.WARNING)

class works(Enum):
    FAILS = auto()
    WORKS = auto()
    UNTRIED = auto()

def enter_word (word):
    pass

class QuordleSpider (scrapy.Spider):
    name="quordle"

    def process_key (self, key, game):
        #print (key)
        if key in ['Enter Key', 'Backspace Key']:
            return works.FAILS, ''

        if 'Not guessed' in key:
            return works.UNTRIED, key[1]
        elif 'Incorrect in all game boards' in key:
            return works.FAILS, key[1]
        elif f"Incorrect in game board {game}" in key:
            return works.FAILS, key[1]
        else:
            return works.WORKS, key[1]

    def process_kb (self, keyboard, board):
        #breakpoint()
        for i in range(1,5):  #timing of moving between boards isn't right. 
            must=''
            maybe=''
            for key in keyboard.css('button'):
                #for ok, ch in [self.process_key (key.attrib['aria-label'], i) for i in range(1,5)]:
                ok, ch = self.process_key (key.attrib['aria-label'], i)
                if ok == works.WORKS:
                    must += ch
                elif ok == works.UNTRIED:
                    maybe += ch

                #print (i, ok, ch)
            print (i, must, maybe)
            if (len (must) > 0) and (len (maybe) <= 11):
                are, are_not = self.process_board (board)
                if len (are) >= 5: continue # guessed this word (not quite: succeeds if they're not all in the same guess!)
                #print (i, options := candidates(must, maybe, are, are_not))
                options = candidates(must, maybe, sure_y=are, sure_n=are_not)
                print (f"i is {i}", are, are_not, must, maybe, options)
                #if i == 1:
                #    are, are_not = self.process_board (board)
                #    print ("i is one", are, are_not, must, maybe, i, options, candidates (must, maybe, sure_y=are, sure_n=are_not))
                if 0 < len (options) <= 2:
                    self.send_str (options[0])
                    sleep (1)
                    return True
        return False

    def process_board (self, board):
        here = defaultdict(str)
        not_here = defaultdict(str)
        for row in board.css('div'):
            loc = 1
            for cell in [i.attrib['aria-label'] for i in row.xpath('.//div/div') if 'aria-label' in i.attrib.keys()]:
                #print ("proc board", here, not_here, cell, loc)
                if 'is correct' in cell:
                    here[loc] = cell[1]
                elif 'different spot' in cell:
                    not_here[loc] += cell[1]
                loc = (loc % 5) + 1 
        return here, not_here


    def send_str (self, string):
        self.driver.find_element_by_xpath('//body').send_keys(string + Keys.ENTER)
        sleep(1) # give it time to settle down?


    def start_requests(self):
        print ("start requests")
        self.url = 'https://www.quordle.com/#/practice'
        #yield scrapy.Request (url=url, callback=self.parse)
        yield SeleniumRequest (url=self.url, callback=self.parse)

    def parse (self, response):
        print("in parse")
        self.driver = webdriver.Chrome ('/usr/local/bin/chromedriver')
        self.driver.get (self.url)
        [self.send_str (string) for string in ['steam', 'blind', 'cough']]
        sleep (1.0)

        stopped = True
        while stopped:
            sel = scrapy.Selector (text=self.driver.page_source)
            kb = scrapy.Selector (text=sel.xpath ('//div[@aria-label="Keyboard"]').getall()[0])
            boards = [scrapy.Selector (text=sel.xpath (f'//div[contains(@aria-label, "Game Board {i}")]').get()) for i in range(1,5)]
            ##print ("found board", len(board.get()), dir(board))
            ##print (self.process_board (board))
            #for i in range (len (boards)):
            for i in range (4):
                boards = [scrapy.Selector (text=sel.xpath (f'//div[contains(@aria-label, "Game Board {b}")]').get()) for b in range(1,5)]
                board = boards[i]
                #print (i, board.__class__, board.xpath('.//div[@aria-label]').getall())
                if self.process_kb (kb, board):
                    print ("grabbing the data, again")
                    break  # not right? board needs to be moved sometimes?
                try:
                    #print ("element")
                    _ = self.driver.find_element_by_xpath('//div/a[@class="quordle-nav inactive"]').is_selected()
                    #print("here",  self.driver.find_element_by_xpath('//div.text'))
                    #print ("element", self.driver.find_element_by_xpath('//div/a[@class="quordle-nav inactive"]').is_selected())
                    sleep (1)
                except Exception as e:
                    print ("failed", e)
                    stopped = False
        sleep (10)
        self.driver.quit ()

    def __del__ (self):
        self.driver.quit()
