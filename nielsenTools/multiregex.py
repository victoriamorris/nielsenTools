#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Classes for making multiple regex replacements."""

import sys

import regex as re

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


class MultiRegex(object):
    simple = False
    regexes = ()

    def __init__(self):
        try:
            self._rx = re.compile('|'.join(self.regexes), flags=re.IGNORECASE)
        except:
            for r in self.regexes:
                try:
                    re.compile(r)
                except:
                    print('Error in regex: {}'.format(str(r)))

    def sub(self, s):
        if not s or s is None: return ''
        return self._rx.sub(self._sub, s)

    def _sub(self, mo):
        try:
            for k, v in mo.groupdict().items():
                if v:
                    if k == 'AllElse':
                        return ''
                    if 'UUU' in str(k):
                        return bytes(str(k).replace('UUU', '\\' + 'u'), 'ascii').decode('unicode-escape')
                    try:
                        sub = getattr(self, k)
                        if callable(sub):
                            return sub(mo)
                        else:
                            return sub
                    except:
                        return str(k)

        except:
            print('\nError MR: {0}\n'.format(str(sys.exc_info())))


class Abbreviations(MultiRegex):
    simple = True
    regexes = (
        r'(?P<January>^jan(uary)?\.*$)',
        r'(?P<February>^feb(ruary)?\.*$)',
        r'(?P<March>^m(ar|rz)(ch)?\.*$)',
        r'(?P<April>^apr(il)?\.*$)',
        r'(?P<June>^june?\.*$)',
        r'(?P<July>^july?\.*$)',
        r'(?P<August>^aug(ust)?\.*$)',
        r'(?P<September>^sept?(ember)?\.*$)',
        r'(?P<October>^o[ck]t(ober)?\.*$)',
        r'(?P<November>^nov(ember)?\.*$)',
        r'(?P<December>^de[cz](ember)?\.*$)',
        r'(?P<Monday>^mon(day)?s?\.*$)',
        r'(?P<Tuesday>^tues?(day)?s?\.*$)',
        r'(?P<Wednesday>^wed(ne)?s?(day)?s?\.*$)',
        r'(?P<Thursday>^thur?s?(day)?s?\.*$)',
        r'(?P<Friday>^fri(day)?s?\.*$)',
        r'(?P<Saturday>^sat(urday)?s?\.*$)',
        r'(?P<Sunday>^sun(day)?s?\.*$)',
        r'(?P<Abbildung>^abb(ildung)?\.*$)',    # German, illustration, figure
        r'(?P<Abdruck>^abdr(uck)?\.*$)',        # German, impression, print, reproduction
        r'(?P<Abhandlung>^abh(andlung)?\.*$)',  # German, treatise
        r'(?P<AbkUUU00FCrzung>^abk(.rzung)?\.*$)',  # German, abbreviation
        r'(?P<Abschrift>^abschr(ift)?\.*$)',    # German, reprint, copy
        r'(?P<Abteilung>^abt(eilung)?\.*$)',    # German
        r'(?P<approximately>^(ca|approx)\.*$)',
        r'(?P<Auflage>^aufl(age)?\.*$)',     # German, edition
        r'(?P<Ausgabe>^ausg(abe)?\.*$)',     # German, edition
        r'(?P<augmented>^aug(mented)\.*$)',
        r'(?P<BUUU00E4ndchen>^b(aen)?dche?n\.*$)',   # German
        r'(?P<BUUU00E4nde>^b(ae?n)?de\.*$)',    # German
        r'(?P<Band>^b(an)?d\.*$)',              # German, volume
        r'(?P<Bearbeitung>^bearb(eitung)?\.*$)',    # German, arrangement
        r'(?P<Beiheft>^beih(eft)?\.*$)',        # German, supplement
        r'(?P<Beispiel>^beisp(iel)?\.*$)',      # German, example
        r'(?P<beziehungsweise>^be?z(iehungs)?w(eise)?\.*$)',    # German, respectively; or, or else; more specifically
        r'(?P<bibliography>^bibl(iog)?(raphy)?\.*$)',
        r'(?P<books>^bo*ks\.*$)',
        r'(?P<book>^bo*k\.*$)',
        r'(?P<Buchhandler>^buchh(andler)?\.*$)',    # German, bookseller
        r'(?P<CDs>^cd-?(rom)?s\.*$)',
        r'(?P<CD>^cd-?(rom)?\.*$)',
        r'(?P<chiefly>^chiefle*y\.*$)',
        r'(?P<cm>^cm\.*$)',
        r'(?P<coloured>^colo+u?red\.*$)',
        r'(?P<colour>^col(o+u?r|eur)?\.*$)',
        r'(?P<columns>^col(umn)?s\.*$)',
        r'(?P<corrected>^corr(ected)?\.*$)',
        r'(?P<cover>^couv(erture)?\.*$)',
        r'(?P<deel>^de*l\.*$)',     # Dutch
        r'(?P<Department>^dept\.*$)',
        r'(?P<diagrams>^diagra?m?s*\.*$)',
        r'(?P<dopolnennoe>^dop(ol)?(nennoe)?\.*$)',  # Russian
        r'(?P<DVDs>^dvd-?(rom)?s\.*$)',
        r'(?P<DVD>^dvd-?(rom)?\.*$)',
        r'(?P<UUU00E9dition>^[\u00e9\u00C9]d(ition)?\.*$)',     # édition
        r'(?P<edition>^ed(itio)?n?\.*$)',
        r'(?P<Einleitung>^einl(eitung)?\.*$)',  # German, introduction
        r'(?P<ekdosi>^ekd(osi)?\.*$)',          # Greek
        r'(?P<engraved>^engr(aved)?\.*$)',
        r'(?P<enlarged>^enl(arged)?\.*$)',
        r'(?P<erweiterte>^erw(eit)?(erte)?\.*$)',   # German
        r'(?P<fascicule>^fasc(icule)?\.*$)',    # French
        r'(?P<facsimiles>^fa(cs|sc)(im)?(ile)?s\.*$)',
        r'(?P<facsimile>^fa(cs|sc)(im)?(ile)?\.*$)',
        r'(?P<feet>^f[e]*t\.*$)',
        r'(?P<figures>^fig(ures)?s*\.*$)',
        r'(?P<folded>^(ofld|fold(ed)?)\.*$)',
        r'(?P<folio>^fol[io.]*\.*$)',
        r'(?P<folios>^fol[io.]*s\.*$)',
        r'(?P<frames>^fr(ame)?s*\.*$)',
        r'(?P<frontispiece>^front(\.|is)(piece)?\.*$)',
        r'(?P<gedruckt>^gedr(uckt)?\.*$)',      # German, printed
        r'(?P<Gegenwart>^gegenw(art)?\.*$)',    # German, present time
        r'(?P<genealogical>^geneal(ogical)?\.*$)',
        r'(?P<geological>^geol(og)?(ical)?\.*$)',
        r'(?P<garren>^g(arre)?n\.*$)',          # Basque, nth
        r'(?P<Handbuch>^h(an)?db(uch)?\.*$)',   # German, handbook, manual
        r'(?P<hardback>^h(ard)?b(ac)?k\.*$)',
        r'(?P<Hefte>^he*fte\.*$)',              # German
        r'(?P<Heft>^he*ft\.*$)',                # German
        r'(?P<Herausgeber>^he?r(au)?sg(eber)?\.*$)',    # German, editor
        r'(?P<illustrations>^a?il+u?s?(tration.*)?s?\.*$)',
        r'(?P<impression>^impr(ession)?\.*$)',
        r'(?P<including>^incl?(uding)?\.*$)',
        r'(?P<introduction>^introd(uction)?\.*$)',
        r'(?P<ispravlennoe>^ispr(avl)?(ennoe)?\.*$)',   # Russian
        r'(?P<izdaniye>^izd(aniye)?\.*$)',      # Russian
        r'(?P<Jahreszahl>^j(ahres)?z(ah)?l\.*$)',       # German, date, year
        r'(?P<jaargang>^jaarg(ang)?\.*$)',      # Dutch
        r'(?P<Jahrgang>^jahrg(ang)?\.*$)',      # German
        r'(?P<Jahrhundert>^j(ahr)?h(undert)?\.*$)',     # German, century
        r'(?P<knjiga>^knj(iga)?\.*$)',          # Croatian
        r'(?P<mahadurah>^mahad(urah)?\.*$)',    # Hebrew
        r'(?P<manuscript>^m(ss*|anuscripts?)\.*$)',
        r'(?P<microfiche>^micr[io]-*fiches*\.*$)',
        r'(?P<microfilm>^micr[io]-*film*\.*$)',
        r'(?P<minutes>^min(ute)?s\.*$)',
        r'(?P<Mitarbeiter>^mitarb(eiter)?\.*$)',    # German, collaborator
        r'(?P<Mitwirkung>^mitw(irkung)?\.*$)',      # German, cooperation
        r'(?P<mm>^mm\.*$)',
        r'(?P<music>^mus(ic)?\.*$)',
        r'(?P<Nachricht>^nachr(icht)?\.*$)',    # German, communication, report, notice
        r'(?P<Nachwort>^nachw(ort)?\.*$)',      # German, concluding remarks, epilogue
        r'(?P<nakladateUUU0142stvUUU00ed>^nakl(ad)?(ate)?\.*$)',      # Czech, nakladatełství
        r'(?P<Neudruck>^neudr(uck)?\.*$)',      # German, reprint
        r'(?P<nouvelle>^nouv(elle)?\.*$)',      # French
        r'(?P<numbers>^n-*(o|ro?|um+b?ero?)s*\.*$)',
        r'(?P<oblong>^obl(ong)?\.*$)',
        r'(?P<Originalausgabe>^Originalausg(abe)?\.*$)',        # German
        r'(?P<pages>^pp+(age)?s*\.*$)',
        r'(?P<paperback>^p(aper)?b(ac)?k\.*$)',
        r'(?P<parts>^p(ar)?t\.*$)',
        r'(?P<patippu>^pat(ippu)?\.*$)',        # Russian
        r'(?P<plates>^pl(at)?e?s*\.*$)',
        r'(?P<poprawione>^popr(awione)?\.*$)',  # Polish, corrected
        r'(?P<portraits>^portr?(ait)?s*\.*$)',
        r'(?P<reprinted>^re-*pr(int)?(ed)?\.*$)',
        r'(?P<revised>^rev(ised)?\.*$)',
        r'(?P<Sammelwerk>^s(ammel)?w(er)?k\.*$)',       # German, collected works
        r'(?P<Sammlung>^samml(ung)?\.*$)',              # German, collection, compilation, set
        r'(?P<Schriftleiter>^schriftl(eiter)?\.*$)',    # German, editor
        r'(?P<selfUUU002Dportraits>^self-?portr?(ait)?s*\.*$)',
        r'(?P<series>^ser(ies)?\.*$)',
        r'(?P<sheet>^sh\.*$)',
        r'(?P<stereograph>^stereo-?graph\.*$)',
        r'(?P<sound>^s(oun)?d\.*$)',
        r'(?P<Stimmbuch>^st(imm)?b(uch)?\.*$)',     # German, part book
        r'(?P<supplement>^suppl?(ement)?\.*$)',
        r'(?P<svazek>^sv(azek)?\.*$)',      # Czech
        r'(?P<tomes>^tome?s*\.*$)',
        r'(?P<undUUU0020soUUU0020weiter>^u(nd)?\s*so?\s*w(eiter)?\.*$)',    # German, and so forth, etc.
        r'(?P<unnumbered>^un-?numbered\.*$)',
        r'(?P<updated>^upd(ated)?\.*$)',
        r'(?P<uzupeUUU0142nione>^uzup(elnione)?\.*$)',  # Polish, uzupełnione
        r'(?P<Verfasser>^verf(asser)?\.*$)',        # German, composer, writer
        r'(?P<vergleich>^vergl(eich)?\.*$)',        # German, compare
        r'(?P<Verzeichnis>^verz(eichnis)?\.*$)',    # German, catalogue
        r'(?P<videodisc>^video-*disc\.*$)',
        r'(?P<volumes>^vol?(ume)?s*\.*$)',
        r'(?P<Vorwort>^vorw(ort)?\.*$)',    # German, foreword
        r'(?P<vydUUU00E1nUUU00ED>^vyd(ani)?\.*$)',      # Czech, vydání
        r'(?P<vypusk>^vyp(usk)?\.*$)',      # Russian
        r'(?P<wydanie>^wyd(anie)?\.*$)',    # Polish
        r'(?P<years>^y(ea)?rs\.*$)',
        r'(?P<year>^y(ea)?r\.*$)',
        r'(?P<Zeitschrift>^z(ei)?tschr(ift)?\.*$)',     # German, periodical
        r'(?P<Zeitung>^z(ei)?t(un)?g\.*$)',  # German, newspaper
        r'(?P<zeszyt>^zesz(yt)?\.*$)',      # Polish
        r'(?P<zvezek>^zv(ezek)?\.*$)',      # Slovenian, volumes
        )
