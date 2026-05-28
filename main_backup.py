import pygame
import random
import json
import os
import math

pygame.init()

szerokosc = 800
wysokosc = 600
okno = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption("Przygoda Łukasza - Ścieżka Byd")

bialy = (255, 255, 255)
zielony = (34, 177, 76)
brazowy = (185, 122, 87)
jasny_braz = (205, 170, 125)
niebieski = (0, 162, 232)
czarny = (0, 0, 0)
szary = (120, 120, 120)
jasny_szary = (245, 245, 245)
ciemny_szary = (60, 60, 60)
czerwony = (255, 0, 0)
ciemna_czerwien = (170, 0, 0)
fioletowy = (163, 73, 164)
zolty = (255, 201, 14)
pomaranczowy = (255, 140, 0)
zielony_hp = (0, 200, 0)
nieco_zloty = (230, 190, 60)
blekit = (120, 200, 255)

rozmiar_kafelka = 40

mapa_szerokosc = 120
mapa_wysokosc = 90

szerokosc_swiata = mapa_szerokosc * rozmiar_kafelka
wysokosc_swiata = mapa_wysokosc * rozmiar_kafelka

font = pygame.font.SysFont("arial", 24)
font_maly = pygame.font.SysFont("arial", 20)
font_duzy = pygame.font.SysFont("arial", 28, bold=True)
font_akt = pygame.font.SysFont("arial", 32, bold=True)
font_wybor = pygame.font.SysFont("arial", 22, bold=True)
font_dymek = pygame.font.SysFont("arial", 18, bold=True)

zegar = pygame.time.Clock()
plik_zapisu = "savegame.json"

lokacja = "zewnatrz"

gracz_szerokosc = 30
gracz_wysokosc = 30
predkosc = 5
gracz_x = 12 * rozmiar_kafelka
gracz_y = 12 * rozmiar_kafelka
ostatni_kierunek = "dol"

gracz_max_hp = 100
gracz_hp = 100
gracz_nie_dostaje_obrazen_timer = 0

stamina_max = 100
stamina = 100
stamina_wyswietlana = 100
regen_staminy_timer = 0

koszt_ataku = 16
koszt_bloku = 10
koszt_uniku = 24

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

jakub_x = 17 * rozmiar_kafelka
jakub_y = 18 * rozmiar_kafelka
jakub_szerokosc = 30
jakub_wysokosc = 30

michal_x = 12 * rozmiar_kafelka
michal_y = 15 * rozmiar_kafelka
michal_szerokosc = 30
michal_wysokosc = 30

pokaz_dialog = False
tekst_dialogu = ""

pokaz_wybor = False
tekst_wyboru = ""
opcja_1 = ""
opcja_2 = ""
wybor_kontekst = None

akt = 1
nazwa_aktu = "AKT 1: Cien nad Bydgostem"
etap_fabuly = 0
sciezka_fabuly = "Byd"
byd_punkty = 0
tekst_zadania = "Zadanie: porozmawiaj z Jakubem"

czy_ma_klucz = False
klucz_x = 9 * rozmiar_kafelka
klucz_y = 3 * rozmiar_kafelka
klucz_szerokosc = 20
klucz_wysokosc = 20

komunikat_systemowy = ""
komunikat_timer = 0

dom_wejscie_rect = pygame.Rect(8 * rozmiar_kafelka, 8 * rozmiar_kafelka, 4 * rozmiar_kafelka, 3 * rozmiar_kafelka)
mlyn_rect = pygame.Rect(33 * rozmiar_kafelka, 20 * rozmiar_kafelka, 4 * rozmiar_kafelka, 4 * rozmiar_kafelka)

wrog_byd = {
    "x": 36 * rozmiar_kafelka,
    "y": 26 * rozmiar_kafelka,
    "szer": 36,
    "wys": 36,
    "kolor": ciemna_czerwien,
    "max_hp": 120,
    "hp": 120,
    "aktywny": False,
    "zyje": True,
    "predkosc": 2,
    "atak_cooldown": 0,
    "nazwa": "Psoglaw",
    "stan_ataku": "brak",
    "telegraph_timer": 0,
    "atak_rect": pygame.Rect(0, 0, 0, 0),
    "typ_ataku": None,
    "dymek_tekst": "",
    "dymek_timer": 0,
    "ogluszony_timer": 0,
    "glosy": [
        "Raaawr!",
        "Gruchotam kosci!",
        "Trakt nalezy do mnie!",
        "Czuje twoj strach!",
        "Rozszarpie cie!",
        "Krew na ziemi Byd!"
    ]
}

mapa_dom = [
    ["sciana"] * 14,
    ["sciana"] + ["podloga"] * 12 + ["sciana"],
    ["sciana"] + ["podloga"] * 12 + ["sciana"],
    ["sciana"] + ["podloga"] * 12 + ["sciana"],
    ["sciana"] + ["podloga"] * 5 + ["stol"] * 2 + ["podloga"] * 5 + ["sciana"],
    ["sciana"] + ["podloga"] * 12 + ["sciana"],
    ["sciana"] + ["podloga"] * 4 + ["wyjscie"] + ["podloga"] * 7 + ["sciana"],
    ["sciana"] * 14
]

npc_wies = [
    {
        "imie": "Stary rybak",
        "x": 22 * rozmiar_kafelka,
        "y": 17 * rozmiar_kafelka,
        "szer": 28,
        "wys": 28,
        "kolor": (120, 80, 40),
        "dialogi": [
            "Rzeka pamieta wiecej niz ludzie.",
            "Mowia, ze przy mlynie znow cos sie budzi.",
            "Za dawnych lat straz Byd trzymala tu porzadek."
        ],
        "timer": 0,
        "kierunek": random.choice(["gora", "dol", "lewo", "prawo", "stop"])
    },
    {
        "imie": "Kobieta z wioski",
        "x": 25 * rozmiar_kafelka,
        "y": 14 * rozmiar_kafelka,
        "szer": 28,
        "wys": 28,
        "kolor": (220, 100, 120),
        "dialogi": [
            "W nocy slyszalam kroki przy starym trakcie.",
            "Lepiej nie isc samemu na wschod.",
            "Jakub zna te ziemie lepiej niz wszyscy."
        ],
        "timer": 0,
        "kierunek": random.choice(["gora", "dol", "lewo", "prawo", "stop"])
    },
    {
        "imie": "Mlodzieniec",
        "x": 19 * rozmiar_kafelka,
        "y": 22 * rozmiar_kafelka,
        "szer": 28,
        "wys": 28,
        "kolor": (70, 70, 200),
        "dialogi": [
            "Widzialem swiatlo przy mlynie.",
            "Straznicy Byd podobno znow zbieraja ludzi.",
            "Jesli szukasz klopotow, idz traktem na wschod."
        ],
        "timer": 0,
        "kierunek": random.choice(["gora", "dol", "lewo", "prawo", "stop"])
    }
]


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

    for y in range(10, mapa_wysokosc - 8):
        mapa[y][30] = "woda"
        mapa[y][31] = "woda"
        mapa[y][32] = "woda"

    for x in range(5, 40):
        mapa[18][x] = "sciezka"
        mapa[19][x] = "sciezka"

    for y in range(8, 24):
        mapa[y][15] = "sciezka"
        mapa[y][16] = "sciezka"

    for x in range(8, 12):
        for y in range(8, 11):
            mapa[y][x] = "dom"

    for x in range(18, 22):
        for y in range(11, 14):
            mapa[y][x] = "dom"

    for x in range(23, 27):
        for y in range(15, 18):
            mapa[y][x] = "dom"

    for x in range(26, 30):
        for y in range(11, 14):
            mapa[y][x] = "dom"

    for x in range(33, 37):
        for y in range(20, 24):
            mapa[y][x] = "mlyn"

    for x in range(40, 60):
        mapa[19][x] = "sciezka"

    for y in range(18, 32):
        mapa[y][58] = "sciezka"
        mapa[y][59] = "sciezka"

    for x in range(60, 80):
        mapa[30][x] = "sciezka"

    return mapa


mapa = stworz_mape_zewnetrzna()


def pokaz_komunikat(tekst):
    global komunikat_systemowy, komunikat_timer
    komunikat_systemowy = tekst
    komunikat_timer = 180


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
        "czy_ma_klucz": czy_ma_klucz,
        "gracz_hp": gracz_hp,
        "wrog_hp": wrog_byd["hp"],
        "wrog_zyje": wrog_byd["zyje"]
    }

    with open(plik_zapisu, "w", encoding="utf-8") as plik:
        json.dump(dane, plik, ensure_ascii=False, indent=4)


def wczytaj_gre():
    global lokacja, gracz_x, gracz_y, akt, nazwa_aktu, etap_fabuly
    global sciezka_fabuly, byd_punkty, tekst_zadania, czy_ma_klucz
    global pokaz_dialog, pokaz_wybor, tekst_dialogu, gracz_hp

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
    czy_ma_klucz = dane["czy_ma_klucz"]
    gracz_hp = dane.get("gracz_hp", 100)
    wrog_byd["hp"] = dane.get("wrog_hp", wrog_byd["max_hp"])
    wrog_byd["zyje"] = dane.get("wrog_zyje", True)

    pokaz_dialog = False
    pokaz_wybor = False
    tekst_dialogu = ""
    pokaz_komunikat("Gra wczytana.")


def pobierz_aktualna_mape():
    if lokacja == "zewnatrz":
        return mapa
    return mapa_dom


def podziel_tekst_na_linie(tekst, font_uzyty, maks_szerokosc):
    slowa = tekst.split()
    linie = []
    aktualna_linia = ""

    for slowo in slowa:
        test_linia = aktualna_linia + slowo + " "
        szerokosc_tekstu, _ = font_uzyty.size(test_linia)

        if szerokosc_tekstu <= maks_szerokosc:
            aktualna_linia = test_linia
        else:
            if aktualna_linia.strip() != "":
                linie.append(aktualna_linia.strip())
            aktualna_linia = slowo + " "

    if aktualna_linia.strip() != "":
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
    global byd_punkty, etap_fabuly, tekst_zadania, tekst_dialogu, pokaz_dialog

    if wybor_kontekst == "decyzja_przy_mlynie":
        if numer_opcji == 1:
            byd_punkty += 2
            tekst_dialogu = "Lukasz: Najpierw oczyszcze teren sila. Droga Byd musi byc bezpieczna."
            pokaz_dialog = True
            etap_fabuly = 7
            tekst_zadania = "Zadanie: pokonaj Psoglawa przy mlynie"
            wrog_byd["aktywny"] = True
        elif numer_opcji == 2:
            byd_punkty += 1
            tekst_dialogu = "Lukasz: Podejde do tego z glowa. Ale i tak trzeba bedzie go zatrzymac."
            pokaz_dialog = True
            etap_fabuly = 7
            tekst_zadania = "Zadanie: pokonaj Psoglawa przy mlynie"
            wrog_byd["aktywny"] = True

    zakoncz_wybor()


def policz_kamere():
    if lokacja == "dom":
        max_szer = len(mapa_dom[0]) * rozmiar_kafelka
        max_wys = len(mapa_dom) * rozmiar_kafelka
        kamera_x = max(0, min(gracz_x - szerokosc // 2, max_szer - szerokosc))
        kamera_y = max(0, min(gracz_y - wysokosc // 2, max_wys - wysokosc))
        return kamera_x, kamera_y

    kamera_x = gracz_x - szerokosc // 2
    kamera_y = gracz_y - wysokosc // 2

    kamera_x = max(0, min(kamera_x, szerokosc_swiata - szerokosc))
    kamera_y = max(0, min(kamera_y, wysokosc_swiata - wysokosc))

    return kamera_x, kamera_y


def rysuj_mape(kamera_x, kamera_y):
    aktualna_mapa = pobierz_aktualna_mape()

    start_kolumna = max(0, kamera_x // rozmiar_kafelka)
    koniec_kolumna = min(len(aktualna_mapa[0]), (kamera_x + szerokosc) // rozmiar_kafelka + 2)

    start_wiersz = max(0, kamera_y // rozmiar_kafelka)
    koniec_wiersz = min(len(aktualna_mapa), (kamera_y + wysokosc) // rozmiar_kafelka + 2)

    for numer_wiersza in range(start_wiersz, koniec_wiersz):
        for numer_kolumny in range(start_kolumna, koniec_kolumna):
            pole = aktualna_mapa[numer_wiersza][numer_kolumny]

            if pole == "trawa":
                kolor = zielony
            elif pole == "sciezka":
                kolor = brazowy
            elif pole == "woda":
                kolor = niebieski
            elif pole == "dom":
                kolor = szary
            elif pole == "mlyn":
                kolor = jasny_braz
            elif pole == "sciana":
                kolor = (80, 80, 80)
            elif pole == "podloga":
                kolor = (210, 180, 140)
            elif pole == "wyjscie":
                kolor = pomaranczowy
            elif pole == "stol":
                kolor = (140, 90, 50)
            else:
                kolor = bialy

            ekran_x = numer_kolumny * rozmiar_kafelka - kamera_x
            ekran_y = numer_wiersza * rozmiar_kafelka - kamera_y

            pygame.draw.rect(okno, kolor, (ekran_x, ekran_y, rozmiar_kafelka, rozmiar_kafelka))
            pygame.draw.rect(okno, czarny, (ekran_x, ekran_y, rozmiar_kafelka, rozmiar_kafelka), 1)


def czy_mozna_wejsc(nowe_x, nowe_y):
    aktualna_mapa = pobierz_aktualna_mape()

    lewy = nowe_x
    prawy = nowe_x + gracz_szerokosc - 1
    gora = nowe_y
    dol = nowe_y + gracz_wysokosc - 1

    rogi = [
        (lewy, gora),
        (prawy, gora),
        (lewy, dol),
        (prawy, dol)
    ]

    for x, y in rogi:
        kolumna = x // rozmiar_kafelka
        wiersz = y // rozmiar_kafelka

        if wiersz < 0 or kolumna < 0:
            return False
        if wiersz >= len(aktualna_mapa) or kolumna >= len(aktualna_mapa[wiersz]):
            return False

        if aktualna_mapa[wiersz][kolumna] in ["woda", "dom", "sciana", "mlyn", "stol"]:
            return False

    if lokacja == "zewnatrz":
        prostokat_gracza = pygame.Rect(nowe_x, nowe_y, gracz_szerokosc, gracz_wysokosc)
        prostokat_jakuba = pygame.Rect(jakub_x, jakub_y, jakub_szerokosc, jakub_wysokosc)
        prostokat_michala = pygame.Rect(michal_x, michal_y, michal_szerokosc, michal_wysokosc)

        if prostokat_gracza.colliderect(prostokat_jakuba):
            return False

        if prostokat_gracza.colliderect(prostokat_michala):
            return False

        for npc in npc_wies:
            prostokat_npc = pygame.Rect(npc["x"], npc["y"], npc["szer"], npc["wys"])
            if prostokat_gracza.colliderect(prostokat_npc):
                return False

        if wrog_byd["aktywny"] and wrog_byd["zyje"]:
            prostokat_wroga = pygame.Rect(wrog_byd["x"], wrog_byd["y"], wrog_byd["szer"], wrog_byd["wys"])
            if prostokat_gracza.colliderect(prostokat_wroga):
                return False

    return True


def czy_gracz_jest_blisko_postaci(postac_x, postac_y, postac_szer, postac_wys):
    if lokacja != "zewnatrz":
        return False

    prostokat_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    prostokat_postaci = pygame.Rect(postac_x, postac_y, postac_szer, postac_wys)
    strefa_rozmowy = prostokat_postaci.inflate(60, 60)

    return prostokat_gracza.colliderect(strefa_rozmowy)


def czy_gracz_jest_blisko_jakuba():
    return czy_gracz_jest_blisko_postaci(jakub_x, jakub_y, jakub_szerokosc, jakub_wysokosc)


def czy_gracz_jest_blisko_michala():
    return czy_gracz_jest_blisko_postaci(michal_x, michal_y, michal_szerokosc, michal_wysokosc)


def czy_gracz_jest_przy_domku():
    if lokacja != "zewnatrz":
        return False

    prostokat_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    strefa_domku = dom_wejscie_rect.inflate(20, 20)

    return prostokat_gracza.colliderect(strefa_domku)


def czy_gracz_jest_przy_kluczu():
    if lokacja != "dom" or czy_ma_klucz:
        return False

    prostokat_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    prostokat_klucza = pygame.Rect(klucz_x, klucz_y, klucz_szerokosc, klucz_wysokosc)
    strefa_klucza = prostokat_klucza.inflate(20, 20)

    return prostokat_gracza.colliderect(strefa_klucza)


def czy_gracz_jest_przy_mlynie():
    if lokacja != "zewnatrz":
        return False

    prostokat_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    return prostokat_gracza.colliderect(mlyn_rect.inflate(40, 40))


def znajdz_bliskiego_npc():
    if lokacja != "zewnatrz":
        return None

    prostokat_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)

    for npc in npc_wies:
        prostokat_npc = pygame.Rect(npc["x"], npc["y"], npc["szer"], npc["wys"])
        strefa = prostokat_npc.inflate(60, 60)
        if prostokat_gracza.colliderect(strefa):
            return npc

    return None


def czy_wystarczy_staminy(koszt):
    return stamina >= koszt


def zuzyj_stamine(ile):
    global stamina, regen_staminy_timer
    stamina -= ile
    if stamina < 0:
        stamina = 0
    regen_staminy_timer = 45


def regeneruj_stamine():
    global stamina, stamina_wyswietlana, regen_staminy_timer

    if regen_staminy_timer > 0:
        regen_staminy_timer -= 1
    else:
        if stamina < stamina_max:
            stamina += 0.45
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
    atak_cooldown = 20
    atak_trafil = False

    if ostatni_kierunek == "gora":
        atak_rect = pygame.Rect(gracz_x - 8, gracz_y - 34, 46, 34)
    elif ostatni_kierunek == "dol":
        atak_rect = pygame.Rect(gracz_x - 8, gracz_y + gracz_wysokosc, 46, 34)
    elif ostatni_kierunek == "lewo":
        atak_rect = pygame.Rect(gracz_x - 34, gracz_y - 8, 34, 46)
    else:
        atak_rect = pygame.Rect(gracz_x + gracz_szerokosc, gracz_y - 8, 34, 46)


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
    unik_cooldown = 40

    dystans_uniku = 60
    nowy_x = gracz_x
    nowy_y = gracz_y

    if ostatni_kierunek == "gora":
        nowy_y -= dystans_uniku
    elif ostatni_kierunek == "dol":
        nowy_y += dystans_uniku
    elif ostatni_kierunek == "lewo":
        nowy_x -= dystans_uniku
    elif ostatni_kierunek == "prawo":
        nowy_x += dystans_uniku

    if lokacja == "zewnatrz":
        nowy_x = max(0, min(nowy_x, szerokosc_swiata - gracz_szerokosc))
        nowy_y = max(0, min(nowy_y, wysokosc_swiata - gracz_wysokosc))

    if czy_mozna_wejsc(nowy_x, nowy_y):
        gracz_x = nowy_x
        gracz_y = nowy_y


def aktualizuj_atak():
    global atak_aktywny, atak_timer, atak_cooldown, atak_trafil

    if atak_cooldown > 0:
        atak_cooldown -= 1

    if atak_aktywny:
        atak_timer -= 1

        if wrog_byd["aktywny"] and wrog_byd["zyje"] and not atak_trafil:
            rect_wroga = pygame.Rect(wrog_byd["x"], wrog_byd["y"], wrog_byd["szer"], wrog_byd["wys"])
            if atak_rect.colliderect(rect_wroga):
                wrog_byd["hp"] -= 12
                atak_trafil = True
                pokaz_komunikat("Trafiles Psoglawa.")

                if wrog_byd["hp"] <= 0:
                    wrog_byd["hp"] = 0
                    wrog_byd["zyje"] = False
                    wrog_byd["aktywny"] = False
                    wrog_byd["stan_ataku"] = "brak"

        if atak_timer <= 0:
            atak_aktywny = False


def dystans_do_gracza():
    srodek_gracza_x = gracz_x + gracz_szerokosc // 2
    srodek_gracza_y = gracz_y + gracz_wysokosc // 2
    srodek_wroga_x = wrog_byd["x"] + wrog_byd["szer"] // 2
    srodek_wroga_y = wrog_byd["y"] + wrog_byd["wys"] // 2

    return math.hypot(srodek_gracza_x - srodek_wroga_x, srodek_gracza_y - srodek_wroga_y)


def wylicz_rect_ataku_wroga(typ_ataku):
    rozmiar = 60 if typ_ataku == "blokowalny" else 95

    dx = gracz_x - wrog_byd["x"]
    dy = gracz_y - wrog_byd["y"]

    if abs(dx) > abs(dy):
        if dx > 0:
            return pygame.Rect(wrog_byd["x"] + wrog_byd["szer"], wrog_byd["y"] - 10, rozmiar, 56)
        else:
            return pygame.Rect(wrog_byd["x"] - rozmiar, wrog_byd["y"] - 10, rozmiar, 56)
    else:
        if dy > 0:
            return pygame.Rect(wrog_byd["x"] - 10, wrog_byd["y"] + wrog_byd["wys"], 56, rozmiar)
        else:
            return pygame.Rect(wrog_byd["x"] - 10, wrog_byd["y"] - rozmiar, 56, rozmiar)


def aktywuj_losowy_dymek_wroga():
    if wrog_byd["dymek_timer"] <= 0 and random.randint(1, 180) == 1:
        wrog_byd["dymek_tekst"] = random.choice(wrog_byd["glosy"])
        wrog_byd["dymek_timer"] = 90


def zadaj_obrazenia_graczowi(typ_ataku):
    global gracz_hp, gracz_nie_dostaje_obrazen_timer

    rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)

    if not wrog_byd["atak_rect"].colliderect(rect_gracza):
        return

    if czy_unik:
        pokaz_komunikat("Udany unik!")
        return

    if typ_ataku == "blokowalny":
        if perfect_block_timer > 0:
            pokaz_komunikat("PERFECT BLOCK!")
            wrog_byd["ogluszony_timer"] = 55
            wrog_byd["atak_cooldown"] = 70
            return

        if blok_aktywny:
            gracz_hp -= 3
            pokaz_komunikat("Zablokowales atak.")
        else:
            gracz_hp -= 14
            pokaz_komunikat("Psoglaw trafil cie.")

    elif typ_ataku == "nieblokowalny":
        gracz_hp -= 28
        pokaz_komunikat("Czerwony atak trafia mocno!")

    if gracz_hp < 0:
        gracz_hp = 0

    gracz_nie_dostaje_obrazen_timer = 28


def aktualizuj_wroga():
    if not wrog_byd["aktywny"] or not wrog_byd["zyje"] or lokacja != "zewnatrz":
        return

    if wrog_byd["ogluszony_timer"] > 0:
        wrog_byd["ogluszony_timer"] -= 1
        if wrog_byd["dymek_timer"] <= 0:
            wrog_byd["dymek_tekst"] = "Auuurgh!"
            wrog_byd["dymek_timer"] = 35
        return

    aktywuj_losowy_dymek_wroga()

    if wrog_byd["dymek_timer"] > 0:
        wrog_byd["dymek_timer"] -= 1

    if wrog_byd["atak_cooldown"] > 0:
        wrog_byd["atak_cooldown"] -= 1

    if wrog_byd["telegraph_timer"] > 0:
        wrog_byd["telegraph_timer"] -= 1

        if wrog_byd["telegraph_timer"] <= 0 and wrog_byd["typ_ataku"] is not None:
            zadaj_obrazenia_graczowi(wrog_byd["typ_ataku"])
            wrog_byd["stan_ataku"] = "brak"
            wrog_byd["typ_ataku"] = None
            wrog_byd["atak_rect"] = pygame.Rect(0, 0, 0, 0)
            wrog_byd["atak_cooldown"] = 45
        return

    dystans = dystans_do_gracza()

    if dystans < 320:
        dx = gracz_x - wrog_byd["x"]
        dy = gracz_y - wrog_byd["y"]

        if dystans > 70:
            if abs(dx) > abs(dy):
                krok_x = wrog_byd["predkosc"] if dx > 0 else -wrog_byd["predkosc"]
                nowy_x = wrog_byd["x"] + krok_x
                rect_test = pygame.Rect(nowy_x, wrog_byd["y"], wrog_byd["szer"], wrog_byd["wys"])
                rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
                if not rect_test.colliderect(rect_gracza):
                    wrog_byd["x"] = nowy_x
            else:
                krok_y = wrog_byd["predkosc"] if dy > 0 else -wrog_byd["predkosc"]
                nowy_y = wrog_byd["y"] + krok_y
                rect_test = pygame.Rect(wrog_byd["x"], nowy_y, wrog_byd["szer"], wrog_byd["wys"])
                rect_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
                if not rect_test.colliderect(rect_gracza):
                    wrog_byd["y"] = nowy_y

    if dystans < 95 and wrog_byd["atak_cooldown"] <= 0:
        los = random.randint(1, 100)

        if los <= 65:
            wrog_byd["typ_ataku"] = "blokowalny"
            wrog_byd["telegraph_timer"] = 28
        else:
            wrog_byd["typ_ataku"] = "nieblokowalny"
            wrog_byd["telegraph_timer"] = 36

        wrog_byd["atak_rect"] = wylicz_rect_ataku_wroga(wrog_byd["typ_ataku"])
        wrog_byd["stan_ataku"] = "telegraph"


def aktualizuj_ruch_npc():
    for npc in npc_wies:
        npc["timer"] += 1

        if npc["timer"] > 50:
            npc["timer"] = 0
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

        kolumna = (npc["x"] + npc["szer"] // 2) // rozmiar_kafelka
        wiersz = (npc["y"] + npc["wys"] // 2) // rozmiar_kafelka

        if not (10 <= npc["x"] <= 30 * rozmiar_kafelka and 10 <= npc["y"] <= 24 * rozmiar_kafelka):
            npc["x"] = stare_x
            npc["y"] = stare_y
        elif mapa[wiersz][kolumna] in ["woda", "dom", "mlyn"]:
            npc["x"] = stare_x
            npc["y"] = stare_y


def rysuj_imie(imie, x, y, szerokosc_postaci, kamera_x, kamera_y):
    tekst = font_maly.render(imie, True, czarny)
    prostokat_tekstu = tekst.get_rect(center=(x - kamera_x + szerokosc_postaci // 2, y - kamera_y - 12))
    okno.blit(tekst, prostokat_tekstu)


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


def rysuj_dymek(tekst, x, y, kamera_x, kamera_y):
    if tekst == "":
        return

    surf = font_dymek.render(tekst, True, czarny)
    padding_x = 10
    padding_y = 6
    szer = surf.get_width() + padding_x * 2
    wys = surf.get_height() + padding_y * 2

    rect = pygame.Rect(x - kamera_x - szer // 2, y - kamera_y - 55, szer, wys)
    pygame.draw.rect(okno, bialy, rect, border_radius=10)
    pygame.draw.rect(okno, czarny, rect, 2, border_radius=10)
    okno.blit(surf, (rect.x + padding_x, rect.y + padding_y))


def rysuj_wroga(kamera_x, kamera_y):
    if lokacja == "zewnatrz" and wrog_byd["zyje"] and (wrog_byd["aktywny"] or etap_fabuly >= 7):
        pygame.draw.rect(okno, wrog_byd["kolor"], (wrog_byd["x"] - kamera_x, wrog_byd["y"] - kamera_y, wrog_byd["szer"], wrog_byd["wys"]))
        rysuj_imie(wrog_byd["nazwa"], wrog_byd["x"], wrog_byd["y"], wrog_byd["szer"], kamera_x, kamera_y)
        rysuj_pasek_hp_nad_postacia(wrog_byd["x"] - kamera_x, wrog_byd["y"] - kamera_y - 22, 50, 7, wrog_byd["hp"], wrog_byd["max_hp"])

        if wrog_byd["dymek_timer"] > 0:
            rysuj_dymek(
                wrog_byd["dymek_tekst"],
                wrog_byd["x"] + wrog_byd["szer"] // 2,
                wrog_byd["y"],
                kamera_x,
                kamera_y
            )


def rysuj_telegraph_wroga(kamera_x, kamera_y):
    if wrog_byd["stan_ataku"] == "telegraph":
        kolor = pomaranczowy if wrog_byd["typ_ataku"] == "blokowalny" else czerwony
        pygame.draw.rect(
            okno,
            kolor,
            (
                wrog_byd["atak_rect"].x - kamera_x,
                wrog_byd["atak_rect"].y - kamera_y,
                wrog_byd["atak_rect"].width,
                wrog_byd["atak_rect"].height
            ),
            3
        )


def rysuj_klucz(kamera_x, kamera_y):
    if lokacja == "dom" and not czy_ma_klucz:
        pygame.draw.rect(okno, zolty, (klucz_x - kamera_x, klucz_y - kamera_y, klucz_szerokosc, klucz_wysokosc))
        pygame.draw.rect(okno, czarny, (klucz_x - kamera_x, klucz_y - kamera_y, klucz_szerokosc, klucz_wysokosc), 2)


def rysuj_gracza(kamera_x, kamera_y):
    kolor_gracza = czerwony

    if czy_unik:
        kolor_gracza = blekit
    elif blok_aktywny:
        kolor_gracza = niebieski
    elif gracz_nie_dostaje_obrazen_timer > 0 and (gracz_nie_dostaje_obrazen_timer // 4) % 2 == 0:
        kolor_gracza = (255, 170, 170)

    pygame.draw.rect(okno, kolor_gracza, (gracz_x - kamera_x, gracz_y - kamera_y, gracz_szerokosc, gracz_wysokosc))
    rysuj_imie("Lukasz", gracz_x, gracz_y, gracz_szerokosc, kamera_x, kamera_y)


def rysuj_atak(kamera_x, kamera_y):
    if atak_aktywny:
        pygame.draw.rect(okno, pomaranczowy, (atak_rect.x - kamera_x, atak_rect.y - kamera_y, atak_rect.width, atak_rect.height), 2)


def rysuj_dialog():
    prostokat_dialogu = pygame.Rect(25, 415, 750, 165)

    pygame.draw.rect(okno, jasny_szary, prostokat_dialogu)
    pygame.draw.rect(okno, czarny, prostokat_dialogu, 4)

    linie = podziel_tekst_na_linie(tekst_dialogu, font, 700)

    y_tekst = 435
    for linia in linie[:4]:
        tekst = font.render(linia, True, czarny)
        okno.blit(tekst, (45, y_tekst))
        y_tekst += 30

    tekst_pomocniczy = font_maly.render("ESC - zamknij dialog", True, ciemny_szary)
    okno.blit(tekst_pomocniczy, (560, 548))


def rysuj_panel_wyboru():
    prostokat_wyboru = pygame.Rect(70, 250, 660, 190)

    pygame.draw.rect(okno, jasny_szary, prostokat_wyboru)
    pygame.draw.rect(okno, czarny, prostokat_wyboru, 4)

    linie = podziel_tekst_na_linie(tekst_wyboru, font, 610)
    y = 270
    for linia in linie[:3]:
        tekst = font.render(linia, True, czarny)
        okno.blit(tekst, (95, y))
        y += 28

    opcja1_tekst = font_wybor.render("1 - " + opcja_1, True, fioletowy)
    opcja2_tekst = font_wybor.render("2 - " + opcja_2, True, fioletowy)

    okno.blit(opcja1_tekst, (95, 345))
    okno.blit(opcja2_tekst, (95, 380))


def rysuj_zadanie():
    panel = pygame.Rect(15, 15, 590, 105)
    pygame.draw.rect(okno, jasny_szary, panel)
    pygame.draw.rect(okno, czarny, panel, 3)

    tekst_aktu = font_akt.render(nazwa_aktu, True, fioletowy)
    okno.blit(tekst_aktu, (28, 22))

    linie_zadania = podziel_tekst_na_linie(tekst_zadania, font_maly, 550)
    y_zadania = 68

    for linia in linie_zadania[:2]:
        tekst = font_maly.render(linia, True, czarny)
        okno.blit(tekst, (30, y_zadania))
        y_zadania += 24


def rysuj_ministatus():
    panel = pygame.Rect(590, 15, 195, 205)
    pygame.draw.rect(okno, jasny_szary, panel)
    pygame.draw.rect(okno, czarny, panel, 3)

    tekst1 = font_maly.render(f"Sciezka: {sciezka_fabuly}", True, czarny)
    tekst2 = font_maly.render(f"Etap: {etap_fabuly}", True, czarny)
    tekst3 = font_maly.render(f"Klucz: {'TAK' if czy_ma_klucz else 'NIE'}", True, czarny)
    tekst4 = font_maly.render(f"Punkty Byd: {byd_punkty}", True, nieco_zloty)
    tekst5 = font_maly.render(f"HP: {gracz_hp}/{gracz_max_hp}", True, czerwony)
    tekst6 = font_maly.render("CTRL blok/parry", True, niebieski)
    tekst7 = font_maly.render("SHIFT unik", True, blekit)
    tekst8 = font_maly.render(f"STA: {int(stamina)}/{stamina_max}", True, zolty)

    okno.blit(tekst1, (602, 28))
    okno.blit(tekst2, (602, 52))
    okno.blit(tekst3, (602, 76))
    okno.blit(tekst4, (602, 100))
    okno.blit(tekst5, (602, 124))
    okno.blit(tekst6, (602, 148))
    okno.blit(tekst7, (602, 170))
    okno.blit(tekst8, (602, 192))


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


def rysuj_pasek_hp_nad_postacia(x, y, szer, wys, hp, max_hp):
    ratio = hp / max_hp
    if ratio < 0:
        ratio = 0

    pygame.draw.rect(okno, ciemna_czerwien, (x, y, szer, wys))
    pygame.draw.rect(okno, zielony_hp, (x, y, int(szer * ratio), wys))
    pygame.draw.rect(okno, czarny, (x, y, szer, wys), 1)


def rysuj_podpowiedz():
    tekst_podpowiedzi = None

    if lokacja == "zewnatrz":
        if czy_gracz_jest_blisko_jakuba() or czy_gracz_jest_blisko_michala():
            tekst_podpowiedzi = "Nacisnij E"

        elif znajdz_bliskiego_npc() is not None:
            tekst_podpowiedzi = "Nacisnij E, aby porozmawiac"

        elif czy_gracz_jest_przy_domku():
            tekst_podpowiedzi = "Nacisnij E, aby wejsc"

        elif czy_gracz_jest_przy_mlynie() and etap_fabuly >= 5 and etap_fabuly < 7:
            tekst_podpowiedzi = "Nacisnij E przy mlynie"

        elif etap_fabuly >= 7 and wrog_byd["zyje"] and dystans_do_gracza() < 150:
            tekst_podpowiedzi = "SPACJA atak | CTRL perfect block | SHIFT unik"

    elif lokacja == "dom":
        if czy_gracz_jest_przy_kluczu():
            tekst_podpowiedzi = "Nacisnij E, aby podniesc klucz"
        else:
            srodek_x = gracz_x + gracz_szerokosc // 2
            srodek_y = gracz_y + gracz_wysokosc // 2

            kolumna = srodek_x // rozmiar_kafelka
            wiersz = srodek_y // rozmiar_kafelka

            if 0 <= wiersz < len(mapa_dom) and 0 <= kolumna < len(mapa_dom[wiersz]):
                if mapa_dom[wiersz][kolumna] == "wyjscie":
                    tekst_podpowiedzi = "Nacisnij E, aby wyjsc"

    if tekst_podpowiedzi:
        tekst = font_maly.render(tekst_podpowiedzi, True, czarny)
        prostokat_tekstu = tekst.get_rect(center=(szerokosc // 2, 395))
        okno.blit(tekst, prostokat_tekstu)


def rysuj_komunikat_systemowy():
    if komunikat_timer > 0 and komunikat_systemowy != "":
        panel = pygame.Rect(215, 560, 370, 28)
        pygame.draw.rect(okno, jasny_szary, panel)
        pygame.draw.rect(okno, czarny, panel, 2)
        tekst = font_maly.render(komunikat_systemowy, True, czarny)
        prostokat = tekst.get_rect(center=panel.center)
        okno.blit(tekst, prostokat)


def reset_po_smierci():
    global gracz_x, gracz_y, gracz_hp, etap_fabuly, tekst_zadania
    global pokaz_dialog, tekst_dialogu, atak_aktywny, blok_aktywny, czy_unik
    global stamina, stamina_wyswietlana, perfect_block_timer, perfect_block_cooldown

    gracz_x = 17 * rozmiar_kafelka
    gracz_y = 18 * rozmiar_kafelka
    gracz_hp = gracz_max_hp
    stamina = stamina_max
    stamina_wyswietlana = stamina_max
    perfect_block_timer = 0
    perfect_block_cooldown = 0
    atak_aktywny = False
    blok_aktywny = False
    czy_unik = False

    wrog_byd["x"] = 36 * rozmiar_kafelka
    wrog_byd["y"] = 26 * rozmiar_kafelka
    wrog_byd["hp"] = wrog_byd["max_hp"]
    wrog_byd["aktywny"] = False
    wrog_byd["zyje"] = True
    wrog_byd["stan_ataku"] = "brak"
    wrog_byd["telegraph_timer"] = 0
    wrog_byd["typ_ataku"] = None
    wrog_byd["dymek_tekst"] = ""
    wrog_byd["dymek_timer"] = 0
    wrog_byd["ogluszony_timer"] = 0

    etap_fabuly = 6
    tekst_zadania = "Zadanie: wroc do Jakuba i wybierz metode dzialania Byd"
    pokaz_dialog = True
    tekst_dialogu = "Lukasz: Psoglaw mnie rozszarpal... Musze sprobowac jeszcze raz."


dziala = True
while dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dziala = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                zapisz_gre()
                pokaz_komunikat("Gra zapisana.")

            elif event.key == pygame.K_F9:
                wczytaj_gre()

            elif pokaz_wybor:
                if event.key == pygame.K_1:
                    obsluz_wybor(1)
                elif event.key == pygame.K_2:
                    obsluz_wybor(2)
                elif event.key == pygame.K_ESCAPE:
                    zakoncz_wybor()

            else:
                if event.key == pygame.K_SPACE:
                    rozpocznij_atak()

                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    rozpocznij_blok()

                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    rozpocznij_unik()

                if event.key == pygame.K_e:
                    if lokacja == "zewnatrz":
                        if czy_gracz_jest_blisko_jakuba():
                            if etap_fabuly == 0:
                                tekst_dialogu = "Jakub: Lukasz, dobrze ze jestes. Michal cos wyczul przy starych znakach. Pogadaj z nim."
                                pokaz_dialog = True
                                etap_fabuly = 1
                                tekst_zadania = "Zadanie: porozmawiaj z Michalem"

                            elif etap_fabuly == 4:
                                tekst_dialogu = "Jakub: Idziemy droga Byd. Zadnych ukrytych rytualow, tylko porzadek. Rusz do starego mlyna i sprawdz trakt."
                                pokaz_dialog = True
                                etap_fabuly = 5
                                tekst_zadania = "Zadanie: idz do starego mlyna i zabezpiecz szlak Byd"

                            elif etap_fabuly == 6:
                                tekst_dialogu = "Jakub: Dobrze. Teraz wybierz, jak umocnic pozycje Byd przy mlynie."
                                pokaz_dialog = True
                                rozpocznij_wybor(
                                    "decyzja_przy_mlynie",
                                    "Jak chcesz rozwiazac sytuacje przy mlynie?",
                                    "Silowo oczyscic teren i pokazac przewage.",
                                    "Ustawic ludzi madrze i zabezpieczyc szlak strategicznie."
                                )

                            elif etap_fabuly == 8:
                                tekst_dialogu = "Jakub: Dobrze. Psoglaw padl. Droga Byd zostala utrzymana."
                                pokaz_dialog = True
                                etap_fabuly = 9
                                tekst_zadania = "Zadanie: porozmawiaj z Michalem po walce"

                            elif etap_fabuly == 11:
                                tekst_dialogu = "Jakub: To dopiero poczatek. Szlak zyje tylko wtedy, gdy ktos go broni."
                                pokaz_dialog = True

                            else:
                                tekst_dialogu = "Jakub: Mamy robote. Najpierw skoncz to, co juz zaczales."
                                pokaz_dialog = True

                        elif czy_gracz_jest_blisko_michala():
                            if etap_fabuly == 1:
                                tekst_dialogu = "Michal: W chacie na zachodzie jest stary klucz. Bez niego nie zrozumiemy, co dzieje sie z ta ziemia."
                                pokaz_dialog = True
                                etap_fabuly = 2
                                tekst_zadania = "Zadanie: znajdz klucz w domu"

                            elif etap_fabuly >= 2 and not czy_ma_klucz:
                                tekst_dialogu = "Michal: Klucz jest w srodku. Szukaj uwaznie."
                                pokaz_dialog = True

                            elif etap_fabuly == 3 and czy_ma_klucz:
                                tekst_dialogu = "Michal: To pieczec dawnego Bydgostu. Zanies to Jakubowi. On wybierze droge."
                                pokaz_dialog = True
                                etap_fabuly = 4
                                tekst_zadania = "Zadanie: porozmawiaj z Jakubem o pieczeci"

                            elif etap_fabuly == 9:
                                if byd_punkty >= 2:
                                    tekst_dialogu = "Michal: Wybrales twardsza droge Byd. Ludzie beda o tym mowic jeszcze dlugo."
                                else:
                                    tekst_dialogu = "Michal: Utrzymales porzadek i nie straciles glowy. To tez jest sila."
                                pokaz_dialog = True
                                etap_fabuly = 10
                                tekst_zadania = "Zadanie: wroc do Jakuba, aby zamknac Akt 1"

                            else:
                                tekst_dialogu = "Michal: Ta ziemia mowi cicho. Trzeba umiec jej sluchac."
                                pokaz_dialog = True

                        elif znajdz_bliskiego_npc() is not None:
                            npc = znajdz_bliskiego_npc()
                            tekst_dialogu = npc["imie"] + ": " + random.choice(npc["dialogi"])
                            pokaz_dialog = True

                        elif czy_gracz_jest_przy_domku():
                            lokacja = "dom"
                            gracz_x = 5 * rozmiar_kafelka
                            gracz_y = 5 * rozmiar_kafelka
                            pokaz_dialog = False

                        elif czy_gracz_jest_przy_mlynie() and etap_fabuly == 5 and sciezka_fabuly == "Byd":
                            tekst_dialogu = "Lukasz: Mlyn stoi, ale trakt jest niespokojny. Droga Byd wymaga, by utrzymac porzadek. Musze wrocic do Jakuba."
                            pokaz_dialog = True
                            etap_fabuly = 6
                            tekst_zadania = "Zadanie: wroc do Jakuba i wybierz metode dzialania Byd"

                    elif lokacja == "dom":
                        if czy_gracz_jest_przy_kluczu():
                            czy_ma_klucz = True
                            tekst_dialogu = "Znalazles stary klucz z dziwnym znakiem."
                            pokaz_dialog = True

                            if etap_fabuly == 2:
                                etap_fabuly = 3
                                tekst_zadania = "Zadanie: wroc do Michala"
                        else:
                            srodek_x = gracz_x + gracz_szerokosc // 2
                            srodek_y = gracz_y + gracz_wysokosc // 2

                            kolumna = srodek_x // rozmiar_kafelka
                            wiersz = srodek_y // rozmiar_kafelka

                            if 0 <= wiersz < len(mapa_dom) and 0 <= kolumna < len(mapa_dom[wiersz]):
                                if mapa_dom[wiersz][kolumna] == "wyjscie":
                                    lokacja = "zewnatrz"
                                    gracz_x = 10 * rozmiar_kafelka
                                    gracz_y = 11 * rozmiar_kafelka
                                    pokaz_dialog = False

                if event.key == pygame.K_ESCAPE:
                    pokaz_dialog = False

    if lokacja == "zewnatrz":
        aktualizuj_ruch_npc()

    klawisze = pygame.key.get_pressed()

    nowe_x = gracz_x
    nowe_y = gracz_y

    if not pokaz_wybor:
        if klawisze[pygame.K_LEFT]:
            nowe_x -= predkosc
            ostatni_kierunek = "lewo"
        if klawisze[pygame.K_RIGHT]:
            nowe_x += predkosc
            ostatni_kierunek = "prawo"
        if klawisze[pygame.K_UP]:
            nowe_y -= predkosc
            ostatni_kierunek = "gora"
        if klawisze[pygame.K_DOWN]:
            nowe_y += predkosc
            ostatni_kierunek = "dol"

    if lokacja == "zewnatrz":
        nowe_x = max(0, min(nowe_x, szerokosc_swiata - gracz_szerokosc))
        nowe_y = max(0, min(nowe_y, wysokosc_swiata - gracz_wysokosc))
    else:
        nowe_x = max(0, min(nowe_x, len(mapa_dom[0]) * rozmiar_kafelka - gracz_szerokosc))
        nowe_y = max(0, min(nowe_y, len(mapa_dom) * rozmiar_kafelka - gracz_wysokosc))

    if czy_mozna_wejsc(nowe_x, nowe_y):
        gracz_x = nowe_x
        gracz_y = nowe_y

    if komunikat_timer > 0:
        komunikat_timer -= 1

    if gracz_nie_dostaje_obrazen_timer > 0:
        gracz_nie_dostaje_obrazen_timer -= 1

    regeneruj_stamine()

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

    aktualizuj_atak()
    aktualizuj_wroga()

    if etap_fabuly == 7 and not wrog_byd["zyje"]:
        etap_fabuly = 8
        tekst_zadania = "Zadanie: wroc do Jakuba po zwyciestwie"
        pokaz_dialog = True
        tekst_dialogu = "Lukasz: Psoglaw pokonany. Trakt znow nalezy do Byd."

    if gracz_hp <= 0:
        reset_po_smierci()

    kamera_x, kamera_y = policz_kamere()

    okno.fill(bialy)
    rysuj_mape(kamera_x, kamera_y)
    rysuj_npc(kamera_x, kamera_y)
    rysuj_telegraph_wroga(kamera_x, kamera_y)
    rysuj_wroga(kamera_x, kamera_y)
    rysuj_klucz(kamera_x, kamera_y)
    rysuj_gracza(kamera_x, kamera_y)
    rysuj_atak(kamera_x, kamera_y)
    rysuj_zadanie()
    rysuj_ministatus()
    rysuj_pasek_hp(605, 225, 180, 18, gracz_hp, gracz_max_hp)
    rysuj_pasek_staminy(605, 250, 180, 14, stamina_wyswietlana, stamina_max)
    rysuj_podpowiedz()
    rysuj_komunikat_systemowy()

    if pokaz_dialog:
        rysuj_dialog()

    if pokaz_wybor:
        rysuj_panel_wyboru()

    pygame.display.flip()
    zegar.tick(60)

pygame.quit()