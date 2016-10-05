#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# yattag.py
#
import re
import codecs
from lxml import objectify
from yattag import Doc, indent


def get_products(file_path):
    tree = objectify.parse(file_path)
    root = tree.getroot()
    products = {}
    for x in root.findall('g_otemp'):
        prodcode = x.prodid.text
        products[prodcode] = x
    return products


def make_html(prod_dict):
    for prodcode, prod in prod_dict.items():

        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html', lang='eng'):

            with tag('head'):
                doc.asis('<meta charset="UTF-8" />')
                doc.asis('<link rel="stylesheet" type="text/css" href="style.css">')
                doc.asis('<meta name="viewport" content="width=device-width">')
                with tag('title'):
                    text(prod.prodid.text)

            with tag('body', klass='main'):
                with tag('header', klass='main-header'):
                    doc.stag('img', klass='logo', src='logo.jpg', alt='Villa Import AS')
                    with tag('h1', klass='prodname'):
                        text(prod.desc.text)

                with tag('div', klass='content'):
                    with tag('div', klass='primary-content group'):

                        with tag('div', klass='product-picture'):
                            doc.stag('img', src='http://www.villaimport.no/images/produktbilder/Full%20Size/'+ prod.prodid.text + '.jpg', alt=prod.desc.text)

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
                                    text(prod.prodnote.text)

                    with tag('div', klass='secondary-content'):
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
                                            print(line)
                                            with tag('tr'):
                                                value = re.split('    ', line)
                                                print(value)
                                                with tag('td'):
                                                    text(value[0])
                                                with tag('td', klass='amount'):
                                                    text(value[1])

                        with tag('div', klass='allergens'):
                            allergens = {'gluten':'nei',
                                        'skalldyr':'nei',
                                        'egg':'nei',
                                        'fisk':'nei',
                                        'peanøtter':'nei',
                                        'soya':'nei',
                                        'melk':'nei',
                                        'nøtter':'nei',
                                        'selleri':'nei',
                                        'sennep':'nei',
                                        'sesamfrø':'nei',
                                        'svoveldioksid eller sulfitter':'nei',
                                        'lupin':'nei',
                                        'bløtdyr':'nei'
                                        }
                            with tag('h2'):
                                text('Allergener')
                            with tag('ul', klass='field'):
                                for word in set(re.split('[\[\]/{}.,() ]+', prod.prodnote.text)):
                                    if word.isupper() and word.isalpha():
                                        with tag('li'):
                                            text(word.capitalize())

                        with tag('div', klass='storage'):
                            with tag('h2'):
                                text('Oppbevaring')
                            with tag('ul', klass='field'):
                                for word in re.split('\n', prod.annenote.text):
                                    with tag('li'):
                                        text(word)

                with tag('footer', klass='main-footer'):
                    with tag('p'):
                        doc.asis(
                            '''<a href="www.villaimport.no">www.villaimport.no</a> &#9702;
                            <a href="tel:+4723229999">+47 23229999</a> &#9702;
                            <a href="mailto:mail@villaimport.no">mail@villaimport.no</a>''')
                    with tag('p'):
                        doc.asis('&copy; Villa Import AS - 2016')

        with codecs.open(prodcode + '.html', 'w', 'utf-8') as file:
            file.write(indent(doc.getvalue()))


xmlfile = input('Select a Catalog File: ');
make_html(get_products(xmlfile))
