#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# datablad.py

import re
import codecs
import pdfkit
from lxml import objectify
from collections import OrderedDict
from yattag import Doc, indent


def get_products(file_path):
    tree = objectify.parse(file_path)
    root = tree.getroot()
    prod_dict = {}
    for x in root.findall('g_otemp'):
        prodcode = x.prodid.text
        prod_dict[prodcode] = x
    return prod_dict


def make_html(prod_dict):
    options = {
        'page-size': 'A4',
        'margin-top': '0.2in',
        'margin-right': '0.2in',
        'margin-bottom': '0.2in',
        'margin-left': '0.2in',
        'encoding': "UTF-8"
    }

    for prodcode, prod in prod_dict.items():

        doc, tag, text = Doc().tagtext()
#        try:
        doc.asis('<!DOCTYPE html>')
        with tag('html', lang='eng'):

            with tag('head'):
                doc.asis('<meta charset="UTF-8" />')
                doc.asis('<link rel="stylesheet" type="text/css" href="style-pdf.css">')
                doc.asis('<meta name="viewport" content="width=device-width">')
                with tag('title'):
                    text(prod.prodid.text)

            with tag('body', klass='main'):
                with tag('header', klass='main-header'):
                    doc.stag('img', klass='logo', src='logo.jpg', alt='Villa Import AS')
                    with tag('h1', klass='prodname'):
                        text(prod.desc.text)

                with tag('div', klass='content'):
                    with tag('div', klass='primary-content clearfix'):

                        with tag('div', klass='product-picture'):
                            doc.stag('img',
                                     src='http://www.villaimport.no/images/produktbilder/Full%20Size/' +
                                         prod.prodid.text + '.jpg', alt=prod.desc.text)

                        with tag('div', klass='product-details'):
                            with tag('div', klass='basic-info'):
                                with tag('h2'):
                                    text('Produktinformasjon')
                                with tag('ul', klass='field'):
                                    with tag('li'):
                                        text('Varenummer: ' + prod.prodid.text)
                                    with tag('li'):
                                        text('Produktgruppe: ' + prod.prodgroupex.text)
                                    with tag('li'):
                                        text('Pakning: ' + re.sub('.000', '',
                                                                  prod.weight.text) + ' ' + prod.weightunit.text)

                            with tag('div', klass='ingredients'):
                                with tag('h2'):
                                    text('Ingredienser')
                                with tag('p', klass='field'):
                                    print(prod.prodnote.text + '\n')
                                    text(prod.prodnote.text)

                    with tag('div', klass='secondary-content clearfix'):
                        with tag('div', klass='col-1'):
                            with tag('div', klass='energy'):
                                with tag('table'):
                                    with tag('thead'):
                                        with tag('tr'):
                                            with tag('th', colspan='2'):
                                                text('Næringsinnehold Pr. 100 gram.')
                                    with tag('tbody'):
                                        for lines in re.split('\n', prod.technote.text):
                                            line = lines.lstrip()
                                            if line != "":
                                                with tag('tr'):
                                                    value = re.split('    ', line)
                                                    with tag('td'):
                                                        text(value[0])
                                                    with tag('td'):
                                                        text(value[1])

                            with tag('div', klass='storage'):
                                with tag('table'):
                                    with tag('thead'):
                                        with tag('tr'):
                                            with tag('th', colspan='2'):
                                                text('Oppbevaring')
                                    with tag('tbody'):
                                        for lines in re.split('\n', prod.annenote.text):
                                            line = lines.lstrip()
                                            with tag('tr'):
                                                value = re.split('    ', line)
                                                with tag('td'):
                                                    text(value[0])
                                                with tag('td'):
                                                    text(value[1])

                        with tag('div', klass='col-2'):
                            with tag('div', klass='allergens'):
                                allergens = OrderedDict([('gluten', 'nei'),
                                                         ('skalldyr', 'nei'),
                                                         ('egg', 'nei'),
                                                         ('fisk', 'nei'),
                                                         ('peanøtter', 'nei'),
                                                         ('soya', 'nei'),
                                                         ('melk', 'nei'),
                                                         ('nøtter', 'nei'),
                                                         ('selleri', 'nei'),
                                                         ('sennep', 'nei'),
                                                         ('sesamfrø', 'nei'),
                                                         ('sulfitter', 'nei'),
                                                         ('lupin', 'nei'),
                                                         ('bløtdyr', 'nei')])
                                with tag('table'):
                                    with tag('thead'):
                                        with tag('tr'):
                                            with tag('th', colspan='2'):
                                                text('Allergener')
                                    with tag('tbody'):
                                        for word in re.split('[.,() ]+', prod.prodnote.text):
                                            if word.isupper() and word.isalpha() and len(word) > 2:
                                                if word.lower() in allergens:
                                                    allergens[word.lower()] = 'ja'
                                        if hasattr(prod, 'supportnote'):
                                            for word in re.split('[.,() ]+', prod.supportnote.txt):
                                                if word.isupper() and word.lower() in allergens:
                                                    allergens[word.lower()] = 'kan'
                                        for key, value in allergens.items():
                                            with tag('tr'):
                                                with tag('td'):
                                                    text(key.capitalize())
                                                with tag('td'):
                                                    text(value.capitalize())

                with tag('footer', klass='main-footer'):
                    with tag('p'):
                        doc.asis(
                            '''<a href="www.villaimport.no">www.villaimport.no</a> &#9702;
                            <a href="tel:+4723229999">+47 23229999</a> &#9702;
                            <a href="mailto:mail@villaimport.no">mail@villaimport.no</a>''')
                    with tag('p'):
                        doc.asis('&copy; Villa Import AS - 2016')

        with codecs.open(prodcode + ' - ' + prod.desc.text + '.html', 'w', 'utf-8') as file:
            file.write(indent(doc.getvalue()))
    location = prodcode + ' - ' + prod.desc.text
    pdfkit.from_file(location + '.html', location + '.pdf', options=options)

 #       except:
 #           incomplete.write(prod.prodid.text + '\n')
 #           continue


def select_products(prod_dict, selection=None):
    if selection is None:
        return prod_dict
    new_dict = {i: prod_dict[i] for i in prod_dict if i in selection}
    return new_dict


incomplete = open('incomplete.txt', 'w+')
xmlfile = input('Select a Catalog File: ')
selected_products = input('Select a list of Products: ')
with open(selected_products, 'r') as f:
    products = [x.rstrip('\n') for x in f.readlines()]
    make_html(select_products(get_products(xmlfile), products))
