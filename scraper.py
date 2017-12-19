# coding: utf8
import os
import sys
from splinter import Browser
from random import randint


lkdn_profiles = [
    {'login': 'michel@ibakus.com', 'pwd': 'KibogO*8011'},
    {'login': 'dev3@ibakus.com', 'pwd': 'KibogO*8011'},
    {'login': 'comm.manager@ibakus.com', 'pwd': 'KibogO*8011'}
]

url = "https://www.linkedin.com"
browser = Browser('firefox')
browser.visit(url)

rand_profile = lkdn_profiles[randint(0,len(lkdn_profiles) - 1)]

print "Connexion avec le compte '" + rand_profile['login'] + "'"

browser.fill('session_key', rand_profile['login'])
browser.fill('session_password', rand_profile['pwd'])
loginSubmit = browser.find_by_id('login-submit')
loginSubmit.click()

if len(sys.argv) > 2:
    keywords = sys.argv[1]
else:
    keywords = 'expert comptable'

print "Recherche de(s) mot(s) clé(s) '" + keywords + "'"

browser.visit('https://www.linkedin.com/search/results/index/?keywords=' + keywords + '&origin=GLOBAL_SEARCH_HEADER')

# Force le scroll vers le bas pour éviter de récupérer des résultats vides lorsqu'ils ne sont pas dans le viewport
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
