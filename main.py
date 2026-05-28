import pygame
import random
import json
import os
import math

pygame.init()

szerokosc = 1100
wysokosc = 720
okno = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption("Bydgost - Sciezka Byd")

bialy = (255, 255, 255)
czarny = (0, 0, 0)
szary = (130, 130, 130)
ciemny_szary = (60, 60, 60)
jasny_szary = (235, 235, 235)
zielony = (60, 160, 70)
ciemna_zielen = (35, 110, 45)
jasna_trawa = (90, 185, 95)
brazowy = (145, 102, 62)
jasny_braz = (190, 145, 100)
piaskowy = (210, 185, 140)
niebieski = (70, 130, 220)
blekit = (120, 200, 255)
zolty = (255, 215, 50)
pomaranczowy = (255, 140, 0)
czerwony = (220, 45, 45)
ciemna_czerwien = (150, 20, 20)
fioletowy = (150, 85, 200)
zielony_hp = (0, 205, 0)
bez_owcy = (245, 245, 240)
kremowy = (250, 235, 190)
kotowy = (210, 150, 90)
ciemny_kot = (80, 70, 70)
nocny_niebieski = (20, 30, 60)
zmierzch = (70, 50, 90)

rozmiar_kafelka = 32

mapa_szerokosc = 300
mapa_wysokosc = 220

szerokosc_swiata = mapa_szerokosc * rozmiar_kafelka
wysokosc_swiata = mapa_wysokosc * rozmiar_kafelka

font = pygame.font.SysFont("arial", 22)
font_maly = pygame.font.SysFont("arial", 18)
font_duzy = pygame.font.SysFont("arial", 28, bold=True)
font_akt = pygame.font.SysFont("arial", 24, bold=True)
font_wybor = pygame.font.SysFont("arial", 22, bold=True)
font_dymek = pygame.font.SysFont("arial", 17, bold=True)
font_bardzo_maly = pygame.font.SysFont("arial", 14)

zegar = pygame.time.Clock()
plik_zapisu = "savegame.json"

lokacja = "zewnatrz"

gracz_szerokosc = 26
gracz_wysokosc = 30
predkosc = 4
gracz_x = 18 * rozmiar_kafelka
gracz_y = 18 * rozmiar_kafelka
ostatni_kierunek = "dol"

gracz_max_hp = 100
gracz_hp = 100
gracz_nie_dostaje_obrazen_timer = 0

stamina_max = 100
stamina = 100
stamina_wyswietlana = 100
regen_staminy_timer = 0

koszt_ataku = 14
koszt_bloku = 8
koszt_uniku = 20

perfect_block_timer = 0
perfect_block_okno = 8
perfect_block_cooldown = 0

atak_aktywny = False
atak_timer = 0
atak_cooldown = 0
atak_rect = pygame.Rect(0, 0, 0, 0)
atak_trafil = False

blok_aktywny = False
blok_timer = 0
blok_cooldown = 0

unik_timer = 0
unik_cooldown = 0
czy_unik = False

poziom = 1
exp = 0
exp_do_nastepnego = 60

drewniany_miecz_posiadany = False
drewniany_miecz_zalozony = False
klucz_do_wiatraka = False
wiatrak_otwarty = False

jakub_x = 22 * rozmiar_kafelka
jakub_y = 24 * rozmiar_kafelka
jakub_szerokosc = 28
jakub_wysokosc = 32

michal_x = 28 * rozmiar_kafelka
michal_y = 20 * rozmiar_kafelka
michal_szerokosc = 28
michal_wysokosc = 32

pokaz_dialog = False
tekst_dialogu = ""

pokaz_wybor = False
tekst_wyboru = ""
opcja_1 = ""
opcja_2 = ""
wybor_kontekst = None

akt = 1
nazwa_aktu = "AKT 1: Trakt Bydgostu"
etap_fabuly = 0
sciezka_fabuly = "Byd"
byd_punkty = 0
tekst_zadania = "Zadanie: porozmawiaj z Jakubem"

komunikat_systemowy = ""
komunikat_timer = 0

czas_gry_ms = 0
czas_cyklu_dzien_noc = 60 * 60 * 1000
pora_dnia = "Dzien"
docelowa_ciemnosc = 0
aktualna_ciemnosc = 0.0
kolor_nakladki = (0, 0, 0)

zora_ujawniony = False
wybor_zory_dokonany = False
zora_oszczedzony = False
zora_zabity = False
zora_ucieczka_timer = 0
zora_migniecie_timer = 0
cialo_zory = False
cialo_zory_x = 0
cialo_zory_y = 0

dom_wejscie_rect = pygame.Rect(14 * rozmiar_kafelka, 14 * rozmiar_kafelka, 4 * rozmiar_kafelka, 3 * rozmiar_kafelka)
wiatrak_rect = pygame.Rect(85 * rozmiar_kafelka, 58 * rozmiar_kafelka, 5 * rozmiar_kafelka, 5 * rozmiar_kafelka)
wioska_psoglowych_rect = pygame.Rect(235 * rozmiar_kafelka, 150 * rozmiar_kafelka, 24 * rozmiar_kafelka, 20 * rozmiar_kafelka)

mapa_dom = [
    ["sciana"] * 24,
    ["sciana"] + ["podloga"] * 22 + ["sciana"],
    ["sciana"] + ["podloga"] * 22 + ["sciana"],
    ["sciana"] + ["podloga"] * 22 + ["sciana"],
    ["sciana"] + ["podloga"] * 5 + ["stol"] * 4 + ["podloga"] * 13 + ["sciana"],
    ["sciana"] + ["podloga"] * 22 + ["sciana"],
    ["sciana"] + ["podloga"] * 22 + ["sciana"],
    ["sciana"] + ["podloga"] * 8 + ["lozko"] * 3 + ["podloga"] * 11 + ["sciana"],
    ["sciana"] + ["podloga"] * 22 + ["sciana"],
    ["sciana"] + ["podloga"] * 10 + ["wyjscie"] + ["podloga"] * 11 + ["sciana"],
    ["sciana"] * 24
]

mapa_wiatrak = [
    ["sciana"] * 18,
    ["sciana"] + ["podloga"] * 16 + ["sciana"],
    ["sciana"] + ["podloga"] * 16 + ["sciana"],
    ["sciana"] + ["podloga"] * 16 + ["sciana"],
    ["sciana"] + ["podloga"] * 7 + ["drabina"] + ["podloga"] * 8 + ["sciana"],
    ["sciana"] + ["podloga"] * 6 + ["skrzynia"] * 2 + ["podloga"] * 8 + ["sciana"],
    ["sciana"] + ["podloga"] * 16 + ["sciana"],
    ["sciana"] + ["podloga"] * 7 + ["miecz"] + ["podloga"] * 8 + ["sciana"],
    ["sciana"] + ["podloga"] * 7 + ["wyjscie"] + ["podloga"] * 8 + ["sciana"],
    ["sciana"] * 18
]

mapa_wiatrak_gora = [
    ["sciana"] * 18,
    ["sciana"] + ["podloga"] * 16 + ["sciana"],
    ["sciana"] + ["podloga"] * 16 + ["sciana"],
    ["sciana"] + ["podloga"] * 16 + ["sciana"],
    ["sciana"] + ["podloga"] * 5 + ["mechanizm"] * 6 + ["podloga"] * 5 + ["sciana"],
    ["sciana"] + ["podloga"] * 16 + ["sciana"],
    ["sciana"] + ["podloga"] * 7 + ["drabina_dol"] + ["podloga"] * 8 + ["sciana"],
    ["sciana"] + ["podloga"] * 16 + ["sciana"],
    ["sciana"] + ["podloga"] * 16 + ["sciana"],
    ["sciana"] * 18
]

miecz_x = 8 * rozmiar_kafelka
miecz_y = 7 * rozmiar_kafelka
miecz_szerokosc = 18
miecz_wysokosc = 18

drabina_x = 8 * rozmiar_kafelka
drabina_y = 4 * rozmiar_kafelka
drabina_szerokosc = 26
drabina_wysokosc = 42

wrog_psoglaw = {
    "x": 92 * rozmiar_kafelka,
    "y": 66 * rozmiar_kafelka,
    "szer": 34,
    "wys": 38,
    "kolor": ciemna_czerwien,
    "max_hp": 125,
    "hp": 125,
    "aktywny": False,
    "zyje": True,
    "predkosc": 2,
    "atak_cooldown": 0,
    "nazwa": "Psoglow Szpieg",
    "stan_ataku": "brak",
    "telegraph_timer": 0,
    "atak_rect": pygame.Rect(0, 0, 0, 0),
    "typ_ataku": None,
    "dymek_tekst": "",
    "dymek_timer": 0,
    "ogluszony_timer": 0,
    "upusc_klucz": True,
    "klucz_upuszczony": False,
    "pokonany": False,
    "po_walce_dialog": False
}

npc_wies = [
    {
        "imie": "Stary rybak",
        "x": 34 * rozmiar_kafelka,
        "y": 30 * rozmiar_kafelka,
        "start_x": 34 * rozmiar_kafelka,
        "start_y": 30 * rozmiar_kafelka,
        "szer": 26,
        "wys": 30,
        "kolor": (120, 90, 55),
        "dialogi": [
            "Na trakcie znow ktos znika po zmroku.",
            "Wiatrak to nie zwykly mlyn. To punkt obserwacyjny.",
            "Psoglowi schodza podobno z dalekiej osady na wschodzie."
        ],
        "tlo": ["Ryby biora gorzej, jak zlo chodzi po trakcie.", "Woda zna wiecej tajemnic niz ludzie."],
        "ruch": False,
        "timer_ruchu": 0,
        "kierunek": "stop",
        "zakres": 24
    },
    {
        "imie": "Kobieta z wioski",
        "x": 18 * rozmiar_kafelka,
        "y": 32 * rozmiar_kafelka,
        "start_x": 18 * rozmiar_kafelka,
        "start_y": 32 * rozmiar_kafelka,
        "szer": 26,
        "wys": 30,
        "kolor": (210, 100, 130),
        "dialogi": [
            "Jakub pilnuje porzadku, ale sam wszystkiego nie utrzyma.",
            "Jesli wiatrak padl, to znaczy, ze trakt jest otwarty dla zla.",
            "Slyszalam wycie od strony starej drogi."
        ],
        "tlo": ["Dzieci lepiej chowac przed noca.", "Wioska juz nie spi tak spokojnie jak dawniej."],
        "ruch": False,
        "timer_ruchu": 0,
        "kierunek": "stop",
        "zakres": 20
    },
    {
        "imie": "Chlopiec",
        "x": 25 * rozmiar_kafelka,
        "y": 28 * rozmiar_kafelka,
        "start_x": 25 * rozmiar_kafelka,
        "start_y": 28 * rozmiar_kafelka,
        "szer": 24,
        "wys": 28,
        "kolor": (70, 90, 210),
        "dialogi": [
            "Widzialem swiatla daleko na wschodzie!",
            "Kot Lubek boi sie wycia z traktu.",
            "Owce robia sie nerwowe przed noca."
        ],
        "tlo": ["Jak dorosne, tez pojde na trakt.", "W nocy wszystko brzmi glosniej."],
        "ruch": False,
        "timer_ruchu": 0,
        "kierunek": "stop",
        "zakres": 18
    }
]

psoglowi_npc = [
    {
        "imie": "Warczyciel",
        "x": 244 * rozmiar_kafelka,
        "y": 158 * rozmiar_kafelka,
        "start_x": 244 * rozmiar_kafelka,
        "start_y": 158 * rozmiar_kafelka,
        "szer": 28,
        "wys": 32,
        "kolor": (125, 50, 50),
        "dialogi": ["Grr-thak. Ruun varg.", "Krash toor. Nakh vel."],
        "tlo": ["Rakh... rakh...", "Vorr naakh..."],
        "kierunek": "stop",
        "timer_ruchu": 0,
        "zakres": 24
    },
    {
        "imie": "Szczerba",
        "x": 252 * rozmiar_kafelka,
        "y": 165 * rozmiar_kafelka,
        "start_x": 252 * rozmiar_kafelka,
        "start_y": 165 * rozmiar_kafelka,
        "szer": 28,
        "wys": 32,
        "kolor": (145, 60, 60),
        "dialogi": ["Vrakh zurr! Tolaak!", "Nekh zora... grath."],
        "tlo": ["Khrr...", "Tchakh..."],
        "kierunek": "stop",
        "timer_ruchu": 0,
        "zakres": 18
    },
    {
        "imie": "Szef Krwawego Pyska",
        "x": 247 * rozmiar_kafelka,
        "y": 157 * rozmiar_kafelka,
        "start_x": 247 * rozmiar_kafelka,
        "start_y": 157 * rozmiar_kafelka,
        "szer": 34,
        "wys": 38,
        "kolor": (95, 20, 20),
        "dialogi": [
            "Ja slyszec o tobie, czlowiek.",
            "Jesli Zora zyje, to wioska bedzie pamietac.",
            "Jesli Zora martwy, krew mowi glosniej od slow."
        ],
        "tlo": ["Grrr...", "Szef patrzy bez mrugania."],
        "kierunek": "stop",
        "timer_ruchu": 0,
        "zakres": 12
    }
]

zwierzeta = [
    {"typ": "owca", "x": 42 * rozmiar_kafelka, "y": 23 * rozmiar_kafelka, "szer": 26, "wys": 20, "imie": "Owca"},
    {"typ": "owca", "x": 44 * rozmiar_kafelka, "y": 24 * rozmiar_kafelka, "szer": 26, "wys": 20, "imie": "Owca"},
    {"typ": "owca", "x": 46 * rozmiar_kafelka, "y": 22 * rozmiar_kafelka, "szer": 26, "wys": 20, "imie": "Owca"},
    {"typ": "kura", "x": 20 * rozmiar_kafelka, "y": 18 * rozmiar_kafelka, "szer": 18, "wys": 18, "imie": "Kura"},
    {"typ": "kura", "x": 23 * rozmiar_kafelka, "y": 17 * rozmiar_kafelka, "szer": 18, "wys": 18, "imie": "Kura"},
    {"typ": "kura", "x": 26 * rozmiar_kafelka, "y": 19 * rozmiar_kafelka, "szer": 18, "wys": 18, "imie": "Kura"},
    {"typ": "kot", "x": 30 * rozmiar_kafelka, "y": 22 * rozmiar_kafelka, "szer": 22, "wys": 16, "imie": "Lubek"},
    {"typ": "kot", "x": 16 * rozmiar_kafelka, "y": 26 * rozmiar_kafelka, "szer": 22, "wys": 16, "imie": "Mruczek"}
]


def pokaz_komunikat(tekst):
    global komunikat_systemowy, komunikat_timer
    komunikat_systemowy = tekst
    komunikat_timer = 180


def wymagany_exp_na_poziom(nowy_poziom):
    return 60 + (nowy_poziom - 1) * 35


def dodaj_exp(ile):
    global exp, poziom, exp_do_nastepnego, gracz_max_hp, gracz_hp, koszt_ataku

    exp += ile
    pokaz_komunikat(f"+{ile} EXP")

    while exp >= exp_do_nastepnego:
        exp -= exp_do_nastepnego
        poziom += 1
        exp_do_nastepnego = wymagany_exp_na_poziom(poziom)
        gracz_max_hp += 8
        gracz_hp = gracz_max_hp
        if koszt_ataku > 8:
            koszt_ataku -= 1
        pokaz_komunikat(f"Awans na poziom {poziom}!")


def zapisz_gre():
    dane = {
        "lokacja": lokacja,
        "gracz_x": gracz_x,
        "gracz_y": gracz_y,
        "akt": akt,
        "nazwa_aktu": nazwa_aktu,
        "etap_fabuly": etap_fabuly,
        "sciezka_fabuly": sciezka_fabuly,
        "byd_punkty": byd_punkty,
        "tekst_zadania": tekst_zadania,
        "gracz_hp": gracz_hp,
        "poziom": poziom,
        "exp": exp,
        "exp_do_nastepnego": exp_do_nastepnego,
        "klucz_do_wiatraka": klucz_do_wiatraka,
        "wiatrak_otwarty": wiatrak_otwarty,
        "drewniany_miecz_posiadany": drewniany_miecz_posiadany,
        "drewniany_miecz_zalozony": drewniany_miecz_zalozony,
        "wrog_hp": wrog_psoglaw["hp"],
        "wrog_zyje": wrog_psoglaw["zyje"],
        "wrog_klucz_upuszczony": wrog_psoglaw["klucz_upuszczony"],
        "wrog_pokonany": wrog_psoglaw["pokonany"],
        "zora_ujawniony": zora_ujawniony,
        "wybor_zory_dokonany": wybor_zory_dokonany,
        "zora_oszczedzony": zora_oszczedzony,
        "zora_zabity": zora_zabity,
        "cialo_zory": cialo_zory,
        "cialo_zory_x": cialo_zory_x,
        "cialo_zory_y": cialo_zory_y,
        "czas_gry_ms": czas_gry_ms
    }

    with open(plik_zapisu, "w", encoding="utf-8") as plik:
        json.dump(dane, plik, ensure_ascii=False, indent=4)

    pokaz_komunikat("Gra zapisana.")


def wczytaj_gre():
    global lokacja, gracz_x, gracz_y, akt, nazwa_aktu, etap_fabuly
    global sciezka_fabuly, byd_punkty, tekst_zadania, gracz_hp, poziom, exp
    global exp_do_nastepnego, klucz_do_wiatraka, wiatrak_otwarty
    global drewniany_miecz_posiadany, drewniany_miecz_zalozony
    global zora_ujawniony, wybor_zory_dokonany, zora_oszczedzony, zora_zabity
    global cialo_zory, cialo_zory_x, cialo_zory_y, czas_gry_ms

    if not os.path.exists(plik_zapisu):
        pokaz_komunikat("Brak pliku zapisu.")
        return

    with open(plik_zapisu, "r", encoding="utf-8") as plik:
        dane = json.load(plik)

    lokacja = dane["lokacja"]
    gracz_x = dane["gracz_x"]
    gracz_y = dane["gracz_y"]
    akt = dane["akt"]
    nazwa_aktu = dane["nazwa_aktu"]
    etap_fabuly = dane["etap_fabuly"]
    sciezka_fabuly = dane["sciezka_fabuly"]
    byd_punkty = dane["byd_punkty"]
    tekst_zadania = dane["tekst_zadania"]
    gracz_hp = dane["gracz_hp"]
    poziom = dane["poziom"]
    exp = dane["exp"]
    exp_do_nastepnego = dane["exp_do_nastepnego"]
    klucz_do_wiatraka = dane["klucz_do_wiatraka"]
    wiatrak_otwarty = dane["wiatrak_otwarty"]
    drewniany_miecz_posiadany = dane["drewniany_miecz_posiadany"]
    drewniany_miecz_zalozony = dane["drewniany_miecz_zalozony"]
    wrog_psoglaw["hp"] = dane["wrog_hp"]
    wrog_psoglaw["zyje"] = dane["wrog_zyje"]
    wrog_psoglaw["klucz_upuszczony"] = dane["wrog_klucz_upuszczony"]
    wrog_psoglaw["pokonany"] = dane.get("wrog_pokonany", False)

    zora_ujawniony = dane.get("zora_ujawniony", False)
    wybor_zory_dokonany = dane.get("wybor_zory_dokonany", False)
    zora_oszczedzony = dane.get("zora_oszczedzony", False)
    zora_zabity = dane.get("zora_zabity", False)
    cialo_zory = dane.get("cialo_zory", False)
    cialo_zory_x = dane.get("cialo_zory_x", 0)
    cialo_zory_y = dane.get("cialo_zory_y", 0)
    czas_gry_ms = dane.get("czas_gry_ms", 0)

    if zora_ujawniony:
        wrog_psoglaw["nazwa"] = "Zora"

    if not wrog_psoglaw["zyje"]:
        wrog_psoglaw["aktywny"] = False

    pokaz_komunikat("Gra wczytana.")


def stworz_mape_zewnetrzna():
    mapa = []

    for y in range(mapa_wysokosc):
        wiersz = []
        for x in range(mapa_szerokosc):
            if x == 0 or y == 0 or x == mapa_szerokosc - 1 or y == mapa_wysokosc - 1:
                wiersz.append("woda")
            else:
                wiersz.append("trawa")
        mapa.append(wiersz)

    for y in range(35, mapa_wysokosc - 15):
        mapa[y][70] = "woda"
        mapa[y][71] = "woda"
        mapa[y][72] = "woda"

    for x in range(8, 110):
        mapa[25][x] = "sciezka"
        mapa[26][x] = "sciezka"

    for y in range(20, 70):
        mapa[y][86] = "sciezka"
        mapa[y][87] = "sciezka"

    for x in range(87, 235):
        mapa[70][x] = "sciezka"
        mapa[71][x] = "sciezka"

    for y in range(71, 155):
        mapa[y][236] = "sciezka"
        mapa[y][237] = "sciezka"

    for x in range(12, 18):
        for y in range(14, 17):
            mapa[y][x] = "dom"

    for x in range(24, 30):
        for y in range(16, 19):
            mapa[y][x] = "dom"

    for x in range(32, 38):
        for y in range(12, 15):
            mapa[y][x] = "dom"

    for x in range(85, 90):
        for y in range(58, 63):
            mapa[y][x] = "wiatrak"

    for x in range(40, 49):
        mapa[21][x] = "plot"
        mapa[26][x] = "plot"
    for y in range(21, 27):
        mapa[y][40] = "plot"
        mapa[y][48] = "plot"

    for x in range(235, 260):
        for y in range(150, 170):
            if x in [235, 236, 258, 259] or y in [150, 151, 168, 169]:
                mapa[y][x] = "plot_psy"
            else:
                mapa[y][x] = "ziemia_psy"

    for x in range(242, 247):
        for y in range(156, 160):
            mapa[y][x] = "dom_psy"

    for x in range(250, 255):
        for y in range(161, 165):
            mapa[y][x] = "dom_psy"

    return mapa


mapa = stworz_mape_zewnetrzna()


def pobierz_aktualna_mape():
    if lokacja == "dom":
        return mapa_dom
    if lokacja == "wiatrak":
        return mapa_wiatrak
    if lokacja == "wiatrak_gora":
        return mapa_wiatrak_gora
    return mapa


def podziel_tekst_na_linie(tekst, font_uzyty, maks_szerokosc):
    slowa = tekst.split()
    linie = []
    aktualna_linia = ""

    for slowo in slowa:
        test_linia = aktualna_linia + slowo + " "
        szer_tekstu, _ = font_uzyty.size(test_linia)

        if szer_tekstu <= maks_szerokosc:
            aktualna_linia = test_linia
        else:
            if aktualna_linia.strip():
                linie.append(aktualna_linia.strip())
            aktualna_linia = slowo + " "

    if aktualna_linia.strip():
        linie.append(aktualna_linia.strip())

    return linie


def rozpocznij_wybor(kontekst, opis, wybor1, wybor2):
    global pokaz_wybor, tekst_wyboru, opcja_1, opcja_2, wybor_kontekst, pokaz_dialog
    pokaz_wybor = True
    tekst_wyboru = opis
    opcja_1 = wybor1
    opcja_2 = wybor2
    wybor_kontekst = kontekst
    pokaz_dialog = False


def zakoncz_wybor():
    global pokaz_wybor, tekst_wyboru, opcja_1, opcja_2, wybor_kontekst
    pokaz_wybor = False
    tekst_wyboru = ""
    opcja_1 = ""
    opcja_2 = ""
    wybor_kontekst = None


def obsluz_wybor(numer_opcji):
    global etap_fabuly, tekst_zadania, tekst_dialogu, pokaz_dialog, byd_punkty
    global wybor_zory_dokonany, zora_oszczedzony, zora_zabity
    global zora_ucieczka_timer, zora_migniecie_timer, cialo_zory, cialo_zory_x, cialo_zory_y

    if wybor_kontekst == "decyzja_traktu":
        if numer_opcji == 1:
            byd_punkty += 2
            tekst_dialogu = "Jakub: To droga Byd. Odbij wiatrak sila i otworz znow trakt."
            pokaz_dialog = True
            etap_fabuly = 3
            tekst_zadania = "Zadanie: pokonaj Psoglowa Straznika przy wiatraku"
            wrog_psoglaw["aktywny"] = True
        elif numer_opcji == 2:
            byd_punkty += 1
            tekst_dialogu = "Jakub: Podejdz ostroznie, ale wiatrak i tak musi zostac odzyskany."
            pokaz_dialog = True
            etap_fabuly = 3
            tekst_zadania = "Zadanie: pokonaj Psoglowa Straznika przy wiatraku"
            wrog_psoglaw["aktywny"] = True

    elif wybor_kontekst == "los_zory":
        wybor_zory_dokonany = True

        if numer_opcji == 1:
            zora_zabity = True
            zora_oszczedzony = False
            cialo_zory = True
            cialo_zory_x = wrog_psoglaw["x"]
            cialo_zory_y = wrog_psoglaw["y"]
            tekst_dialogu = "Zora osuwa sie na ziemie. Wioska Psoglowych kiedys sie o tym dowie."
            pokaz_dialog = True
            etap_fabuly = 5
            tekst_zadania = "Zadanie: rusz dalej traktem i odnajdz wioske Psoglowych"
            wrog_psoglaw["zyje"] = False
            wrog_psoglaw["aktywny"] = False

        elif numer_opcji == 2:
            zora_oszczedzony = True
            zora_zabity = False
            tekst_dialogu = "Zora warczy cicho: Dobra walka... czlowieku. Zapamietam cie."
            pokaz_dialog = True
            etap_fabuly = 5
            tekst_zadania = "Zadanie: rusz dalej traktem i odnajdz wioske Psoglowych"
            zora_ucieczka_timer = 120
            zora_migniecie_timer = 18

    zakoncz_wybor()


def policz_kamere():
    aktualna_mapa = pobierz_aktualna_mape()
    max_szer = len(aktualna_mapa[0]) * rozmiar_kafelka
    max_wys = len(aktualna_mapa) * rozmiar_kafelka

    srodek_gracza_x = gracz_x + gracz_szerokosc // 2
    srodek_gracza_y = gracz_y + gracz_wysokosc // 2

    if max_szer <= szerokosc:
        kamera_x = -(szerokosc - max_szer) // 2
    else:
        kamera_x = srodek_gracza_x - szerokosc // 2
        kamera_x = max(0, min(kamera_x, max_szer - szerokosc))

    if max_wys <= wysokosc:
        kamera_y = -(wysokosc - max_wys) // 2
    else:
        kamera_y = srodek_gracza_y - wysokosc // 2
        kamera_y = max(0, min(kamera_y, max_wys - wysokosc))

    return kamera_x, kamera_y


def kolor_pola(pole):
    if pole == "trawa":
        return zielony
    if pole == "sciezka":
        return brazowy
    if pole == "woda":
        return niebieski
    if pole == "dom":
        return szary
    if pole == "wiatrak":
        return jasny_braz
    if pole == "sciana":
        return (85, 85, 85)
    if pole == "podloga":
        return piaskowy
    if pole == "wyjscie":
        return pomaranczowy
    if pole == "stol":
        return (120, 75, 45)
    if pole == "skrzynia":
        return (120, 80, 35)
    if pole == "miecz":
        return zolty
    if pole == "plot":
        return (95, 70, 40)
    if pole == "plot_psy":
        return (110, 45, 45)
    if pole == "ziemia_psy":
        return (120, 95, 85)
    if pole == "dom_psy":
        return (80, 35, 35)
    if pole == "drabina" or pole == "drabina_dol":
        return (170, 120, 70)
    if pole == "mechanizm":
        return (120, 120, 120)
    if pole == "lozko":
        return (120, 40, 40)
    return bialy


def rysuj_mape(kamera_x, kamera_y):
    aktualna_mapa = pobierz_aktualna_mape()

    start_kolumna = max(0, kamera_x // rozmiar_kafelka)
    koniec_kolumna = min(len(aktualna_mapa[0]), (kamera_x + szerokosc) // rozmiar_kafelka + 2)
    start_wiersz = max(0, kamera_y // rozmiar_kafelka)
    koniec_wiersz = min(len(aktualna_mapa), (kamera_y + wysokosc) // rozmiar_kafelka + 2)

    for numer_wiersza in range(start_wiersz, koniec_wiersz):
        for numer_kolumny in range(start_kolumna, koniec_kolumna):
            pole = aktualna_mapa[numer_wiersza][numer_kolumny]
            kolor = kolor_pola(pole)

            ekran_x = numer_kolumny * rozmiar_kafelka - kamera_x
            ekran_y = numer_wiersza * rozmiar_kafelka - kamera_y

            pygame.draw.rect(okno, kolor, (ekran_x, ekran_y, rozmiar_kafelka, rozmiar_kafelka))
            pygame.draw.rect(okno, czarny, (ekran_x, ekran_y, rozmiar_kafelka, rozmiar_kafelka), 1)


def czy_pole_blokuje(pole):
    return pole in ["woda", "dom", "sciana", "wiatrak", "stol", "skrzynia", "plot", "plot_psy", "dom_psy", "mechanizm",
                    "lozko"]


def rect_npc_koliduje(nowe_x, nowe_y, lista_postaci):
    prostokat_gracza = pygame.Rect(nowe_x, nowe_y, gracz_szerokosc, gracz_wysokosc)
    for postac in lista_postaci:
        rect_postaci = pygame.Rect(postac["x"], postac["y"], postac["szer"], postac["wys"])
        if prostokat_gracza.colliderect(rect_postaci):
            return True
    return False


def czy_mozna_wejsc(nowe_x, nowe_y):
    aktualna_mapa = pobierz_aktualna_mape()

    lewy = nowe_x
    prawy = nowe_x + gracz_szerokosc - 1
    gora = nowe_y
    dol = nowe_y + gracz_wysokosc - 1

    rogi = [(lewy, gora), (prawy, gora), (lewy, dol), (prawy, dol)]

    for x, y in rogi:
        kolumna = x // rozmiar_kafelka
        wiersz = y // rozmiar_kafelka

        if wiersz < 0 or kolumna < 0:
            return False
        if wiersz >= len(aktualna_mapa) or kolumna >= len(aktualna_mapa[wiersz]):
            return False

        pole = aktualna_mapa[wiersz][kolumna]
        if czy_pole_blokuje(pole):
            return False

    if lokacja == "zewnatrz":
        prostokat_gracza = pygame.Rect(nowe_x, nowe_y, gracz_szerokosc, gracz_wysokosc)

        for npc in npc_wies:
            prostokat_npc = pygame.Rect(npc["x"], npc["y"], npc["szer"], npc["wys"])
            if prostokat_gracza.colliderect(prostokat_npc):
                return False

        for npc in psoglowi_npc:
            prostokat_npc = pygame.Rect(npc["x"], npc["y"], npc["szer"], npc["wys"])
            if prostokat_gracza.colliderect(prostokat_npc):
                return False

        for zwierze in zwierzeta:
            prostokat_zwierzecia = pygame.Rect(zwierze["x"], zwierze["y"], zwierze["szer"], zwierze["wys"])
            if prostokat_gracza.colliderect(prostokat_zwierzecia):
                return False

        rect_jakub = pygame.Rect(jakub_x, jakub_y, jakub_szerokosc, jakub_wysokosc)
        rect_michal = pygame.Rect(michal_x, michal_y, michal_szerokosc, michal_wysokosc)
        if prostokat_gracza.colliderect(rect_jakub) or prostokat_gracza.colliderect(rect_michal):
            return False

        if wrog_psoglaw["aktywny"] and wrog_psoglaw["zyje"]:
            rect_wroga = pygame.Rect(wrog_psoglaw["x"], wrog_psoglaw["y"], wrog_psoglaw["szer"], wrog_psoglaw["wys"])
            if prostokat_gracza.colliderect(rect_wroga):
                return False

    return True


def czy_gracz_jest_blisko_postaci(postac_x, postac_y, postac_szer, postac_wys):
    if lokacja != "zewnatrz":
        return False
    prostokat_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    prostokat_postaci = pygame.Rect(postac_x, postac_y, postac_szer, postac_wys)
    return prostokat_gracza.colliderect(prostokat_postaci.inflate(60, 60))


def czy_gracz_jest_blisko_jakuba():
    return czy_gracz_jest_blisko_postaci(jakub_x, jakub_y, jakub_szerokosc, jakub_wysokosc)


def czy_gracz_jest_blisko_michala():
    return czy_gracz_jest_blisko_postaci(michal_x, michal_y, michal_szerokosc, michal_wysokosc)


def znajdz_bliskiego_npc():
    if lokacja != "zewnatrz":
        return None
    rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    for npc in npc_wies:
        rect_npc = pygame.Rect(npc["x"], npc["y"], npc["szer"], npc["wys"])
        if rect_gracza.colliderect(rect_npc.inflate(55, 55)):
            return npc
    for npc in psoglowi_npc:
        rect_npc = pygame.Rect(npc["x"], npc["y"], npc["szer"], npc["wys"])
        if rect_gracza.colliderect(rect_npc.inflate(55, 55)):
            return npc
    return None


def znajdz_bliskiego_kota():
    if lokacja != "zewnatrz":
        return None
    rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    for zwierze in zwierzeta:
        if zwierze["typ"] == "kot":
            rect_zwierzecia = pygame.Rect(zwierze["x"], zwierze["y"], zwierze["szer"], zwierze["wys"])
            if rect_gracza.colliderect(rect_zwierzecia.inflate(55, 55)):
                return zwierze
    return None


def czy_gracz_jest_przy_domku():
    if lokacja != "zewnatrz":
        return False
    rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    return rect_gracza.colliderect(dom_wejscie_rect.inflate(20, 20))


def czy_gracz_jest_przy_wiatraku():
    if lokacja != "zewnatrz":
        return False
    rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    return rect_gracza.colliderect(wiatrak_rect.inflate(30, 30))


def czy_gracz_jest_przy_mieczu():
    if lokacja != "wiatrak" or drewniany_miecz_posiadany:
        return False
    rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    rect_miecza = pygame.Rect(miecz_x, miecz_y, miecz_szerokosc, miecz_wysokosc)
    return rect_gracza.colliderect(rect_miecza.inflate(20, 20))


def czy_gracz_jest_przy_drabinie_dol():
    if lokacja != "wiatrak":
        return False
    rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    rect_drabiny = pygame.Rect(drabina_x, drabina_y, drabina_szerokosc, drabina_wysokosc)
    return rect_gracza.colliderect(rect_drabiny.inflate(18, 18))


def czy_gracz_jest_przy_drabinie_gora():
    if lokacja != "wiatrak_gora":
        return False
    rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    rect_drabiny = pygame.Rect(8 * rozmiar_kafelka, 6 * rozmiar_kafelka, 26, 42)
    return rect_gracza.colliderect(rect_drabiny.inflate(18, 18))


def czy_wystarczy_staminy(koszt):
    return stamina >= koszt


def zuzyj_stamine(ile):
    global stamina, regen_staminy_timer
    stamina -= ile
    if stamina < 0:
        stamina = 0
    regen_staminy_timer = 40


def regeneruj_stamine():
    global stamina, stamina_wyswietlana, regen_staminy_timer

    if regen_staminy_timer > 0:
        regen_staminy_timer -= 1
    else:
        if stamina < stamina_max:
            stamina += 0.5
            if stamina > stamina_max:
                stamina = stamina_max

    if stamina_wyswietlana < stamina:
        stamina_wyswietlana += 1.2
        if stamina_wyswietlana > stamina:
            stamina_wyswietlana = stamina
    elif stamina_wyswietlana > stamina:
        stamina_wyswietlana -= 2
        if stamina_wyswietlana < stamina:
            stamina_wyswietlana = stamina


def aktualizuj_pore_dnia(dt):
    global czas_gry_ms, pora_dnia, docelowa_ciemnosc, aktualna_ciemnosc, kolor_nakladki

    czas_gry_ms += dt
    faza = (czas_gry_ms // czas_cyklu_dzien_noc) % 2

    if faza == 0:
        pora_dnia = "Dzien"
        docelowa_ciemnosc = 0
        kolor_nakladki = (20, 30, 60)
    else:
        pora_dnia = "Noc"
        docelowa_ciemnosc = 120
        kolor_nakladki = (20, 30, 70)

    if aktualna_ciemnosc < docelowa_ciemnosc:
        aktualna_ciemnosc += 0.25 * (dt / 16.67)
        if aktualna_ciemnosc > docelowa_ciemnosc:
            aktualna_ciemnosc = docelowa_ciemnosc
    elif aktualna_ciemnosc > docelowa_ciemnosc:
        aktualna_ciemnosc -= 0.25 * (dt / 16.67)
        if aktualna_ciemnosc < docelowa_ciemnosc:
            aktualna_ciemnosc = docelowa_ciemnosc


def rysuj_nakladke_dnia_i_nocy():
    if aktualna_ciemnosc <= 1:
        return

    nakladka = pygame.Surface((szerokosc, wysokosc), pygame.SRCALPHA)
    nakladka.fill((kolor_nakladki[0], kolor_nakladki[1], kolor_nakladki[2], int(aktualna_ciemnosc)))
    okno.blit(nakladka, (0, 0))


def aktualizuj_prosty_ruch_npc(npc, blokada_rects=None):
    if blokada_rects is None:
        blokada_rects = []

    if npc["timer_ruchu"] > 0:
        npc["timer_ruchu"] -= 1
    else:
        npc["timer_ruchu"] = random.randint(20, 80)
        npc["kierunek"] = random.choice(["gora", "dol", "lewo", "prawo", "stop", "stop"])

    stare_x = npc["x"]
    stare_y = npc["y"]
    krok = 1

    if npc["kierunek"] == "gora":
        npc["y"] -= krok
    elif npc["kierunek"] == "dol":
        npc["y"] += krok
    elif npc["kierunek"] == "lewo":
        npc["x"] -= krok
    elif npc["kierunek"] == "prawo":
        npc["x"] += krok

    if abs(npc["x"] - npc["start_x"]) > npc["zakres"] or abs(npc["y"] - npc["start_y"]) > npc["zakres"]:
        npc["x"] = stare_x
        npc["y"] = stare_y
        npc["kierunek"] = "stop"

    rect_npc = pygame.Rect(npc["x"], npc["y"], npc["szer"], npc["wys"])

    for rect_blokady in blokada_rects:
        if rect_npc.colliderect(rect_blokady):
            npc["x"] = stare_x
            npc["y"] = stare_y
            npc["kierunek"] = "stop"
            break


def aktualizuj_tlo_postaci():
    global komunikat_systemowy

    if lokacja != "zewnatrz":
        return

    if random.randint(1, 240) == 1:
        wybor = random.choice(["jakub", "michal", "npc", "psoglow"])

        if wybor == "jakub":
            teksty = [
                "Jakub mruczy: Gdzie ja dalem te kryszta... eee... rozkazy?",
                "Jakub mamrocze: Powinienem powachac tylko jeden...",
                "Jakub gada do siebie o wrozkowych krysztalach."
            ]
            pokaz_komunikat(random.choice(teksty))

        elif wybor == "michal":
            teksty = [
                "Michal: Broda sama sie nie ogoli.",
                "Michal poprawia brzytwe i wzdycha.",
                "Michal: Kiedys tu bylo spokojniej."
            ]
            pokaz_komunikat(random.choice(teksty))

        elif wybor == "npc":
            losowy = random.choice(npc_wies)
            pokaz_komunikat(losowy["imie"] + ": " + random.choice(losowy["tlo"]))

        elif wybor == "psoglow" and etap_fabuly >= 5:
            losowy = random.choice(psoglowi_npc)
            pokaz_komunikat(losowy["imie"] + ": " + random.choice(losowy["tlo"]))


def aktualizuj_zwierzeta():
    for zwierze in zwierzeta:
        if random.randint(1, 90) == 1:
            kierunek = random.choice(["gora", "dol", "lewo", "prawo", "stop"])
            krok = 4

            stare_x = zwierze["x"]
            stare_y = zwierze["y"]

            if kierunek == "gora":
                zwierze["y"] -= krok
            elif kierunek == "dol":
                zwierze["y"] += krok
            elif kierunek == "lewo":
                zwierze["x"] -= krok
            elif kierunek == "prawo":
                zwierze["x"] += krok

            if zwierze["typ"] == "owca":
                if not (41 * rozmiar_kafelka <= zwierze["x"] <= 47 * rozmiar_kafelka and 22 * rozmiar_kafelka <=
                        zwierze["y"] <= 25 * rozmiar_kafelka):
                    zwierze["x"] = stare_x
                    zwierze["y"] = stare_y

            if zwierze["typ"] == "kura":
                if not (18 * rozmiar_kafelka <= zwierze["x"] <= 28 * rozmiar_kafelka and 16 * rozmiar_kafelka <=
                        zwierze["y"] <= 22 * rozmiar_kafelka):
                    zwierze["x"] = stare_x
                    zwierze["y"] = stare_y

            if zwierze["typ"] == "kot":
                if not (13 * rozmiar_kafelka <= zwierze["x"] <= 32 * rozmiar_kafelka and 18 * rozmiar_kafelka <=
                        zwierze["y"] <= 28 * rozmiar_kafelka):
                    zwierze["x"] = stare_x
                    zwierze["y"] = stare_y


def aktualizuj_npc():
    global jakub_x, jakub_y, michal_x, michal_y, zora_ucieczka_timer, zora_migniecie_timer

    if lokacja != "zewnatrz":
        return

    rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)

    jakub = {
        "x": jakub_x,
        "y": jakub_y,
        "start_x": 22 * rozmiar_kafelka,
        "start_y": 24 * rozmiar_kafelka,
        "szer": jakub_szerokosc,
        "wys": jakub_wysokosc,
        "kierunek": random.choice(["stop"]),
        "timer_ruchu": random.randint(10, 60),
        "zakres": 18
    }

    michal = {
        "x": michal_x,
        "y": michal_y,
        "start_x": 28 * rozmiar_kafelka,
        "start_y": 20 * rozmiar_kafelka,
        "szer": michal_szerokosc,
        "wys": michal_wysokosc,
        "kierunek": random.choice(["stop"]),
        "timer_ruchu": random.randint(10, 60),
        "zakres": 16
    }

    if random.randint(1, 50) == 1:
        kier = random.choice(["gora", "dol", "lewo", "prawo", "stop", "stop"])
        stare_x = jakub_x
        stare_y = jakub_y
        krok = 2
        if kier == "gora":
            jakub_y -= krok
        elif kier == "dol":
            jakub_y += krok
        elif kier == "lewo":
            jakub_x -= krok
        elif kier == "prawo":
            jakub_x += krok

        if abs(jakub_x - 22 * rozmiar_kafelka) > 22 or abs(jakub_y - 24 * rozmiar_kafelka) > 22:
            jakub_x = stare_x
            jakub_y = stare_y
        if pygame.Rect(jakub_x, jakub_y, jakub_szerokosc, jakub_wysokosc).colliderect(rect_gracza):
            jakub_x = stare_x
            jakub_y = stare_y

    if random.randint(1, 50) == 1:
        kier = random.choice(["gora", "dol", "lewo", "prawo", "stop", "stop"])
        stare_x = michal_x
        stare_y = michal_y
        krok = 2
        if kier == "gora":
            michal_y -= krok
        elif kier == "dol":
            michal_y += krok
        elif kier == "lewo":
            michal_x -= krok
        elif kier == "prawo":
            michal_x += krok

        if abs(michal_x - 28 * rozmiar_kafelka) > 22 or abs(michal_y - 20 * rozmiar_kafelka) > 22:
            michal_x = stare_x
            michal_y = stare_y
        if pygame.Rect(michal_x, michal_y, michal_szerokosc, michal_wysokosc).colliderect(rect_gracza):
            michal_x = stare_x
            michal_y = stare_y

    blokady = [
        pygame.Rect(jakub_x, jakub_y, jakub_szerokosc, jakub_wysokosc),
        pygame.Rect(michal_x, michal_y, michal_szerokosc, michal_wysokosc),
        rect_gracza
    ]

    for npc in npc_wies:
        aktualizuj_prosty_ruch_npc(npc, blokady)

    if etap_fabuly >= 5:
        for npc in psoglowi_npc:
            aktualizuj_prosty_ruch_npc(npc, [rect_gracza])

    if zora_ucieczka_timer > 0:
        zora_ucieczka_timer -= 1
        wrog_psoglaw["x"] += 3
        wrog_psoglaw["y"] -= 1

        if zora_migniecie_timer > 0:
            zora_migniecie_timer -= 1

        if zora_ucieczka_timer <= 0:
            wrog_psoglaw["aktywny"] = False
            wrog_psoglaw["zyje"] = False

    aktualizuj_tlo_postaci()


def rysuj_imie(imie, x, y, szerokosc_postaci, kamera_x, kamera_y):
    tekst = font_maly.render(imie, True, czarny)
    prostokat = tekst.get_rect(center=(x - kamera_x + szerokosc_postaci // 2, y - kamera_y - 12))
    okno.blit(tekst, prostokat)


def rysuj_owce(x, y):
    pygame.draw.ellipse(okno, bez_owcy, (x, y, 26, 18))
    pygame.draw.ellipse(okno, czarny, (x, y, 26, 18), 1)
    pygame.draw.circle(okno, ciemny_szary, (x + 22, y + 8), 6)
    pygame.draw.line(okno, czarny, (x + 5, y + 16), (x + 5, y + 22), 2)
    pygame.draw.line(okno, czarny, (x + 11, y + 16), (x + 11, y + 22), 2)
    pygame.draw.line(okno, czarny, (x + 17, y + 16), (x + 17, y + 22), 2)
    pygame.draw.line(okno, czarny, (x + 22, y + 16), (x + 22, y + 22), 2)


def rysuj_kure(x, y):
    pygame.draw.ellipse(okno, kremowy, (x, y + 3, 16, 12))
    pygame.draw.circle(okno, kremowy, (x + 13, y + 5), 5)
    pygame.draw.polygon(okno, czerwony, [(x + 11, y + 1), (x + 14, y - 3), (x + 16, y + 1)])
    pygame.draw.polygon(okno, zolty, [(x + 18, y + 5), (x + 22, y + 7), (x + 18, y + 9)])
    pygame.draw.polygon(okno, jasny_braz, [(x + 2, y + 5), (x - 2, y + 1), (x + 1, y + 9)])
    pygame.draw.line(okno, czarny, (x + 6, y + 14), (x + 6, y + 20), 2)
    pygame.draw.line(okno, czarny, (x + 11, y + 14), (x + 11, y + 20), 2)


def rysuj_kota(x, y):
    pygame.draw.ellipse(okno, kotowy, (x + 4, y + 5, 16, 10))
    pygame.draw.circle(okno, kotowy, (x + 18, y + 8), 5)
    pygame.draw.polygon(okno, kotowy, [(x + 15, y + 4), (x + 17, y), (x + 19, y + 4)])
    pygame.draw.polygon(okno, kotowy, [(x + 18, y + 4), (x + 20, y), (x + 22, y + 4)])
    pygame.draw.arc(okno, ciemny_kot, (x - 1, y + 3, 10, 14), 4.8, 1.8, 2)
    pygame.draw.circle(okno, czarny, (x + 20, y + 8), 1)
    pygame.draw.line(okno, czarny, (x + 8, y + 14), (x + 8, y + 18), 2)
    pygame.draw.line(okno, czarny, (x + 13, y + 14), (x + 13, y + 18), 2)


def rysuj_zwierzeta(kamera_x, kamera_y):
    if lokacja != "zewnatrz":
        return

    for zwierze in zwierzeta:
        x = zwierze["x"] - kamera_x
        y = zwierze["y"] - kamera_y

        if zwierze["typ"] == "owca":
            rysuj_owce(x, y)
        elif zwierze["typ"] == "kura":
            rysuj_kure(x, y)
        elif zwierze["typ"] == "kot":
            rysuj_kota(x, y)


def rysuj_domek_styl(x, y, szer, wys):
    pygame.draw.rect(okno, (166, 111, 74), (x, y + 14, szer, wys - 14))
    pygame.draw.rect(okno, czarny, (x, y + 14, szer, wys - 14), 2)
    pygame.draw.polygon(okno, (120, 55, 40), [(x - 4, y + 16), (x + szer // 2, y - 8), (x + szer + 4, y + 16)])
    pygame.draw.polygon(okno, czarny, [(x - 4, y + 16), (x + szer // 2, y - 8), (x + szer + 4, y + 16)], 2)
    pygame.draw.rect(okno, (90, 55, 25), (x + szer // 2 - 5, y + wys - 18, 10, 18))
    pygame.draw.rect(okno, (210, 240, 255), (x + 5, y + 22, 8, 8))
    pygame.draw.rect(okno, (210, 240, 255), (x + szer - 13, y + 22, 8, 8))


def rysuj_wiatrak_styl(x, y, szer, wys):
    pygame.draw.rect(okno, (175, 145, 105), (x + 8, y + 8, szer - 16, wys - 8))
    pygame.draw.rect(okno, czarny, (x + 8, y + 8, szer - 16, wys - 8), 2)
    pygame.draw.polygon(okno, (125, 70, 45), [(x + 4, y + 10), (x + szer // 2, y - 10), (x + szer - 4, y + 10)])
    pygame.draw.polygon(okno, czarny, [(x + 4, y + 10), (x + szer // 2, y - 10), (x + szer - 4, y + 10)], 2)

    srodek_x = x + szer // 2
    srodek_y = y + 18
    pygame.draw.circle(okno, ciemny_szary, (srodek_x, srodek_y), 5)

    pygame.draw.line(okno, jasny_szary, (srodek_x - 18, srodek_y), (srodek_x + 18, srodek_y), 3)
    pygame.draw.line(okno, jasny_szary, (srodek_x, srodek_y - 18), (srodek_x, srodek_y + 18), 3)
    pygame.draw.line(okno, jasny_szary, (srodek_x - 13, srodek_y - 13), (srodek_x + 13, srodek_y + 13), 2)
    pygame.draw.line(okno, jasny_szary, (srodek_x + 13, srodek_y - 13), (srodek_x - 13, srodek_y + 13), 2)


def rysuj_budynki_dekoracyjne(kamera_x, kamera_y):
    if lokacja != "zewnatrz":
        return

    domki = [
        (12 * rozmiar_kafelka, 14 * rozmiar_kafelka, 6 * rozmiar_kafelka, 3 * rozmiar_kafelka),
        (24 * rozmiar_kafelka, 16 * rozmiar_kafelka, 6 * rozmiar_kafelka, 3 * rozmiar_kafelka),
        (32 * rozmiar_kafelka, 12 * rozmiar_kafelka, 6 * rozmiar_kafelka, 3 * rozmiar_kafelka)
    ]

    for dx, dy, ds, dw in domki:
        rysuj_domek_styl(dx - kamera_x, dy - kamera_y, ds, dw)

    rysuj_wiatrak_styl(wiatrak_rect.x - kamera_x, wiatrak_rect.y - kamera_y, wiatrak_rect.width, wiatrak_rect.height)


def rysuj_npc(kamera_x, kamera_y):
    if lokacja != "zewnatrz":
        return

    pygame.draw.rect(okno, fioletowy, (jakub_x - kamera_x, jakub_y - kamera_y, jakub_szerokosc, jakub_wysokosc))
    pygame.draw.rect(okno, zolty, (michal_x - kamera_x, michal_y - kamera_y, michal_szerokosc, michal_wysokosc))
    rysuj_imie("Jakub", jakub_x, jakub_y, jakub_szerokosc, kamera_x, kamera_y)
    rysuj_imie("Michal", michal_x, michal_y, michal_szerokosc, kamera_x, kamera_y)

    for npc in npc_wies:
        pygame.draw.rect(okno, npc["kolor"], (npc["x"] - kamera_x, npc["y"] - kamera_y, npc["szer"], npc["wys"]))
        rysuj_imie(npc["imie"], npc["x"], npc["y"], npc["szer"], kamera_x, kamera_y)

    if etap_fabuly >= 5:
        for npc in psoglowi_npc:
            pygame.draw.rect(okno, npc["kolor"], (npc["x"] - kamera_x, npc["y"] - kamera_y, npc["szer"], npc["wys"]))
            rysuj_imie(npc["imie"], npc["x"], npc["y"], npc["szer"], kamera_x, kamera_y)


def rysuj_dymek(tekst, x, y, kamera_x, kamera_y):
    if tekst == "":
        return

    surf = font_dymek.render(tekst, True, czarny)
    padding_x = 10
    padding_y = 6
    szer = surf.get_width() + padding_x * 2
    wys = surf.get_height() + padding_y * 2

    rect = pygame.Rect(x - kamera_x - szer // 2, y - kamera_y - 54, szer, wys)
    pygame.draw.rect(okno, bialy, rect, border_radius=10)
    pygame.draw.rect(okno, czarny, rect, 2, border_radius=10)
    okno.blit(surf, (rect.x + padding_x, rect.y + padding_y))


def rysuj_pasek_hp_nad_postacia(x, y, szer, wys, hp, max_hp):
    ratio = hp / max_hp
    if ratio < 0:
        ratio = 0
    pygame.draw.rect(okno, ciemna_czerwien, (x, y, szer, wys))
    pygame.draw.rect(okno, zielony_hp, (x, y, int(szer * ratio), wys))
    pygame.draw.rect(okno, czarny, (x, y, szer, wys), 1)

def rozpocznij_perfect_block():
    global perfect_block_timer, perfect_block_cooldown, blok_aktywny, blok_timer, blok_cooldown

    if perfect_block_cooldown > 0:
        return
    if not czy_wystarczy_staminy(koszt_bloku):
        pokaz_komunikat("Brak staminy na blok.")
        return
    if czy_unik or pokaz_dialog or pokaz_wybor:
        return

    zuzyj_stamine(koszt_bloku)
    blok_aktywny = True
    blok_timer = 18
    blok_cooldown = 22
    perfect_block_timer = perfect_block_okno
    perfect_block_cooldown = 20


def rozpocznij_atak():
    global atak_aktywny, atak_timer, atak_rect, atak_cooldown, atak_trafil

    if atak_cooldown > 0 or pokaz_wybor or pokaz_dialog:
        return

    if not czy_wystarczy_staminy(koszt_ataku):
        pokaz_komunikat("Za malo staminy na atak.")
        return

    zuzyj_stamine(koszt_ataku)

    atak_aktywny = True
    atak_timer = 10
    atak_cooldown = 18
    atak_trafil = False

    zasieg = 36
    if drewniany_miecz_zalozony:
        zasieg = 48

    if ostatni_kierunek == "gora":
        atak_rect = pygame.Rect(gracz_x - 8, gracz_y - zasieg, 44, zasieg)
    elif ostatni_kierunek == "dol":
        atak_rect = pygame.Rect(gracz_x - 8, gracz_y + gracz_wysokosc, 44, zasieg)
    elif ostatni_kierunek == "lewo":
        atak_rect = pygame.Rect(gracz_x - zasieg, gracz_y - 8, zasieg, 44)
    else:
        atak_rect = pygame.Rect(gracz_x + gracz_szerokosc, gracz_y - 8, zasieg, 44)


def rozpocznij_blok():
    rozpocznij_perfect_block()


def rozpocznij_unik():
    global unik_timer, unik_cooldown, czy_unik, gracz_x, gracz_y

    if unik_cooldown > 0 or blok_aktywny or pokaz_dialog or pokaz_wybor:
        return

    if not czy_wystarczy_staminy(koszt_uniku):
        pokaz_komunikat("Za malo staminy na unik.")
        return

    zuzyj_stamine(koszt_uniku)

    czy_unik = True
    unik_timer = 10
    unik_cooldown = 34

    dystans_uniku = 56
    nowy_x = gracz_x
    nowy_y = gracz_y

    if ostatni_kierunek == "gora":
        nowy_y -= dystans_uniku
    elif ostatni_kierunek == "dol":
        nowy_y += dystans_uniku
    elif ostatni_kierunek == "lewo":
        nowy_x -= dystans_uniku
    else:
        nowy_x += dystans_uniku

    if czy_mozna_wejsc(nowy_x, nowy_y):
        gracz_x = nowy_x
        gracz_y = nowy_y


def aktualizuj_atak():
    global atak_aktywny, atak_timer, atak_cooldown, atak_trafil

    if atak_cooldown > 0:
        atak_cooldown -= 1

    if atak_aktywny:
        atak_timer -= 1

        if wrog_psoglaw["aktywny"] and wrog_psoglaw["zyje"] and not atak_trafil:
            rect_wroga = pygame.Rect(wrog_psoglaw["x"], wrog_psoglaw["y"], wrog_psoglaw["szer"], wrog_psoglaw["wys"])
            if atak_rect.colliderect(rect_wroga):
                obrazenia = 12
                if drewniany_miecz_zalozony:
                    obrazenia = 20
                wrog_psoglaw["hp"] -= obrazenia
                atak_trafil = True
                pokaz_komunikat("Trafiles przeciwnika.")

                if wrog_psoglaw["hp"] <= 0:
                    wrog_psoglaw["hp"] = 0
                    wrog_psoglaw["pokonany"] = True
                    wrog_psoglaw["aktywny"] = False
                    wrog_psoglaw["stan_ataku"] = "brak"
                    wrog_psoglaw["po_walce_dialog"] = True
                    dodaj_exp(45)

                    if wrog_psoglaw["upusc_klucz"] and not wrog_psoglaw["klucz_upuszczony"]:
                        wrog_psoglaw["klucz_upuszczony"] = True
                        wrog_psoglaw["drop_x"] = wrog_psoglaw["x"]
                        wrog_psoglaw["drop_y"] = wrog_psoglaw["y"]

        if atak_timer <= 0:
            atak_aktywny = False


def dystans_do_gracza():
    srodek_gracza_x = gracz_x + gracz_szerokosc // 2
    srodek_gracza_y = gracz_y + gracz_wysokosc // 2
    srodek_wroga_x = wrog_psoglaw["x"] + wrog_psoglaw["szer"] // 2
    srodek_wroga_y = wrog_psoglaw["y"] + wrog_psoglaw["wys"] // 2
    return math.hypot(srodek_gracza_x - srodek_wroga_x, srodek_gracza_y - srodek_wroga_y)


def wylicz_rect_ataku_wroga(typ_ataku):
    rozmiar = 60 if typ_ataku == "blokowalny" else 92

    dx = gracz_x - wrog_psoglaw["x"]
    dy = gracz_y - wrog_psoglaw["y"]

    if abs(dx) > abs(dy):
        if dx > 0:
            return pygame.Rect(wrog_psoglaw["x"] + wrog_psoglaw["szer"], wrog_psoglaw["y"] - 10, rozmiar, 56)
        return pygame.Rect(wrog_psoglaw["x"] - rozmiar, wrog_psoglaw["y"] - 10, rozmiar, 56)
    else:
        if dy > 0:
            return pygame.Rect(wrog_psoglaw["x"] - 10, wrog_psoglaw["y"] + wrog_psoglaw["wys"], 56, rozmiar)
        return pygame.Rect(wrog_psoglaw["x"] - 10, wrog_psoglaw["y"] - rozmiar, 56, rozmiar)


def zadaj_obrazenia_graczowi(typ_ataku):
    global gracz_hp, gracz_nie_dostaje_obrazen_timer

    rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)

    if not wrog_psoglaw["atak_rect"].colliderect(rect_gracza):
        return

    if czy_unik:
        pokaz_komunikat("Udany unik!")
        return

    if typ_ataku == "blokowalny":
        if perfect_block_timer > 0:
            pokaz_komunikat("PERFECT BLOCK!")
            wrog_psoglaw["ogluszony_timer"] = 55
            wrog_psoglaw["atak_cooldown"] = 70
            return

        if blok_aktywny:
            gracz_hp -= 3
            pokaz_komunikat("Zablokowales atak.")
        else:
            gracz_hp -= 14
            pokaz_komunikat("Psoglow trafil cie.")

    elif typ_ataku == "nieblokowalny":
        gracz_hp -= 28
        pokaz_komunikat("Czerwony atak trafia mocno!")

    if gracz_hp < 0:
        gracz_hp = 0

    gracz_nie_dostaje_obrazen_timer = 26


def aktualizuj_wroga():
    global pokaz_dialog, tekst_dialogu, zora_ujawniony

    if wrog_psoglaw["po_walce_dialog"] and not pokaz_wybor and not wybor_zory_dokonany:
        wrog_psoglaw["po_walce_dialog"] = False
        zora_ujawniony = True
        wrog_psoglaw["nazwa"] = "Zora"
        tekst_dialogu = "Psoglow dyszy ciezko. Jesli musisz wiedziec... nazywaja mnie Zora."
        pokaz_dialog = True
        return

    if not wrog_psoglaw["aktywny"] or not wrog_psoglaw["zyje"] or lokacja != "zewnatrz":
        return

    if wrog_psoglaw["ogluszony_timer"] > 0:
        wrog_psoglaw["ogluszony_timer"] -= 1
        return

    if wrog_psoglaw["atak_cooldown"] > 0:
        wrog_psoglaw["atak_cooldown"] -= 1

    if wrog_psoglaw["telegraph_timer"] > 0:
        wrog_psoglaw["telegraph_timer"] -= 1
        if wrog_psoglaw["telegraph_timer"] <= 0 and wrog_psoglaw["typ_ataku"] is not None:
            zadaj_obrazenia_graczowi(wrog_psoglaw["typ_ataku"])
            wrog_psoglaw["stan_ataku"] = "brak"
            wrog_psoglaw["typ_ataku"] = None
            wrog_psoglaw["atak_rect"] = pygame.Rect(0, 0, 0, 0)
            wrog_psoglaw["atak_cooldown"] = 42
        return

    dystans = dystans_do_gracza()

    if dystans < 320:
        dx = gracz_x - wrog_psoglaw["x"]
        dy = gracz_y - wrog_psoglaw["y"]

        if dystans > 70:
            if abs(dx) > abs(dy):
                krok_x = wrog_psoglaw["predkosc"] if dx > 0 else -wrog_psoglaw["predkosc"]
                nowy_x = wrog_psoglaw["x"] + krok_x
                rect_test = pygame.Rect(nowy_x, wrog_psoglaw["y"], wrog_psoglaw["szer"], wrog_psoglaw["wys"])
                rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
                if not rect_test.colliderect(rect_gracza):
                    wrog_psoglaw["x"] = nowy_x
            else:
                krok_y = wrog_psoglaw["predkosc"] if dy > 0 else -wrog_psoglaw["predkosc"]
                nowy_y = wrog_psoglaw["y"] + krok_y
                rect_test = pygame.Rect(wrog_psoglaw["x"], nowy_y, wrog_psoglaw["szer"], wrog_psoglaw["wys"])
                rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
                if not rect_test.colliderect(rect_gracza):
                    wrog_psoglaw["y"] = nowy_y

    if dystans < 95 and wrog_psoglaw["atak_cooldown"] <= 0:
        los = random.randint(1, 100)
        if los <= 65:
            wrog_psoglaw["typ_ataku"] = "blokowalny"
            wrog_psoglaw["telegraph_timer"] = 26
        else:
            wrog_psoglaw["typ_ataku"] = "nieblokowalny"
            wrog_psoglaw["telegraph_timer"] = 34

        wrog_psoglaw["atak_rect"] = wylicz_rect_ataku_wroga(wrog_psoglaw["typ_ataku"])
        wrog_psoglaw["stan_ataku"] = "telegraph"


def rysuj_wroga(kamera_x, kamera_y):
    if lokacja == "zewnatrz" and wrog_psoglaw["zyje"] and (wrog_psoglaw["aktywny"] or etap_fabuly >= 3):
        x = wrog_psoglaw["x"] - kamera_x
        y = wrog_psoglaw["y"] - kamera_y

        if zora_migniecie_timer <= 0 or (zora_migniecie_timer // 3) % 2 == 0:
            pygame.draw.rect(okno, wrog_psoglaw["kolor"], (x, y, wrog_psoglaw["szer"], wrog_psoglaw["wys"]))
            pygame.draw.circle(okno, czarny, (x + 20, y + 10), 4)
            pygame.draw.rect(okno, czarny, (x + 8, y + 22, 18, 4))
            pygame.draw.line(okno, czarny, (x + 5, y + 4), (x + 11, y - 4), 3)
            pygame.draw.line(okno, czarny, (x + 28, y + 4), (x + 22, y - 4), 3)

            rysuj_imie(wrog_psoglaw["nazwa"], wrog_psoglaw["x"], wrog_psoglaw["y"], wrog_psoglaw["szer"], kamera_x, kamera_y)
            rysuj_pasek_hp_nad_postacia(x, y - 20, 56, 7, max(0, wrog_psoglaw["hp"]), wrog_psoglaw["max_hp"])

    if wrog_psoglaw.get("klucz_upuszczony", False) and not klucz_do_wiatraka:
        x = wrog_psoglaw["drop_x"] - kamera_x
        y = wrog_psoglaw["drop_y"] - kamera_y
        pygame.draw.rect(okno, zolty, (x, y, 16, 10))
        pygame.draw.circle(okno, zolty, (x + 4, y + 5), 4)
        pygame.draw.circle(okno, czarny, (x + 4, y + 5), 2)
        pygame.draw.rect(okno, czarny, (x, y, 16, 10), 1)

    if cialo_zory:
        x = cialo_zory_x - kamera_x
        y = cialo_zory_y - kamera_y
        pygame.draw.ellipse(okno, (90, 40, 40), (x, y + 10, 42, 22))
        pygame.draw.line(okno, czarny, (x + 6, y + 24), (x - 3, y + 30), 3)
        pygame.draw.line(okno, czarny, (x + 35, y + 24), (x + 46, y + 30), 3)
        pygame.draw.line(okno, czarny, (x + 16, y + 15), (x + 6, y + 6), 3)
        pygame.draw.line(okno, czarny, (x + 25, y + 15), (x + 35, y + 6), 3)


def rysuj_telegraph_wroga(kamera_x, kamera_y):
    if wrog_psoglaw["stan_ataku"] == "telegraph":
        kolor = pomaranczowy if wrog_psoglaw["typ_ataku"] == "blokowalny" else czerwony
        pygame.draw.rect(okno, kolor, (
            wrog_psoglaw["atak_rect"].x - kamera_x,
            wrog_psoglaw["atak_rect"].y - kamera_y,
            wrog_psoglaw["atak_rect"].width,
            wrog_psoglaw["atak_rect"].height
        ), 3)


def rysuj_miecz_w_wiatraku(kamera_x, kamera_y):
    if lokacja == "wiatrak" and not drewniany_miecz_posiadany:
        x = miecz_x - kamera_x
        y = miecz_y - kamera_y
        pygame.draw.line(okno, ciemny_szary, (x + 9, y + 2), (x + 9, y + 18), 3)
        pygame.draw.line(okno, zolty, (x + 9, y + 2), (x + 9, y + 10), 4)
        pygame.draw.line(okno, brazowy, (x + 4, y + 14), (x + 14, y + 14), 3)


def rysuj_drabiny(kamera_x, kamera_y):
    if lokacja == "wiatrak":
        x = drabina_x - kamera_x
        y = drabina_y - kamera_y
        pygame.draw.line(okno, jasny_braz, (x, y), (x, y + 40), 4)
        pygame.draw.line(okno, jasny_braz, (x + 20, y), (x + 20, y + 40), 4)
        for i in range(5):
            pygame.draw.line(okno, jasny_braz, (x, y + i * 9), (x + 20, y + i * 9), 3)

    elif lokacja == "wiatrak_gora":
        x = 8 * rozmiar_kafelka - kamera_x
        y = 6 * rozmiar_kafelka - kamera_y

        pygame.draw.line(okno, jasny_braz, (x, y), (x, y + 40), 4)
        pygame.draw.line(okno, jasny_braz, (x + 20, y), (x + 20, y + 40), 4)
        for i in range(5):
            pygame.draw.line(okno, jasny_braz, (x, y + i * 9), (x + 20, y + i * 9), 3)

        mech_x = 6 * rozmiar_kafelka - kamera_x
        mech_y = 4 * rozmiar_kafelka - kamera_y
        pygame.draw.circle(okno, ciemny_szary, (mech_x + 80, mech_y + 48), 26)
        pygame.draw.circle(okno, jasny_szary, (mech_x + 80, mech_y + 48), 10)

        for offset in [(0, -24), (0, 24), (-24, 0), (24, 0), (-18, -18), (18, 18), (-18, 18), (18, -18)]:
            pygame.draw.line(
                okno,
                jasny_szary,
                (mech_x + 80, mech_y + 48),
                (mech_x + 80 + offset[0], mech_y + 48 + offset[1]),
                3
            )


    elif lokacja == "wiatrak_gora":

        if czy_gracz_jest_przy_drabinie_gora():
            lokacja = "wiatrak"

            gracz_x = 11 * rozmiar_kafelka

            gracz_y = 6 * rozmiar_kafelka

            pokaz_komunikat("Schodzisz na dol.")

            return
    x = 6 * rozmiar_kafelka - kamera_x
    y = 4 * rozmiar_kafelka - kamera_y

    pygame.draw.circle(okno, ciemny_szary, (x + 80, y + 48), 26)
    pygame.draw.circle(okno, jasny_szary, (x + 80, y + 48), 10)

    for offset in [(0, -24), (0, 24), (-24, 0), (24, 0), (-18, -18), (18, 18), (-18, 18), (18, -18)]:
        pygame.draw.line(okno, jasny_szary, (x + 80, y + 48), (x + 80 + offset[0], y + 48 + offset[1]), 3)


def rysuj_gracza(kamera_x, kamera_y):
    x = gracz_x - kamera_x
    y = gracz_y - kamera_y

    kolor_gracza = czerwony
    if czy_unik:
        kolor_gracza = blekit
    elif blok_aktywny:
        kolor_gracza = niebieski
    elif gracz_nie_dostaje_obrazen_timer > 0 and (gracz_nie_dostaje_obrazen_timer // 4) % 2 == 0:
        kolor_gracza = (255, 170, 170)

    pygame.draw.rect(okno, kolor_gracza, (x, y, gracz_szerokosc, gracz_wysokosc))
    pygame.draw.circle(okno, czarny, (x + 13, y + 8), 3)

    if drewniany_miecz_zalozony:
        if ostatni_kierunek == "prawo":
            pygame.draw.line(okno, zolty, (x + 26, y + 8), (x + 38, y + 8), 4)
            pygame.draw.line(okno, brazowy, (x + 24, y + 8), (x + 28, y + 8), 5)
        elif ostatni_kierunek == "lewo":
            pygame.draw.line(okno, zolty, (x - 12, y + 8), (x, y + 8), 4)
            pygame.draw.line(okno, brazowy, (x - 2, y + 8), (x + 2, y + 8), 5)
        elif ostatni_kierunek == "gora":
            pygame.draw.line(okno, zolty, (x + 20, y - 10), (x + 20, y + 2), 4)
            pygame.draw.line(okno, brazowy, (x + 20, y), (x + 20, y + 4), 5)
        else:
            pygame.draw.line(okno, zolty, (x + 20, y + 28), (x + 20, y + 40), 4)
            pygame.draw.line(okno, brazowy, (x + 20, y + 26), (x + 20, y + 30), 5)

    rysuj_imie("Lukasz", gracz_x, gracz_y, gracz_szerokosc, kamera_x, kamera_y)


def rysuj_atak(kamera_x, kamera_y):
    if atak_aktywny:
        pygame.draw.rect(okno, pomaranczowy, (
            atak_rect.x - kamera_x,
            atak_rect.y - kamera_y,
            atak_rect.width,
            atak_rect.height
        ), 2)


def rysuj_dialog():
    rect = pygame.Rect(25, wysokosc - 180, szerokosc - 50, 155)
    pygame.draw.rect(okno, jasny_szary, rect)
    pygame.draw.rect(okno, czarny, rect, 4)

    linie = podziel_tekst_na_linie(tekst_dialogu, font, szerokosc - 110)
    y = wysokosc - 160

    for linia in linie[:4]:
        tekst = font.render(linia, True, czarny)
        okno.blit(tekst, (45, y))
        y += 28

    pomoc = font_maly.render("ESC - zamknij dialog", True, ciemny_szary)
    okno.blit(pomoc, (szerokosc - 210, wysokosc - 45))


def rysuj_panel_wyboru():
    rect = pygame.Rect(140, 250, szerokosc - 280, 190)
    pygame.draw.rect(okno, jasny_szary, rect)
    pygame.draw.rect(okno, czarny, rect, 4)

    linie = podziel_tekst_na_linie(tekst_wyboru, font, szerokosc - 360)
    y = 272

    for linia in linie[:3]:
        tekst = font.render(linia, True, czarny)
        okno.blit(tekst, (165, y))
        y += 28

    t1 = font_wybor.render("1 - " + opcja_1, True, fioletowy)
    t2 = font_wybor.render("2 - " + opcja_2, True, fioletowy)
    okno.blit(t1, (165, 345))
    okno.blit(t2, (165, 378))


def rysuj_zadanie():
    szer_panelu = 430
    wys_panelu = 72

    if lokacja in ["wiatrak", "wiatrak_gora", "dom"]:
        szer_panelu = 360
        wys_panelu = 56

    panel = pygame.Surface((szer_panelu, wys_panelu), pygame.SRCALPHA)
    panel.fill((20, 20, 20, 120))

    okno.blit(panel, (12, 12))
    pygame.draw.rect(okno, (210, 210, 210), (12, 12, szer_panelu, wys_panelu), 1)

    if lokacja in ["wiatrak", "wiatrak_gora", "dom"]:
        tekst_aktu = font_maly.render(nazwa_aktu, True, (230, 230, 230))
        okno.blit(tekst_aktu, (24, 20))

        linie = podziel_tekst_na_linie(tekst_zadania, font_maly, szer_panelu - 30)
        y = 40
        for linia in linie[:1]:
            tekst = font_maly.render(linia, True, (220, 220, 220))
            okno.blit(tekst, (24, y))
    else:
        tekst_aktu = font_akt.render(nazwa_aktu, True, (235, 235, 235))
        okno.blit(tekst_aktu, (24, 18))

        linie = podziel_tekst_na_linie(tekst_zadania, font_maly, szer_panelu - 30)
        y = 46
        for linia in linie[:2]:
            tekst = font_maly.render(linia, True, (225, 225, 225))
            okno.blit(tekst, (24, y))
            y += 18


def rysuj_ministatus():
    panel = pygame.Rect(12, 118, 320, 212)
    pygame.draw.rect(okno, jasny_szary, panel)
    pygame.draw.rect(okno, czarny, panel, 3)

    teksty = [
        f"Poziom: {poziom}",
        f"EXP: {int(exp)}/{int(exp_do_nastepnego)}",
        f"Sciezka: {sciezka_fabuly}",
        f"Etap: {etap_fabuly}",
        f"Klucz do wiatraka: {'TAK' if klucz_do_wiatraka else 'NIE'}",
        f"Miecz: {'ZALOZONY' if drewniany_miecz_zalozony else 'BRAK'}",
        f"Pora dnia: {pora_dnia}",
        "SPACJA atak | CTRL blok | SHIFT unik"
    ]

    y = 132
    for tekst_linia in teksty:
        tekst = font_maly.render(tekst_linia, True, czarny)
        okno.blit(tekst, (24, y))
        y += 22


def rysuj_pasek_hp(x, y, szer, wys, hp, max_hp):
    ratio = hp / max_hp
    if ratio < 0:
        ratio = 0
    pygame.draw.rect(okno, ciemna_czerwien, (x, y, szer, wys))
    pygame.draw.rect(okno, zielony_hp, (x, y, int(szer * ratio), wys))
    pygame.draw.rect(okno, czarny, (x, y, szer, wys), 2)


def rysuj_pasek_staminy(x, y, szer, wys, stamina_now, stamina_max_now):
    ratio = stamina_now / stamina_max_now
    if ratio < 0:
        ratio = 0
    pygame.draw.rect(okno, ciemny_szary, (x, y, szer, wys))
    pygame.draw.rect(okno, zolty, (x, y, int(szer * ratio), wys))
    pygame.draw.rect(okno, czarny, (x, y, szer, wys), 2)


def rysuj_pasek_exp(x, y, szer, wys, exp_now, exp_max):
    ratio = exp_now / exp_max
    if ratio < 0:
        ratio = 0
    pygame.draw.rect(okno, ciemny_szary, (x, y, szer, wys))
    pygame.draw.rect(okno, fioletowy, (x, y, int(szer * ratio), wys))
    pygame.draw.rect(okno, czarny, (x, y, szer, wys), 2)


def rysuj_minimape():
    if lokacja != "zewnatrz":
        return

    mini_szer = 220
    mini_wys = 150
    mini_x = szerokosc - mini_szer - 15
    mini_y = 15

    panel = pygame.Rect(mini_x, mini_y, mini_szer, mini_wys)
    pygame.draw.rect(okno, (25, 25, 25), panel)
    pygame.draw.rect(okno, bialy, panel, 2)

    skala_x = mini_szer / szerokosc_swiata
    skala_y = mini_wys / wysokosc_swiata

    pygame.draw.rect(okno, zielony, (mini_x, mini_y, mini_szer, mini_wys))
    pygame.draw.rect(okno, niebieski, (mini_x + int(70 * rozmiar_kafelka * skala_x), mini_y + int(35 * rozmiar_kafelka * skala_y), int(3 * rozmiar_kafelka * skala_x), int((mapa_wysokosc - 50) * rozmiar_kafelka * skala_y)))
    pygame.draw.rect(okno, brazowy, (mini_x + int(8 * rozmiar_kafelka * skala_x), mini_y + int(25 * rozmiar_kafelka * skala_y), int(102 * rozmiar_kafelka * skala_x), int(2 * rozmiar_kafelka * skala_y)))
    pygame.draw.rect(okno, brazowy, (mini_x + int(87 * rozmiar_kafelka * skala_x), mini_y + int(70 * rozmiar_kafelka * skala_y), int(150 * rozmiar_kafelka * skala_x), int(2 * rozmiar_kafelka * skala_y)))

    pygame.draw.rect(okno, szary, (mini_x + int(dom_wejscie_rect.x * skala_x), mini_y + int(dom_wejscie_rect.y * skala_y), max(4, int(dom_wejscie_rect.width * skala_x)), max(4, int(dom_wejscie_rect.height * skala_y))))
    pygame.draw.rect(okno, jasny_braz, (mini_x + int(wiatrak_rect.x * skala_x), mini_y + int(wiatrak_rect.y * skala_y), max(5, int(wiatrak_rect.width * skala_x)), max(5, int(wiatrak_rect.height * skala_y))))
    pygame.draw.rect(okno, ciemna_czerwien, (mini_x + int(wioska_psoglowych_rect.x * skala_x), mini_y + int(wioska_psoglowych_rect.y * skala_y), max(10, int(wioska_psoglowych_rect.width * skala_x)), max(8, int(wioska_psoglowych_rect.height * skala_y))))

    px = mini_x + int(gracz_x * skala_x)
    py = mini_y + int(gracz_y * skala_y)
    pygame.draw.circle(okno, zolty, (px, py), 4)

    if wrog_psoglaw["zyje"]:
        wx = mini_x + int(wrog_psoglaw["x"] * skala_x)
        wy = mini_y + int(wrog_psoglaw["y"] * skala_y)
        pygame.draw.circle(okno, czerwony, (wx, wy), 3)

    t = font_maly.render("MINIMAPA", True, bialy)
    okno.blit(t, (mini_x + 8, mini_y + 6))

    def rysuj_podpowiedz():
        tekst_podpowiedzi = None

        if pokaz_dialog or pokaz_wybor:
            return

        if lokacja == "zewnatrz":
            if czy_gracz_jest_blisko_jakuba():
                tekst_podpowiedzi = "E - rozmawiaj z Jakubem"
            elif czy_gracz_jest_blisko_michala():
                tekst_podpowiedzi = "E - rozmawiaj z Michalem"
            elif znajdz_bliskiego_npc() is not None:
                tekst_podpowiedzi = "E - rozmawiaj"
            elif znajdz_bliskiego_kota() is not None:
                tekst_podpowiedzi = "E - poglaskaj kota"
            elif czy_gracz_jest_przy_domku():
                tekst_podpowiedzi = "E - wejdz do domu"
            elif czy_gracz_jest_przy_wiatraku() and not klucz_do_wiatraka and not wrog_psoglaw[
                "zyje"] and wrog_psoglaw.get("klucz_upuszczony", False):
                tekst_podpowiedzi = "E - podnies klucz"
            elif czy_gracz_jest_przy_wiatraku() and klucz_do_wiatraka:
                tekst_podpowiedzi = "E - wejdz do wiatraka"
            elif etap_fabuly == 3 and wrog_psoglaw["zyje"] and dystans_do_gracza() < 140:
                tekst_podpowiedzi = "SPACJA - atak | CTRL - blok | SHIFT - unik"

        elif lokacja == "dom":
            aktualna_mapa = pobierz_aktualna_mape()
            kolumna = (gracz_x + gracz_szerokosc // 2) // rozmiar_kafelka
            wiersz = (gracz_y + gracz_wysokosc // 2) // rozmiar_kafelka
            if aktualna_mapa[wiersz][kolumna] == "wyjscie":
                tekst_podpowiedzi = "E - wyjdz"

        elif lokacja == "wiatrak":
            if czy_gracz_jest_przy_mieczu():
                tekst_podpowiedzi = "E - podnies drewniany miecz"
            elif czy_gracz_jest_przy_drabinie_dol():
                tekst_podpowiedzi = "E - wejdz na gore"
            else:
                aktualna_mapa = pobierz_aktualna_mape()
                kolumna = (gracz_x + gracz_szerokosc // 2) // rozmiar_kafelka
                wiersz = (gracz_y + gracz_wysokosc // 2) // rozmiar_kafelka
                if aktualna_mapa[wiersz][kolumna] == "wyjscie":
                    tekst_podpowiedzi = "E - wyjdz z wiatraka"

        elif lokacja == "wiatrak_gora":
            if czy_gracz_jest_przy_drabinie_gora():
                tekst_podpowiedzi = "E - zejdz na dol"

        if tekst_podpowiedzi is not None:
            surf = font_maly.render(tekst_podpowiedzi, True, bialy)
            panel = pygame.Surface((surf.get_width() + 20, 30), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 140))
            x = szerokosc // 2 - panel.get_width() // 2
            y = wysokosc - 210
            okno.blit(panel, (x, y))
            okno.blit(surf, (x + 10, y + 6))

        elif czy_gracz_jest_przy_wiatraku() and k
        y = wysokosc - 210
        okno.blit(panel, (x, y))
        okno.blit(surf, (x + 10, y + 6))

    tedef rysuj_podpowiedz():kst_podpowiedzi = None

    if pokaz_dialog or pokaz_wybor:
        return

    if lokacja == "zewnatrz":
        if czy_gracz_jest_blisko_jakuba():
            tekst_podpowiedzi = "E - rozmawiaj z Jakubem"
        elif czy_gracz_jest_blisko_michala():
            tekst_podpowiedzi = "E - rozmawiaj z Michalem"
        elif znajdz_bliskiego_npc() is not None:
            tekst_podpowiedzi = "E - rozmawiaj"
        elif znajdz_bliskiego_kota() is not None:
            tekst_podpowiedzi = "E - poglaskaj kota"
        elif czy_gracz_jest_przy_domku():
            tekst_podpowiedzi = "E - wejdz do domu"
        elif czy_gracz_jest_przy_wiatraku() and klucz_do_wiatraka:
            tekst_podpowiedzi = "E - wejdz do wiatraka"
        elif czy_gracz_jest_przy_wiatraku() and not klucz_do_wiatraka:
            tekst_podpowiedzi = "Wiatrak zamkniety"

    elif lokacja == "dom":
        aktualna_mapa = pobierz_aktualna_mape()
        kolumna = (gracz_x + gracz_szerokosc // 2) // rozmiar_kafelka
        wiersz = (gracz_y + gracz_wysokosc // 2) // rozmiar_kafelka
        if aktualna_mapa[wiersz][kolumna] == "wyjscie":
            tekst_podpowiedzi = "E - wyjdz"

    elif lokacja == "wiatrak":
        if czy_gracz_jest_przy_mieczu():
            tekst_podpowiedzi = "E - podnies miecz"
        elif czy_gracz_jest_przy_drabinie_dol():
            tekst_podpowiedzi = "E - wejdz po drabinie"
        else:
            aktualna_mapa = pobierz_aktualna_mape()
            kolumna = (gracz_x + gracz_szerokosc // 2) // rozmiar_kafelka
            wiersz = (gracz_y + gracz_wysokosc // 2) // rozmiar_kafelka
            if aktualna_mapa[wiersz][kolumna] == "wyjscie":
                tekst_podpowiedzi = "E - wyjdz z wiatraka"

    elif lokacja == "wiatrak_gora":
        if czy_gracz_jest_przy_drabinie_gora():
            tekst_podpowiedzi = "E - zejdz na dol"

    if tekst_podpowiedzi is not None:
        surf = font_maly.render(tekst_podpowiedzi, True, bialy)
        panel = pygame.Surface((surf.get_width() + 20, 30), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 140))
        x = szerokosc // 2 - panel.get_width() // 2
        y = wysokosc - 210
        okno.blit(panel, (x, y))
        okno.blit(surf, (x + 10, y + 6))


def obsluz_interakcje():
    global lokacja, gracz_x, gracz_y, tekst_dialogu, pokaz_dialog
    global etap_fabuly, tekst_zadania, klucz_do_wiatraka, wiatrak_otwarty
    global drewniany_miecz_posiadany, drewniany_miecz_zalozony

    if lokacja == "zewnatrz":
        if czy_gracz_jest_blisko_jakuba():
            if etap_fabuly == 0:
                tekst_dialogu = "Jakub: Jestem zastepca wodza... chyba. Trakt zly. Wiatrak zajety. A krysz... niewazne."
                pokaz_dialog = True
                etap_fabuly = 1
                tekst_zadania = "Zadanie: porozmawiaj jeszcze z Michalem"
            else:
                teksty = [
                    "Jakub: Zastepca wodza musi myslec. Nawet jak mysli bokiem.",
                    "Jakub: Wrozkowe krysztaly pachna jak decyzje.",
                    "Jakub: Pilnuj traktu. Ja pilnuje... no, pilnuje."
                ]
                tekst_dialogu = random.choice(teksty)
                pokaz_dialog = True
            return

        if czy_gracz_jest_blisko_michala():
            if etap_fabuly == 1:
                tekst_dialogu = "Michal: Jestem golibroda, nie woj. Ale Jakub ma racje - odbij wiatrak."
                pokaz_dialog = True
                etap_fabuly = 2
                tekst_zadania = "Zadanie: zdecyduj jak podejsc do odzyskania wiatraka"
                return
            else:
                teksty = [
                    "Michal: Broda i ostrze wymagaja pewnej reki.",
                    "Michal: Jakub znow gada do siebie?",
                    "Michal: Nie zapuszczaj brody jak Psoglow."
                ]
                tekst_dialogu = random.choice(teksty)
                pokaz_dialog = True
                return

        bliski_npc = znajdz_bliskiego_npc()
        if bliski_npc is not None:
            if bliski_npc["imie"] == "Szef Krwawego Pyska":
                if zora_oszczedzony:
                    tekst_dialogu = "Szef Krwawego Pyska: Zora zyje. To znaczy, ze umiesz wstrzymac reke."
                elif zora_zabity:
                    tekst_dialogu = "Szef Krwawego Pyska: Zabiles Zore. Krew nie znika z ziemi szybko."
                else:
                    tekst_dialogu = random.choice(bliski_npc["dialogi"])
            else:
                tekst_dialogu = random.choice(bliski_npc["dialogi"])
            pokaz_dialog = True
            return

        bliski_kot = znajdz_bliskiego_kota()
        if bliski_kot is not None:
            tekst_dialogu = f"{bliski_kot['imie']} mruczy z zadowoleniem."
            pokaz_dialog = True
            return

        if czy_gracz_jest_przy_domku():
            lokacja = "dom"
            gracz_x = 10 * rozmiar_kafelka
            gracz_y = 8 * rozmiar_kafelka
            pokaz_komunikat("Wchodzisz do domu.")
            return

        if czy_gracz_jest_przy_wiatraku() and not klucz_do_wiatraka and not wrog_psoglaw["zyje"] and wrog_psoglaw.get(
                "klucz_upuszczony", False):
            klucz_do_wiatraka = True
            wrog_psoglaw["klucz_upuszczony"] = False
            pokaz_komunikat("Podnosisz klucz do wiatraka.")
            return

        if czy_gracz_jest_przy_wiatraku() and klucz_do_wiatraka:
            lokacja = "wiatrak"
            gracz_x = 8 * rozmiar_kafelka
            gracz_y = 7 * rozmiar_kafelka
            wiatrak_otwarty = True
            pokaz_komunikat("Wchodzisz do wiatraka.")
            return

    elif lokacja == "dom":
        aktualna_mapa = pobierz_aktualna_mape()
        kolumna = (gracz_x + gracz_szerokosc // 2) // rozmiar_kafelka
        wiersz = (gracz_y + gracz_wysokosc // 2) // rozmiar_kafelka
        if aktualna_mapa[wiersz][kolumna] == "wyjscie":
            lokacja = "zewnatrz"
            gracz_x = 16 * rozmiar_kafelka
            gracz_y = 18 * rozmiar_kafelka
            pokaz_komunikat("Wychodzisz z domu.")
            return

    elif lokacja == "wiatrak":
        if czy_gracz_jest_przy_mieczu():
            drewniany_miecz_posiadany = True
            drewniany_miecz_zalozony = True
            pokaz_komunikat("Zdobyto drewniany miecz.")
            return

        if czy_gracz_jest_przy_drabinie_dol():
            lokacja = "wiatrak_gora"
            gracz_x = 8 * rozmiar_kafelka
            gracz_y = 7 * rozmiar_kafelka
            pokaz_komunikat("Wchodzisz na gore wiatraka.")
            return

        aktualna_mapa = pobierz_aktualna_mape()
        kolumna = (gracz_x + gracz_szerokosc // 2) // rozmiar_kafelka
        wiersz = (gracz_y + gracz_wysokosc // 2) // rozmiar_kafelka
        if aktualna_mapa[wiersz][kolumna] == "wyjscie":
            lokacja = "zewnatrz"
            gracz_x = 86 * rozmiar_kafelka
            gracz_y = 64 * rozmiar_kafelka
            pokaz_komunikat("Wychodzisz z wiatraka.")
            return

    elif lokacja == "wiatrak_gora":
        if czy_gracz_jest_przy_drabinie_gora():
            lokacja = "wiatrak"
            gracz_x = 8 * rozmiar_kafelka
            gracz_y = 5 * rozmiar_kafelka
            pokaz_komunikat("Schodzisz na dol.")
            return


uruchomiona = True

while uruchomiona:
    dt = zegar.tick(60)

    if komunikat_timer > 0:
        komunikat_timer -= 1

    if perfect_block_timer > 0:
        perfect_block_timer -= 1
    if perfect_block_cooldown > 0:
        perfect_block_cooldown -= 1

    if blok_timer > 0:
        blok_timer -= 1
    else:
        blok_aktywny = False

    if blok_cooldown > 0:
        blok_cooldown -= 1

    if unik_timer > 0:
        unik_timer -= 1
    else:
        czy_unik = False

    if unik_cooldown > 0:
        unik_cooldown -= 1

    if gracz_nie_dostaje_obrazen_timer > 0:
        gracz_nie_dostaje_obrazen_timer -= 1

    aktualizuj_pore_dnia(dt)
    regeneruj_stamine()
    aktualizuj_atak()
    aktualizuj_wroga()
    aktualizuj_zwierzeta()
    aktualizuj_npc()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            uruchomiona = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if pokaz_dialog:
                    pokaz_dialog = False

                    if zora_ujawniony and wrog_psoglaw["pokonany"] and not wybor_zory_dokonany:
                        rozpocznij_wybor(
                            "los_zory",
                            "Pokonales Psoglowa Szpiega. Zora ledwo oddycha. Co robisz?",
                            "Dobij Zore",
                            "Pusc Zore wolno"
                        )
                elif pokaz_wybor:
                    zakoncz_wybor()
                else:
                    uruchomiona = False

            elif event.key == pygame.K_e:
                if not pokaz_dialog and not pokaz_wybor:
                    obsluz_interakcje()

            elif event.key == pygame.K_1 and pokaz_wybor:
                obsluz_wybor(1)

            elif event.key == pygame.K_2 and pokaz_wybor:
                obsluz_wybor(2)

            elif event.key == pygame.K_SPACE:
                if not pokaz_dialog and not pokaz_wybor:
                    rozpocznij_atak()

            elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                if not pokaz_dialog and not pokaz_wybor:
                    rozpocznij_blok()

            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                if not pokaz_dialog and not pokaz_wybor:
                    rozpocznij_unik()

            elif event.key == pygame.K_F5:
                zapisz_gre()

            elif event.key == pygame.K_F9:
                wczytaj_gre()

            elif event.key == pygame.K_TAB:
                if drewniany_miecz_posiadany:
                    drewniany_miecz_zalozony = not drewniany_miecz_zalozony
                    pokaz_komunikat("Przelaczono bron.")

    if not pokaz_dialog and not pokaz_wybor:
        klawisze = pygame.key.get_pressed()
        nowy_x = gracz_x
        nowy_y = gracz_y

        if klawisze[pygame.K_w] or klawisze[pygame.K_UP]:
            nowy_y -= predkosc
            ostatni_kierunek = "gora"
        if klawisze[pygame.K_s] or klawisze[pygame.K_DOWN]:
            nowy_y += predkosc
            ostatni_kierunek = "dol"
        if klawisze[pygame.K_a] or klawisze[pygame.K_LEFT]:
            nowy_x -= predkosc
            ostatni_kierunek = "lewo"
        if klawisze[pygame.K_d] or klawisze[pygame.K_RIGHT]:
            nowy_x += predkosc
            ostatni_kierunek = "prawo"

        if czy_mozna_wejsc(nowy_x, gracz_y):
            gracz_x = nowy_x
        if czy_mozna_wejsc(gracz_x, nowy_y):
            gracz_y = nowy_y

        if etap_fabuly == 2:
            rozpocznij_wybor(
                "decyzja_traktu",
                "Jak chcesz podejsc do odzyskania wiatraka?",
                "Droga sily",
                "Podejscie ostrozne"
            )

    kamera_x, kamera_y = policz_kamere()

    okno.fill(czarny)
    rysuj_mape(kamera_x, kamera_y)
    rysuj_budynki_dekoracyjne(kamera_x, kamera_y)
    rysuj_zwierzeta(kamera_x, kamera_y)
    rysuj_npc(kamera_x, kamera_y)
    rysuj_wroga(kamera_x, kamera_y)
    rysuj_telegraph_wroga(kamera_x, kamera_y)
    rysuj_miecz_w_wiatraku(kamera_x, kamera_y)
    rysuj_drabiny(kamera_x, kamera_y)
    rysuj_mechanizm_wiatraka(kamera_x, kamera_y)
    rysuj_gracza(kamera_x, kamera_y)
    rysuj_atak(kamera_x, kamera_y)

    rysuj_nakladke_dnia_i_nocy()

    rysuj_zadanie()
    rysuj_ministatus()
    rysuj_pasek_hp(12, 340, 220, 20, gracz_hp, gracz_max_hp)
    rysuj_pasek_staminy(12, 366, 220, 16, stamina_wyswietlana, stamina_max)
    rysuj_pasek_exp(12, 388, 220, 12, exp, exp_do_nastepnego)
    rysuj_minimape()


    def rysuj_podpowiedz():
        tekst_podpowiedzi = None

        if lokacja == "zewnatrz":
            if czy_gracz_jest_blisko_jakuba() or czy_gracz_jest_blisko_michala():
                tekst_podpowiedzi = "Nacisnij E"

            elif znajdz_bliskiego_npc() is not None:
                tekst_podpowiedzi = "Nacisnij E, aby porozmawiac"

            elif znajdz_bliskiego_kota() is not None:
                tekst_podpowiedzi = "Nacisnij E, aby poglaskac kota"

            elif czy_gracz_jest_przy_wiatraku() and not klucz_do_wiatraka and not wrog_psoglaw[
                "zyje"] and wrog_psoglaw.get("klucz_upuszczony", False):
                tekst_podpowiedzi = "Nacisnij E, aby podniesc klucz"

            elif czy_gracz_jest_przy_domku():
                tekst_podpowiedzi = "Nacisnij E, aby wejsc do domu"

            elif czy_gracz_jest_przy_wiatraku() and klucz_do_wiatraka:
                tekst_podpowiedzi = "Nacisnij E, aby wejsc do wiatraka"

            elif etap_fabuly >= 3 and wrog_psoglaw["zyje"] and dystans_do_gracza() < 140:
                tekst_podpowiedzi = "SPACJA atak | CTRL blok | SHIFT unik"

        elif lokacja == "dom":
            tekst_podpowiedzi = "Nacisnij E na wyjsciu"

        elif lokacja == "wiatrak":
            if czy_gracz_jest_przy_mieczu():
                tekst_podpowiedzi = "Nacisnij E, aby podniesc drewniany miecz"
            elif czy_gracz_jest_przy_drabinie_dol():
                tekst_podpowiedzi = "Nacisnij E, aby wejsc na gore"
            else:
                tekst_podpowiedzi = "Nacisnij E na wyjsciu"

        elif lokacja == "wiatrak_gora":
            if czy_gracz_jest_przy_drabinie_gora():
                tekst_podpowiedzi = "Nacisnij E, aby zejsc na dol"

        if tekst_podpowiedzi is not None:
            surf = font_maly.render(tekst_podpowiedzi, True, bialy)
            panel = pygame.Surface((surf.get_width() + 20, 30), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 140))
            x = szerokosc // 2 - panel.get_width() // 2
            y = wysokosc - 210
            okno.blit(panel, (x, y))
            okno.blit(surf, (x + 10, y + 6))


    hp_tekst = font_bardzo_maly.render("HP", True, bialy)
    st_tekst = font_bardzo_maly.render("ST", True, bialy)
    exp_tekst = font_bardzo_maly.render("EXP", True, bialy)
    okno.blit(hp_tekst, (238, 340))
    okno.blit(st_tekst, (238, 364))
    okno.blit(exp_tekst, (238, 384))

    if komunikat_timer > 0:
        panel = pygame.Surface((640, 34), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 140))
        okno.blit(panel, (szerokosc // 2 - 320, wysokosc - 28))
        tekst = font_maly.render(komunikat_systemowy, True, bialy)
        okno.blit(tekst, (szerokosc // 2 - tekst.get_width() // 2, wysokosc - 22))

    if pokaz_dialog:
        rysuj_dialog()

    if pokaz_wybor:
        rysuj_panel_wyboru()

    pygame.display.flip()

pygame.quit()