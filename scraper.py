# coding: utf8
import os
import sys
import time
from splinter import Browser
from random import randint

browser = Browser('firefox')

def main():
    lkdn_profiles = [
        {'login': 'michel@ibakus.com', 'pwd': 'KibogO*8011'},
        #{'login': 'dev3@ibakus.com', 'pwd': 'KibogO*8011'},
        #{'login': 'comm.manager@ibakus.com', 'pwd': 'KibogO*8011'}
    ]

    url = "https://www.linkedin.com"
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
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, 0);")

    getPageList()

# Fonction permettant d'afficher la liste des personnes de la page
def getPageList():
    time.sleep(10)
    # Récupère la liste de résultats
    results = browser.find_by_css('.search-results__primary-cluster ul.results-list li.search-result')

    # Affiche les informations voulue
    for i,result in enumerate(results):
        name = result.find_by_css('span.name')
        tagline = result.find_by_css('p.subline-level-1')
        position = result.find_by_css('p.search-result__snippets')
        location = result.find_by_css('p.subline-level-2')
        action = result.find_by_css('button.search-result__actions--primary')

        print {
            'name': name.html.encode('utf8','xmlcharrefreplace').strip() if len(name) > 0 else None,
            'tagline': tagline.html.encode('utf8', 'xmlcharrefreplace').strip() if len(tagline) > 0 else None,
            'job position': position.html.encode('utf8','xmlcharrefreplace').strip() if len(position) > 0 else None,
            'location': location.html.encode('utf8','xmlcharrefreplace').strip() if len(location) > 0 else None,
            'action': action.html.encode('utf8','xmlcharrefreplace').strip() if len(action) > 0 else None
        }

    if browser.is_element_present_by_css('button.next'):
        nextButton = browser.find_by_css('button.next')
        nextButton.click()
        
        # Force le scroll vers le bas pour éviter de récupérer des résultats vides lorsqu'ils ne sont pas dans le viewport
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        browser.execute_script("window.scrollTo(0, 0);")

        getPageList()

main()
