# coding: utf8
import os
import sys
import time
import random
from splinter import Browser
from random import randint

browser = Browser('firefox', headless=True)

# Fonction permettant de construire le message à envoyer
def setMessage(item):
    message = u"Bonjour " + item['firstname'].decode('utf-8') + u",\r\nJ'aimerai beaucoup faire partie de votre réseau sur LinkedIn.\r\nNous développons des solutions technologiques anti-blanchiment à destination de votre métier et cela pourrait potentiellement vous intéresser dans le futur.\r\n\r\nBien à vous,\r\n\r\nMichel"
    return message

# Fonction permettant d'afficher la liste des personnes de la page
def getPageList(stop):
    time.sleep(5)
    # Récupère la liste de résultats
    results = browser.find_by_css('.search-results__primary-cluster ul.results-list li.search-result')

    # Affiche les informations voulue
    for i,result in enumerate(results):
        name = result.find_by_css('span.name')
        tagline = result.find_by_css('p.subline-level-1')
        position = result.find_by_css('p.search-result__snippets')
        location = result.find_by_css('p.subline-level-2')
        action = result.find_by_css('button.search-result__actions--primary')

        item = {
            'name': name.html.encode('utf8','xmlcharrefreplace').strip() if len(name) > 0 else None,
            'firstname': name.html.encode('utf8','xmlcharrefreplace').strip().split(' ')[0].capitalize() if len(name) > 0 else None,
            'tagline': tagline.html.encode('utf8', 'xmlcharrefreplace').strip() if len(tagline) > 0 else None,
            'job position': position.html.encode('utf8','xmlcharrefreplace').strip() if len(position) > 0 else None,
            'location': location.html.encode('utf8','xmlcharrefreplace').strip() if len(location) > 0 else None,
            'action': action.html.encode('utf8','xmlcharrefreplace').strip() if len(action) > 0 else None
        }

        # Si le bouton permet de se connecter, on clique dessus puis on envoi un message prédéfini
        if item['action'] == "Se connecter":
            print "Click pour " + item['name']
            action.click()

            # On clique sur le bouton permettant d'écrire un message à envoyer en plus de la demande de connexion
            addNote = browser.find_by_css('div.send-invite__actions button.button-secondary-large.mr1')
            print "Click sur Ajouter une note"
            addNote.click()

            # Rempli le champ de message avant d'envoyer la demande de connexion
            message = setMessage(item)
            browser.fill('message', message)
            sendInvite = browser.find_by_css('div.send-invite__actions button.button-primary-large.ml1')
            print "Click sur Terminé"
            sendInvite.click()
            time.sleep(30)
        print "----"

    # Si un lien permettant de passer à la page de résultats suivants est présent, on clique dessus puis on appelle getPageList()
    if browser.is_element_present_by_css('button.next'):
        nextButton = browser.find_by_css('button.next')
        nextButton.click()

        # Force le scroll vers le bas pour éviter de récupérer des résultats vides lorsqu'ils ne sont pas dans le viewport
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        browser.execute_script("window.scrollTo(0, 0);")

        if (stop == False):
            getPageList(stop)

# Fonction principale
def main():
    print sys.argv

    if "--user" in sys.argv:
        login = sys.argv[sys.argv.index("--user") + 1]
    elif "-u" in sys.argv:
        login = sys.argv[sys.argv.index("-u") + 1]
    else:
        sys.exit("Erreur : le paramètre `--user` ou `-u` n'est pas renseigné")

    if "--password" in sys.argv:
        pwd = sys.argv[sys.argv.index("--password") + 1]
    elif "-w" in sys.argv:
        pwd = sys.argv[sys.argv.index("-w") + 1]
    else:
        sys.exit("Erreur : le paramètre `--password` ou `-w` n'est pas renseigné")

    if "--keywords" in sys.argv:
        keywords = sys.argv[sys.argv.index("--keywords") + 1]
    elif "-k" in sys.argv:
        keywords = sys.argv[sys.argv.index("-k") + 1]
    else:
        keywords = 'expert comptable'

    if "--page" in sys.argv:
        page = sys.argv[sys.argv.index("--page") + 1]
    elif "-p" in sys.argv:
        page = sys.argv[sys.argv.index("-p") + 1]
    else:
        page = str(1)


    if "--stop" in sys.argv:
        stop = True
    elif "-s" in sys.argv:
        stop = True
    else:
        stop = False

    print "Connexion avec le compte '" + login + "'"
    url = "https://www.linkedin.com"
    browser.visit(url)

    browser.fill('session_key', login)
    browser.fill('session_password', pwd)
    loginSubmit = browser.find_by_id('login-submit')
    loginSubmit.click()

    print "Recherche de(s) mot(s) clé(s) '" + keywords + "'"
    #sys.exit()

    filters = []

    # filtre = relation : 2e, 3e et +; lieux : france, region de paris, region de lyon, region de metz; secteurs : Comptabilité, Services financiers; langue : Français
    filters.append('?company=&facetGeoRegion=%5B"fr%3A0"%2C"fr%3A5227"%2C"fr%3A5210"%2C"fr%3A5213"%5D&facetIndustry=%5B"47"%2C"43"%5D&facetNetwork=%5B"S"%2C"O"%5D&facetProfileLanguage=%5B"fr"%5D&keywords=' + keywords + '&origin=FACETED_SEARCH' + '&page=' + page)

    # filtres = relation : 2e, 3e et +; lieux : belgique, region de bruxelles; secteurs : Avocats, Services juridiques, Institutions judiciaires
    filters.append('?facetGeoRegion=%5B"be%3A0"%2C"be%3A4920"%5D&facetIndustry=%5B"9"%2C"10"%2C"73"%5D&facetNetwork=%5B"S"%2C"O"%5D&facetProfileLanguage=%5B"fr"%5D&keywords=' + keywords + '&origin=FACETED_SEARCH' + '&page=' + page)

    # filtres = relation : 2e, 3e et +; lieux : belgique; secteurs : Comptabilité, Services financiers; langue : Français
    filters.append( '?facetGeoRegion=%5B"be%3A0"%5D&facetIndustry=%5B"47"%2C"43"%5D&facetNetwork=%5B"S"%2C"O"%5D&facetProfileLanguage=%5B"fr"%5D&keywords=' + keywords + '&origin=FACETED_SEARCH' + '&page=' + page)

    # filtres = relation : 2e, 3e et +; lieux: luxembourg;
    filters.append('?facetGeoRegion=["lu%3A0"]&facetNetwork=%5B%22S%22%2C%22O%22%5D&keywords=' + keywords + '&origin=FACETED_SEARCH')

    browser.visit('https://www.linkedin.com/search/results/people/' + random.choice(filters))
    # Force le scroll vers le bas pour éviter de récupérer des résultats vides lorsqu'ils ne sont pas dans le viewport
    time.sleep(3)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    browser.execute_script("window.scrollTo(0, 0);")

    getPageList(stop)

main()
