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

#window.scrollTo(0, document.body.scrollHeight)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

results = browser.find_by_css('.search-results__primary-cluster ul.results-list li.search-result')

for i,result in enumerate(results):
    try:
        name = result.find_by_css('span.name')
        print name.html.encode('utf8','xmlcharrefreplace')
    except:
        try:
            name = result.find_by_css('h3.actor-name-with-distance')
            print name.html.encode('utf8','xmlcharrefreplace')
        except:
            print "error"
