import pygame

pygame.init()

szerokosc = 800
wysokosc = 600
okno = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption("Przygoda Łukasza")

bialy = (255, 255, 255)
zielony = (34, 177, 76)
brazowy = (185, 122, 87)
niebieski = (0, 162, 232)
czarny = (0, 0, 0)
szary = (120, 120, 120)
czerwony = (255, 0, 0)
fioletowy = (163, 73, 164)
zolty = (255, 201, 14)

rozmiar_kafelka = 40

mapa = [
    ["woda"] * 20,
    ["woda"] + ["trawa"] * 18 + ["woda"],
    ["woda"] + ["trawa"] * 18 + ["woda"],
    ["woda"] + ["trawa"] * 18 + ["woda"],
    ["woda"] + ["trawa"] * 4 + ["sciezka"] * 8 + ["trawa"] * 6 + ["woda"],
    ["woda"] + ["trawa"] * 4 + ["dom"] * 3 + ["trawa"] * 5 + ["sciezka"] + ["trawa"] * 5 + ["woda"],
    ["woda"] + ["trawa"] * 4 + ["dom"] * 3 + ["trawa"] * 5 + ["sciezka"] + ["trawa"] * 5 + ["woda"],
    ["woda"] + ["trawa"] * 4 + ["dom"] * 3 + ["trawa"] * 5 + ["sciezka"] + ["trawa"] * 5 + ["woda"],
    ["woda"] + ["trawa"] * 11 + ["sciezka"] + ["trawa"] * 7 + ["woda"],
    ["woda"] + ["trawa"] * 11 + ["sciezka"] + ["trawa"] * 7 + ["woda"],
    ["woda"] + ["trawa"] * 11 + ["sciezka"] + ["trawa"] * 7 + ["woda"],
    ["woda"] + ["trawa"] * 11 + ["sciezka"] + ["trawa"] * 7 + ["woda"],
    ["woda"] + ["trawa"] * 11 + ["sciezka"] + ["trawa"] * 7 + ["woda"],
    ["woda"] + ["trawa"] * 11 + ["sciezka"] + ["trawa"] * 7 + ["woda"],
    ["woda"] * 20
]

mapa_dom = [
    ["sciana"] * 10,
    ["sciana"] + ["podloga"] * 8 + ["sciana"],
    ["sciana"] + ["podloga"] * 8 + ["sciana"],
    ["sciana"] + ["podloga"] * 8 + ["sciana"],
    ["sciana"] + ["podloga"] * 3 + ["wyjscie"] + ["podloga"] * 4 + ["sciana"],
    ["sciana"] * 10
]

gracz_x = 100
gracz_y = 100
gracz_szerokosc = 30
gracz_wysokosc = 30
predkosc = 5

jakub_x = 520
jakub_y = 360
jakub_szerokosc = 30
jakub_wysokosc = 30

michal_x = 320
michal_y = 200
michal_szerokosc = 30
michal_wysokosc = 30

pokaz_dialog = False
tekst_dialogu = ""

rozmowa_z_jakubem = False
rozmowa_z_michalem = False
tekst_zadania = "Zadanie: porozmawiaj z Jakubem i Michałem"

lokacja = "zewnatrz"

czy_ma_klucz = False
klucz_x = 240
klucz_y = 120
klucz_szerokosc = 20
klucz_wysokosc = 20

font = pygame.font.SysFont("arial", 24)
zegar = pygame.time.Clock()


def pobierz_aktualna_mape():
    if lokacja == "zewnatrz":
        return mapa
    elif lokacja == "dom":
        return mapa_dom


def rysuj_mape(aktualna_mapa):
    for numer_wiersza in range(len(aktualna_mapa)):
        for numer_kolumny in range(len(aktualna_mapa[numer_wiersza])):
            pole = aktualna_mapa[numer_wiersza][numer_kolumny]

            if pole == "trawa":
                kolor = zielony
            elif pole == "sciezka":
                kolor = brazowy
            elif pole == "woda":
                kolor = niebieski
            elif pole == "dom":
                kolor = szary
            elif pole == "sciana":
                kolor = (80, 80, 80)
            elif pole == "podloga":
                kolor = (210, 180, 140)
            elif pole == "wyjscie":
                kolor = (255, 140, 0)
            else:
                kolor = bialy

            x = numer_kolumny * rozmiar_kafelka
            y = numer_wiersza * rozmiar_kafelka

            pygame.draw.rect(okno, kolor, (x, y, rozmiar_kafelka, rozmiar_kafelka))
            pygame.draw.rect(okno, czarny, (x, y, rozmiar_kafelka, rozmiar_kafelka), 1)


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

        if aktualna_mapa[wiersz][kolumna] in ["woda", "dom", "sciana"]:
            return False

    if lokacja == "zewnatrz":
        prostokat_gracza = pygame.Rect(nowe_x, nowe_y, gracz_szerokosc, gracz_wysokosc)
        prostokat_jakuba = pygame.Rect(jakub_x, jakub_y, jakub_szerokosc, jakub_wysokosc)
        prostokat_michala = pygame.Rect(michal_x, michal_y, michal_szerokosc, michal_wysokosc)

        if prostokat_gracza.colliderect(prostokat_jakuba):
            return False

        if prostokat_gracza.colliderect(prostokat_michala):
            return False

    return True


def czy_gracz_jest_blisko_jakuba():
    if lokacja != "zewnatrz":
        return False

    prostokat_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    prostokat_jakuba = pygame.Rect(jakub_x, jakub_y, jakub_szerokosc, jakub_wysokosc)

    strefa_rozmowy = prostokat_jakuba.inflate(50, 50)

    return prostokat_gracza.colliderect(strefa_rozmowy)


def czy_gracz_jest_blisko_michala():
    if lokacja != "zewnatrz":
        return False

    prostokat_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    prostokat_michala = pygame.Rect(michal_x, michal_y, michal_szerokosc, michal_wysokosc)

    strefa_rozmowy = prostokat_michala.inflate(50, 50)

    return prostokat_gracza.colliderect(strefa_rozmowy)


def czy_gracz_jest_przy_domku():
    if lokacja != "zewnatrz":
        return False

    prostokat_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    strefa_domku = pygame.Rect(180, 180, 220, 180)

    return prostokat_gracza.colliderect(strefa_domku)


def rysuj_dialog():
    pygame.draw.rect(okno, bialy, (40, 500, 720, 80))
    pygame.draw.rect(okno, czarny, (40, 500, 720, 80), 3)

    tekst = font.render(tekst_dialogu, True, czarny)
    okno.blit(tekst, (60, 530))


def rysuj_zadanie():
    tekst = font.render(tekst_zadania, True, czarny)
    okno.blit(tekst, (20, 20))


def rysuj_imie(imie, x, y, szerokosc_postaci):
    tekst = font.render(imie, True, czarny)
    prostokat_tekstu = tekst.get_rect(center=(x + szerokosc_postaci // 2, y - 10))
    okno.blit(tekst, prostokat_tekstu)


def rysuj_podpowiedz():
    if lokacja == "zewnatrz":
        if czy_gracz_jest_blisko_jakuba() or czy_gracz_jest_blisko_michala():
            tekst = font.render("Nacisnij E", True, czarny)
            prostokat_tekstu = tekst.get_rect(center=(szerokosc // 2, 470))
            okno.blit(tekst, prostokat_tekstu)

        elif czy_gracz_jest_przy_domku():
            tekst = font.render("Nacisnij E, aby wejsc", True, czarny)
            prostokat_tekstu = tekst.get_rect(center=(szerokosc // 2, 470))
            okno.blit(tekst, prostokat_tekstu)


    elif lokacja == "dom":

        if czy_gracz_jest_przy_kluczu():

            czy_ma_klucz = True

            tekst_dialogu = "Znalazles klucz!"

            pokaz_dialog = True

        else:

            srodek_x = gracz_x + gracz_szerokosc // 2

            srodek_y = gracz_y + gracz_wysokosc // 2

            kolumna = srodek_x // rozmiar_kafelka

            wiersz = srodek_y // rozmiar_kafelka

            if 0 <= wiersz < len(mapa_dom) and 0 <= kolumna < len(mapa_dom[wiersz]):

                if mapa_dom[wiersz][kolumna] == "wyjscie":
                    lokacja = "zewnatrz"

                    gracz_x = 480

                    gracz_y = 360

                    pokaz_dialog = False
                tekst = font.render("Nacisnij E, aby wyjsc", True, czarny)
                prostokat_tekstu = tekst.get_rect(center=(szerokosc // 2, 470))
                okno.blit(tekst, prostokat_tekstu)

def rysuj_klucz():
    if lokacja == "dom" and not czy_ma_klucz:
        pygame.draw.rect(okno, zolty, (klucz_x, klucz_y, klucz_szerokosc, klucz_wysokosc))

def czy_gracz_jest_przy_kluczu():
    if lokacja != "dom" or czy_ma_klucz:
        return False

    prostokat_gracza = pygame.Rect(gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc)
    prostokat_klucza = pygame.Rect(klucz_x, klucz_y, klucz_szerokosc, klucz_wysokosc)

    strefa_klucza = prostokat_klucza.inflate(20, 20)

    return prostokat_gracza.colliderect(strefa_klucza)

dziala = True
while dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dziala = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if lokacja == "zewnatrz":
                    if czy_gracz_jest_blisko_jakuba():
                        tekst_dialogu = "Jakub: Czesc Łukasz, idz pogadac z Michałem."
                        pokaz_dialog = True
                        rozmowa_z_jakubem = True

                    elif czy_gracz_jest_blisko_michala():
                        tekst_dialogu = "Michał: Hej Łukasz, dobrze cie widziec."
                        pokaz_dialog = True
                        rozmowa_z_michalem = True

                    elif czy_gracz_jest_przy_domku():
                        lokacja = "dom"
                        gracz_x = 160
                        gracz_y = 160
                        pokaz_dialog = False

                    if rozmowa_z_jakubem and rozmowa_z_michalem:
                        tekst_zadania = "Zadanie wykonane!"

                elif lokacja == "dom":
                    srodek_x = gracz_x + gracz_szerokosc // 2
                    srodek_y = gracz_y + gracz_wysokosc // 2

                    kolumna = srodek_x // rozmiar_kafelka
                    wiersz = srodek_y // rozmiar_kafelka

                    if 0 <= wiersz < len(mapa_dom) and 0 <= kolumna < len(mapa_dom[wiersz]):
                        if mapa_dom[wiersz][kolumna] == "wyjscie":
                            lokacja = "zewnatrz"
                            gracz_x = 480
                            gracz_y = 360
                            pokaz_dialog = False

            if event.key == pygame.K_ESCAPE:
                pokaz_dialog = False

    klawisze = pygame.key.get_pressed()

    nowe_x = gracz_x
    nowe_y = gracz_y

    if klawisze[pygame.K_LEFT] and gracz_x > 0:
        nowe_x -= predkosc
    if klawisze[pygame.K_RIGHT] and gracz_x < szerokosc - gracz_szerokosc:
        nowe_x += predkosc
    if klawisze[pygame.K_UP] and gracz_y > 0:
        nowe_y -= predkosc
    if klawisze[pygame.K_DOWN] and gracz_y < wysokosc - gracz_wysokosc:
        nowe_y += predkosc

    if czy_mozna_wejsc(nowe_x, nowe_y):
        gracz_x = nowe_x
        gracz_y = nowe_y

    okno.fill(bialy)
    rysuj_mape(pobierz_aktualna_mape())
    rysuj_zadanie()

    if lokacja == "zewnatrz":
        pygame.draw.rect(okno, fioletowy, (jakub_x, jakub_y, jakub_szerokosc, jakub_wysokosc))
        pygame.draw.rect(okno, zolty, (michal_x, michal_y, michal_szerokosc, michal_wysokosc))

        rysuj_imie("Jakub", jakub_x, jakub_y, jakub_szerokosc)
        rysuj_imie("Michał", michal_x, michal_y, michal_szerokosc)

    rysuj_klucz()

    pygame.draw.rect(okno, czerwony, (gracz_x, gracz_y, gracz_szerokosc, gracz_wysokosc))
    rysuj_imie("Łukasz", gracz_x, gracz_y, gracz_szerokosc)

    rysuj_podpowiedz()

    if pokaz_dialog:
        rysuj_dialog()

    pygame.display.flip()
    zegar.tick(60)

pygame.quit()