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
                with tag('p', klass='prodid'):
                    text('prodid: ' + prod.prodid.text)
                with tag('h4', klass='title'):
                    text('Produktnavn: ')
                with tag('h1', klass='prodname'):
                    text(prod.desc.text)
                with tag('h2', klass='ingredienser'):
                    text('Ingredienser')
                with tag('p', klass='ingredienser'):
                    if hasattr(prod, 'prodnote'):
                        text(prod.prodnote.text)
                    else:
                        text('no data yet')
                with tag('h2', klass='energy'):
                    text('Næringsinneholder for 100g')
                with tag('p', klass='energy'):
                    if hasattr(prod, 'technote'):
                        text(prod.technote.text)
                    else:
                        text('no data yet')
                with tag('h2', klass='allergener'):
                    text('Allergener')
                with tag('p', klass='allergener'):
                    text('allergener....')
                with tag('h2', klass='shelf'):
                    text('Oppbevaring')
                with tag('p', klass='shelf'):
                    text('shelf-life, temp')

        with codecs.open(prodcode + '.html', 'w', 'utf-8') as file:
            file.write(indent(doc.getvalue()))


xmlfile = "PESTO.XML"
make_html(get_products(xmlfile))
