# coding: utf8
import os
import sys
from splinter import Browser
from random import randint


lkdn_profiles = [
    {'login': 'michel@ibakus.com', 'pwd': 'KibogO*8011'},
    #{'login': 'dev3@ibakus.com', 'pwd': 'KibogO*8011'},
    #{'login': 'comm.manager@ibakus.com', 'pwd': 'KibogO*8011'}
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

browser.visit('https://www.linkedin.com/search/results/people/?facetGeoRegion=["lu%3A0"]&facetNetwork=%5B%22S%22%2C%22O%22%5D&keywords=' + keywords + '&origin=FACETED_SEARCH')

# Force le scroll vers le bas pour éviter de récupérer des résultats vides lorsqu'ils ne sont pas dans le viewport
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
browser.execute_script("window.scrollTo(0, 0);")

results = browser.find_by_css('.search-results__primary-cluster ul.results-list li.search-result')

for i,result in enumerate(results):
    name = result.find_by_css('span.name')
    tagline = result.find_by_css('p.subline-level-1')
    position = result.find_by_css('p.search-result__snippets')
    location = result.find_by_css('p.subline-level-2')
    action = result.find_by_css('button.search-result__actions--primary')

    print {
        'name': name.html.encode('utf8','xmlcharrefreplace').strip(),
        'tagline': tagline.html.encode('utf8', 'xmlcharrefreplace').strip(),
        'job position': position.html.encode('utf8','xmlcharrefreplace').strip(),
        'location': location.html.encode('utf8','xmlcharrefreplace').strip(),
        'action': action.html.encode('utf8','xmlcharrefreplace').strip()
    }
