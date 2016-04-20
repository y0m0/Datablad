#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# yattag.py
#
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

                        with tag ('div', klass='product-picture'):
                            doc.stag('img', src='102029.jpg', alt='Product Picture')


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
                                        text('Pakning: ' + prod.weight.text + prod.weightunit.text)

                            with tag('div', klass='ingredients'):
                                with tag('h2'):
                                    text('Ingredienser')
                                with tag('p', klass='field'):
                                    # if hasattr(prod, 'prodnote'):
                                    #     text(prod.prodnote.text)
                                    # else:
                                    #     text('no data yet')
                                    text(prod.prodnote.text)


                    with tag('div', klass='secondary-content'):

                        with tag('div', klass='energy'):
                            with tag('h2'):
                                text('Næringsinnehold Pr. 100 gram.')
                            with tag('ul', klass='field'):
                                with tag('li'):
                                    text('Energi(kcal/kj) 437/1931')
                                with tag('li'):
                                    text('Fett 45g')
                                with tag('li'):
                                    text('hvorav Mettet Fett 5,4g')
                                with tag('li'):
                                    text('Karbohydrat 4,2g')
                                with tag('li'):
                                    text('hvorav Sukker 1,5g')
                                with tag('li'):
                                    text('Protein 4,4g')
                                with tag('li'):
                                    text('Salt 2,2g')
                                with tag('li'):
                                    text('Kostfiber 0,7g')

                        with tag('div', klass='allergens'):
                            with tag('h2'):
                                text('Allergener')
                            with tag('ul', klass='field'):
                                for i in range(4):
                                    with tag('li'):
                                        text('....')

                        with tag('div', klass='storage'):
                            with tag('h2'):
                                text('Oppbevaring')
                            with tag('ul', klass='field'):
                                with tag('li'):
                                    text('....')

                with tag('footer', klass='main-footer'):
                    with tag('p'):
                        doc.asis('<a href="www.villaimport.no">www.villaimport.no</a> &#9702; <a href="tel:+4723229999">+47 23229999</a> &#9702; <a href="mailto:mail@villaimport.no">mail@villaimport.no</a>')
                    with tag('p'):
                        doc.asis('&copy; Villa Import AS - 2016')

        with codecs.open(prodcode + '.html', 'w', 'utf-8') as file:
            file.write(indent(doc.getvalue()))


xmlfile = "PESTO.XML"
make_html(get_products(xmlfile))
