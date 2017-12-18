# coding: utf8
from splinter import Browser

url = "https://www.linkedin.com"
browser = Browser('firefox')
browser.visit(url)
browser.fill('session_key', 'michel@ibakus.com')
browser.fill('session_password', 'KibogO*8011')
loginSubmit = browser.find_by_id('login-submit')
loginSubmit.click()

keywords = 'expert+comptable'

browser.visit('https://www.linkedin.com/search/results/index/?keywords=' + keywords + '&origin=GLOBAL_SEARCH_HEADER')

results = browser.find_by_css('.search-results__primary-cluster ul.results-list li')
