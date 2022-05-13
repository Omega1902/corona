import logging
from enum import Enum
from typing import Iterable, List, Optional

LOG = logging.getLogger(__name__)

DEUTSCHLAND = "Deutschland"

BW = "Baden-Württemberg"
BAYERN = "Bayern"
BERLIN = "Berlin"
BRANDENBURG = "Brandenburg"
BREMEN = "Bremen"
HAMBURG = "Hamburg"
HESSEN = "Hessen"
MV = "Mecklenburg-Vorpommern"
NIEDERSACHSEN = "Niedersachsen"
NRW = "Nordrhein-Westfalen"
RP = "Rheinland-Pfalz"
SAARLAND = "Saarland"
SACHSEN = "Sachsen"
SA = "Sachsen-Anhalt"
SH = "Schleswig-Holstein"
THURINGEN = "Thüringen"


class Landkreise(Enum):
    AHRWEILER = (144, "LK Ahrweiler")
    AICHACH_FRIEDBERG = (309, "LK Aichach-Friedberg")
    ALB_DONAU_KREIS = (218, "LK Alb-Donau-Kreis")
    ALTENBURGER_LAND = (401, "LK Altenburger Land")
    ALTENKIRCHEN_WESTERWALD = (145, "LK Altenkirchen")
    ALTMARKKREIS_SALZWEDEL = (368, "LK Altmarkkreis Salzwedel")
    ALTOETTING = (226, "LK Altötting")
    ALZEY_WORMS = (169, "LK Alzey-Worms")
    AMBERG = (258, "SK Amberg")
    AMBERG_SULZBACH = (261, "LK Amberg-Sulzbach")
    AMMERLAND = (50, "LK Ammerland")
    ANHALT_BITTERFELD = (369, "LK Anhalt-Bitterfeld")
    ANSBACH_SK = (281, "SK Ansbach")
    ANSBACH_LK = (286, "LK Ansbach")
    ASCHAFFENBURG_SK = (293, "SK Aschaffenburg")
    ASCHAFFENBURG_LK = (296, "LK Aschaffenburg")
    AUGSBURG_SK = (305, "SK Augsburg")
    AUGSBURG_LK = (310, "LK Augsburg")
    AURICH = (51, "LK Aurich", NIEDERSACHSEN)
    BAD_DUERKHEIM = (170, "LK Bad Dürkheim")
    BAD_KISSINGEN = (297, "LK Bad Kissingen")
    BAD_KREUZNACH = (146, "LK Bad Kreuznach")
    BAD_TOELZ_WOLFRATSHAUSEN = (228, "LK Bad Tölz-Wolfratshausen")
    BADEN_BADEN = (192, "SK Baden-Baden")
    BAMBERG_SK = (268, "SK Bamberg")
    BAMBERG_LK = (272, "LK Bamberg")
    BARNIM = (330, "LK Barnim")
    BAUTZEN = (358, "LK Bautzen")
    BAYREUTH_SK = (269, "SK Bayreuth")
    BAYREUTH_LK = (273, "LK Bayreuth")
    BERCHTESGADENER_LAND = (227, "LK Berchtesgadener Land")
    BERGSTRASSE = (121, "LK Bergstraße")
    BERLIN_CHARLOTTENBURG_WILMERSDORF = (405, "SK Berlin Charlottenburg-Wilmersdorf")
    BERLIN_FRIEDRICHSHAIN_KREUZBERG = (414, "SK Berlin Friedrichshain-Kreuzberg")
    BERLIN_LICHTENBERG = (409, "SK Berlin Lichtenberg")
    BERLIN_MARZAHN_HELLERSDORF = (410, "SK Berlin Marzahn-Hellersdorf")
    BERLIN_MITTE = (413, "SK Berlin Mitte", BERLIN)
    BERLIN_NEUKOELLN = (408, "SK Berlin Neukölln")
    BERLIN_PANKOW = (407, "SK Berlin Pankow")
    BERLIN_REINICKENDORF = (404, "SK Berlin Reinickendorf")
    BERLIN_SPANDAU = (411, "SK Berlin Spandau")
    BERLIN_STEGLITZ_ZEHLENDORF = (412, "SK Berlin Steglitz-Zehlendorf")
    BERLIN_TEMPELHOF_SCHOENEBERG = (415, "SK Berlin Tempelhof-Schöneberg")
    BERLIN_TREPTOW_KOEPENICK = (406, "SK Berlin Treptow-Köpenick")
    BERNKASTEL_WITTLICH = (155, "LK Bernkastel-Wittlich")
    BIBERACH = (219, "LK Biberach")
    BIELEFELD = (98, "SK Bielefeld")
    BIRKENFELD = (147, "LK Birkenfeld")
    BOCHUM = (105, "SK Bochum", NRW)
    BODENSEEKREIS = (220, "LK Bodenseekreis")
    BONN = (79, "SK Bonn", NRW)
    BORKEN = (93, "LK Borken")
    BOTTROP = (90, "SK Bottrop")
    BRANDENBURG_HAVEL = (326, "SK Brandenburg a.d.Havel")
    BRAUNSCHWEIG = (17, "SK Braunschweig", NIEDERSACHSEN)
    BREISGAU_HOCHSCHWARZWALD = (205, "LK Breisgau-Hochschwarzwald")
    BREMEN = (62, "SK Bremen", BREMEN)
    BREMERHAVEN = (63, "SK Bremerhaven", BREMEN)
    BURGENLANDKREIS = (371, "LK Burgenlandkreis")
    BOEBLINGEN = (180, "LK Böblingen")
    BOERDE = (370, "LK Börde")
    CALW = (201, "LK Calw")
    CELLE = (34, "LK Celle", NIEDERSACHSEN)
    CHAM = (262, "LK Cham")
    CHEMNITZ = (352, "SK Chemnitz")
    CLOPPENBURG = (52, "LK Cloppenburg")
    COBURG_SK = (270, "SK Coburg")
    COBURG_LK = (274, "LK Coburg")
    COCHEM_ZELL = (148, "LK Cochem-Zell")
    COESFELD = (94, "LK Coesfeld")
    COTTBUS = (327, "SK Cottbus")
    CUXHAVEN = (35, "LK Cuxhaven")
    DACHAU = (229, "LK Dachau")
    DAHME_SPREEWALD = (331, "LK Dahme-Spreewald")
    DARMSTADT = (117, "SK Darmstadt")
    DARMSTADT_DIEBURG = (122, "LK Darmstadt-Dieburg")
    DEGGENDORF = (249, "LK Deggendorf")
    DELMENHORST = (45, "SK Delmenhorst")
    DESSAU_ROSSLAU = (365, "SK Dessau-Roßlau")
    DIEPHOLZ = (28, "LK Diepholz")
    DILLINGEN_DONAU = (311, "LK Dillingen a.d.Donau")
    DINGOLFING_LANDAU = (257, "LK Dingolfing-Landau")
    DITHMARSCHEN = (5, "LK Dithmarschen")
    DONAU_RIES = (317, "LK Donau-Ries")
    DONNERSBERGKREIS = (171, "LK Donnersbergkreis")
    DORTMUND = (106, "SK Dortmund", NRW)
    DRESDEN = (357, "SK Dresden", SACHSEN)
    DUISBURG = (65, "SK Duisburg")
    DUEREN = (83, "LK Düren")
    DUESSELDORF = (64, "SK Düsseldorf")
    EBERSBERG = (230, "LK Ebersberg")
    EICHSFELD = (385, "LK Eichsfeld")
    EICHSTAETT = (231, "LK Eichstätt")
    EIFELKREIS_BITBURG_PRUEM = (156, "LK Bitburg-Prüm")
    # EISENACH = (384, "SK Eisenach")  # does no longer work
    ELBE_ELSTER = (332, "LK Elbe-Elster")
    EMDEN = (46, "SK Emden")
    EMMENDINGEN = (206, "LK Emmendingen")
    EMSLAND = (53, "LK Emsland")
    ENNEPE_RUHR_KREIS = (110, "LK Ennepe-Ruhr-Kreis")
    ENZKREIS = (202, "LK Enzkreis")
    ERDING = (232, "LK Erding")
    ERFURT = (379, "SK Erfurt")
    ERLANGEN = (282, "SK Erlangen")
    ERLANGEN_HOECHSTADT = (287, "LK Erlangen-Höchstadt")
    ERZGEBIRGSKREIS = (353, "LK Erzgebirgskreis")
    ESSEN = (66, "SK Essen")
    ESSLINGEN = (181, "LK Esslingen")
    EUSKIRCHEN = (85, "LK Euskirchen")
    FLENSBURG = (1, "SK Flensburg")
    FORCHHEIM = (275, "LK Forchheim")
    FRANKENTHAL = (159, "SK Frankenthal")
    FRANKFURT_ODER = (328, "SK Frankfurt (Oder)")
    FRANKFURT_AM_MAIN = (118, "SK Frankfurt am Main")
    FREIBURG_BREISGAU = (204, "SK Freiburg i.Breisgau")
    FREISING = (233, "LK Freising")
    FREUDENSTADT = (203, "LK Freudenstadt")
    FREYUNG_GRAFENAU = (250, "LK Freyung-Grafenau")
    FRIESLAND = (54, "LK Friesland")
    FULDA = (137, "LK Fulda")
    FUERSTENFELDBRUCK = (234, "LK Fürstenfeldbruck")
    FUERTH_SK = (283, "SK Fürth")
    FUERTH_LK = (288, "LK Fürth")
    GARMISCH_PARTENKIRCHEN = (235, "LK Garmisch-Partenkirchen")
    GELSENKIRCHEN = (91, "SK Gelsenkirchen")
    GERA = (380, "SK Gera")
    GERMERSHEIM = (172, "LK Germersheim")
    GIESSEN = (131, "LK Gießen")
    GIFHORN = (20, "LK Gifhorn")
    GOSLAR = (21, "LK Goslar")
    GOTHA = (391, "LK Gotha")
    GRAFSCHAFT_BENTHEIM = (55, "LK Grafschaft Bentheim")
    GREIZ = (400, "LK Greiz")
    GROSS_GERAU = (123, "LK Groß-Gerau")
    GOEPPINGEN = (182, "LK Göppingen")
    GOERLITZ = (359, "LK Görlitz")
    GOETTINGEN = (26, "LK Göttingen")
    GUENZBURG = (312, "LK Günzburg")
    GUETERSLOH = (99, "LK Gütersloh")
    HAGEN = (107, "SK Hagen")
    HALLE = (366, "SK Halle")
    HAMBURG = (16, "SK Hamburg", HAMBURG)
    HAMELN_PYRMONT = (29, "LK Hameln-Pyrmont")
    HAMM = (108, "SK Hamm")
    HANNOVER = (27, "Region Hannover", NIEDERSACHSEN, "Hannover")
    HARBURG = (36, "LK Harburg")
    HARZ = (372, "LK Harz")
    HAVELLAND = (333, "LK Havelland")
    HASSBERGE = (299, "LK Haßberge")
    HEIDEKREIS = (41, "LK Heidekreis")
    HEIDELBERG = (196, "SK Heidelberg")
    HEIDENHEIM = (190, "LK Heidenheim")
    HEILBRONN_SK = (185, "SK Heilbronn")
    HEILBRONN_LK = (186, "LK Heilbronn")
    HEINSBERG = (86, "LK Heinsberg")
    HELMSTEDT = (22, "LK Helmstedt")
    HERFORD = (100, "LK Herford")
    HERNE = (109, "SK Herne")
    HERSFELD_ROTENBURG = (138, "LK Hersfeld-Rotenburg")
    HERZOGTUM_LAUENBURG = (6, "LK Herzogtum Lauenburg")
    HILDBURGHAUSEN = (393, "LK Hildburghausen")
    HILDESHEIM = (30, "LK Hildesheim")
    HOCHSAUERLANDKREIS = (111, "LK Hochsauerlandkreis")
    HOCHTAUNUSKREIS = (124, "LK Hochtaunuskreis")
    HOF_SK = (271, "SK Hof")
    HOF_LK = (276, "LK Hof")
    HOHENLOHEKREIS = (187, "LK Hohenlohekreis")
    HOLZMINDEN = (31, "LK Holzminden")
    HOEXTER = (101, "LK Höxter")
    ILM_KREIS = (394, "LK Ilm-Kreis")
    INGOLSTADT = (223, "SK Ingolstadt")
    JENA = (381, "SK Jena")
    JERICHOWER_LAND = (373, "LK Jerichower Land")
    KAISERSLAUTERN_SK = (160, "SK Kaiserslautern")
    KAISERSLAUTERN_LK = (173, "LK Kaiserslautern")
    KARLSRUHE_SK = (193, "SK Karlsruhe")
    KARLSRUHE_LK = (194, "LK Karlsruhe")
    KASSEL_SK = (136, "SK Kassel")
    KASSEL_LK = (139, "LK Kassel")
    KAUFBEUREN = (306, "SK Kaufbeuren")
    KELHEIM = (251, "LK Kelheim")
    KEMPTEN = (307, "SK Kempten")
    KIEL = (2, "SK Kiel")
    KITZINGEN = (300, "LK Kitzingen")
    KLEVE = (74, "LK Kleve")
    KOBLENZ = (143, "SK Koblenz")
    KONSTANZ = (211, "LK Konstanz")
    KREFELD = (67, "SK Krefeld")
    KRONACH = (277, "LK Kronach")
    KULMBACH = (278, "LK Kulmbach")
    KUSEL = (174, "LK Kusel")
    KYFFHAEUSERKREIS = (389, "LK Kyffhäuserkreis")
    KOELN = (80, "SK Köln", NRW)
    LAHN_DILL_KREIS = (132, "LK Lahn-Dill-Kreis")
    LANDAU = (161, "SK Landau i.d.Pfalz")
    LANDSBERG = (236, "LK Landsberg a.Lech")
    LANDSHUT_SK = (246, "SK Landshut")
    LANDSHUT_LK = (252, "LK Landshut")
    LEER = (56, "LK Leer")
    LEIPZIG_SK = (362, "SK Leipzig")
    LEIPZIG_LK = (363, "LK Leipzig")
    LEVERKUSEN = (81, "SK Leverkusen")
    LICHTENFELS = (279, "LK Lichtenfels")
    LIMBURG_WEILBURG = (133, "LK Limburg-Weilburg")
    LINDAU = (314, "LK Lindau")
    LIPPE = (102, "LK Lippe")
    LUDWIGSBURG = (183, "LK Ludwigsburg")
    LUDWIGSHAFEN = (162, "SK Ludwigshafen")
    LUDWIGSLUST_PARCHIM = (351, "LK Ludwigslust-Parchim")
    LOERRACH = (212, "LK Lörrach")
    LUEBECK = (3, "SK Lübeck", SH)
    LUECHOW_DANNENBERG = (37, "LK Lüchow-Dannenberg")
    LUENEBURG = (38, "LK Lüneburg")
    MAGDEBURG = (367, "SK Magdeburg")
    MAIN_KINZIG_KREIS = (125, "LK Main-Kinzig-Kreis")
    MAIN_SPESSART = (302, "LK Main-Spessart")
    MAIN_TAUBER_KREIS = (189, "LK Main-Tauber-Kreis")
    MAIN_TAUNUS_KREIS = (126, "LK Main-Taunus-Kreis")
    MAINZ = (163, "SK Mainz")
    MAINZ_BINGEN = (177, "LK Mainz-Bingen")
    MANNHEIM = (197, "SK Mannheim")
    MANSFELD_SUEDHARZ = (374, "LK Mansfeld-Südharz")
    MARBURG_BIEDENKOPF = (134, "LK Marburg-Biedenkopf")
    MAYEN_KOBLENZ = (149, "LK Mayen-Koblenz")
    MECKLENBURGISCHE_SEENPLATTE = (346, "LK Mecklenburgische Seenplatte")
    MEISSEN = (360, "LK Meißen")
    MEMMINGEN = (308, "SK Memmingen")
    MERZIG_WADERN = (320, "LK Merzig-Wadern")
    METTMANN = (75, "LK Mettmann")
    MIESBACH = (237, "LK Miesbach")
    MILTENBERG = (301, "LK Miltenberg")
    MINDEN_LUEBBECKE = (103, "LK Minden-Lübbecke")
    MITTELSACHSEN = (354, "LK Mittelsachsen")
    MAERKISCH_ODERLAND = (334, "LK Märkisch-Oderland")
    MAERKISCHER_KREIS = (112, "LK Märkischer Kreis")
    MOENCHENGLADBACH = (68, "SK Mönchengladbach")
    MUEHLDORF_INN = (238, "LK Mühldorf a.Inn")
    MUELHEIM_AN_DER_RUHR = (69, "SK Mülheim a.d.Ruhr")
    MUENCHEN_SK = (224, "SK München", BAYERN)
    MUENCHEN_LK = (239, "LK München", BAYERN)
    MUENSTER = (92, "SK Münster")
    NECKAR_ODENWALD_KREIS = (198, "LK Neckar-Odenwald-Kreis")
    NEU_ULM = (313, "LK Neu-Ulm")
    NEUBURG_SCHROBENHAUSEN = (240, "LK Neuburg-Schrobenhausen")
    NEUMARKT_OPF = (263, "LK Neumarkt i.d.OPf.")
    NEUMUENSTER = (4, "SK Neumünster")
    NEUNKIRCHEN = (321, "LK Neunkirchen")
    NEUSTADT_AISCH_BAD_WINDSHEIM = (290, "LK Neustadt a.d.Aisch-Bad Windsheim")
    NEUSTADT_WALDNAAB = (264, "LK Neustadt a.d.Waldnaab")
    NEUSTADT_WEINSTRASSE = (164, "SK Neustadt a.d.Weinstraße")
    NEUWIED = (150, "LK Neuwied")
    NIENBURG_WESER = (32, "LK Nienburg (Weser)")
    NORDFRIESLAND = (7, "LK Nordfriesland", SH)
    NORDHAUSEN = (386, "LK Nordhausen")
    NORDSACHSEN = (364, "LK Nordsachsen")
    NORDWESTMECKLENBURG = (349, "LK Nordwestmecklenburg")
    NORTHEIM = (23, "LK Northeim")
    NUERNBERG = (284, "SK Nürnberg")
    NUERNBERGER_LAND = (289, "LK Nürnberger Land")
    OBERALLGAEU = (318, "LK Oberallgäu")
    OBERBERGISCHER_KREIS = (87, "LK Oberbergischer Kreis", NRW)
    OBERHAUSEN = (70, "SK Oberhausen")
    OBERHAVEL = (335, "LK Oberhavel")
    OBERSPREEWALD_LAUSITZ = (336, "LK Oberspreewald-Lausitz")
    ODENWALDKREIS = (127, "LK Odenwaldkreis")
    ODER_SPREE = (337, "LK Oder-Spree")
    OFFENBACH_LK = (128, "LK Offenbach")
    OFFENBACH_SK = (119, "SK Offenbach")
    OLDENBURG_LK = (57, "LK Oldenburg")
    OLDENBURG_SK = (47, "SK Oldenburg")
    OLPE = (113, "LK Olpe")
    ORTENAUKREIS = (207, "LK Ortenaukreis")
    OSNABRUECK_SK = (48, "SK Osnabrück")
    OSNABRUECK_LK = (58, "LK Osnabrück")
    OSTALBKREIS = (191, "LK Ostalbkreis")
    OSTALLGAEU = (315, "LK Ostallgäu")
    OSTERHOLZ = (39, "LK Osterholz")
    OSTHOLSTEIN = (8, "LK Ostholstein", SH)
    OSTPRIGNITZ_RUPPIN = (338, "LK Ostprignitz-Ruppin")
    PADERBORN = (104, "LK Paderborn")
    PASSAU_SK = (247, "SK Passau")
    PASSAU_LK = (253, "LK Passau")
    PEINE = (24, "LK Peine")
    PFAFFENHOFEN_ILM = (241, "LK Pfaffenhofen a.d.Ilm")
    PFORZHEIM = (200, "SK Pforzheim")
    PINNEBERG = (9, "LK Pinneberg")
    PIRMASENS = (165, "SK Pirmasens")
    PLOEN = (10, "LK Plön")
    POTSDAM = (329, "SK Potsdam")
    POTSDAM_MITTELMARK = (339, "LK Potsdam-Mittelmark")
    PRIGNITZ = (340, "LK Prignitz")
    RASTATT = (195, "LK Rastatt")
    RAVENSBURG = (221, "LK Ravensburg")
    RECKLINGHAUSEN = (95, "LK Recklinghausen")
    REGEN = (254, "LK Regen")
    REGENSBURG_SK = (259, "SK Regensburg", BAYERN)
    REGENSBURG_LK = (265, "LK Regensburg", BAYERN)
    REGIONALVERBAND_SAARBRUECKEN = (319, "LK Stadtverband Saarbrücken")
    REMS_MURR_KREIS = (184, "LK Rems-Murr-Kreis")
    REMSCHEID = (71, "SK Remscheid")
    RENDSBURG_ECKERNFOERDE = (11, "LK Rendsburg-Eckernförde")
    REUTLINGEN = (214, "LK Reutlingen")
    RHEIN_ERFT_KREIS = (84, "LK Rhein-Erft-Kreis")
    RHEIN_HUNSRUECK_KREIS = (151, "LK Rhein-Hunsrück-Kreis")
    RHEIN_KREIS_NEUSS = (76, "LK Rhein-Kreis Neuss")
    RHEIN_LAHN_KREIS = (152, "LK Rhein-Lahn-Kreis")
    RHEIN_NECKAR_KREIS = (199, "LK Rhein-Neckar-Kreis")
    RHEIN_PFALZ_KREIS = (176, "LK Rhein-Pfalz-Kreis")
    RHEIN_SIEG_KREIS = (89, "LK Rhein-Sieg-Kreis")
    RHEINGAU_TAUNUS_KREIS = (129, "LK Rheingau-Taunus-Kreis")
    RHEINISCH_BERGISCHER_KREIS = (88, "LK Rheinisch-Bergischer Kreis")
    RHOEN_GRABFELD = (298, "LK Rhön-Grabfeld")
    ROSENHEIM_SK = (225, "SK Rosenheim")
    ROSENHEIM_LK = (242, "LK Rosenheim")
    ROSTOCK_SK = (344, "SK Rostock")
    ROSTOCK_LK = (347, "LK Rostock")
    ROTENBURG_WUEMME = (40, "LK Rotenburg (Wümme)")
    ROTH = (291, "LK Roth")
    ROTTAL_INN = (255, "LK Rottal-Inn")
    ROTTWEIL = (208, "LK Rottweil")
    SAALE_HOLZLAND_KREIS = (398, "LK Saale-Holzland-Kreis")
    SAALE_ORLA_KREIS = (399, "LK Saale-Orla-Kreis")
    SAALEKREIS = (375, "LK Saalekreis")
    SAALFELD_RUDOLSTADT = (397, "LK Saalfeld-Rudolstadt")
    SAARLOUIS = (322, "LK Saarlouis")
    SAARPFALZ_KREIS = (323, "LK Saarpfalz-Kreis")
    SALZGITTER = (18, "SK Salzgitter")
    SALZLANDKREIS = (376, "LK Salzlandkreis")
    SCHAUMBURG = (33, "LK Schaumburg")
    SCHLESWIG_FLENSBURG = (12, "LK Schleswig-Flensburg")
    SCHMALKALDEN_MEININGEN = (390, "LK Schmalkalden-Meiningen")
    SCHWABACH = (285, "SK Schwabach")
    SCHWALM_EDER_KREIS = (140, "LK Schwalm-Eder-Kreis")
    SCHWANDORF = (266, "LK Schwandorf")
    SCHWARZWALD_BAAR_KREIS = (209, "LK Schwarzwald-Baar-Kreis")
    SCHWEINFURT_SK = (294, "SK Schweinfurt")
    SCHWEINFURT_LK = (303, "LK Schweinfurt")
    SCHWERIN = (345, "SK Schwerin")
    SCHWAEBISCH_HALL = (188, "LK Schwäbisch Hall")
    SEGEBERG = (13, "LK Segeberg")
    SIEGEN_WITTGENSTEIN = (114, "LK Siegen-Wittgenstein")
    SIGMARINGEN = (222, "LK Sigmaringen")
    SOEST = (115, "LK Soest")
    SOLINGEN = (72, "SK Solingen")
    SONNEBERG = (396, "LK Sonneberg")
    SPEYER = (166, "SK Speyer")
    SPREE_NEISSE = (341, "LK Spree-Neiße")
    ST_WENDEL = (324, "LK Sankt Wendel")
    STADE = (42, "LK Stade")
    STARNBERG = (243, "LK Starnberg")
    STEINBURG = (14, "LK Steinburg")
    STEINFURT = (96, "LK Steinfurt")
    STENDAL = (377, "LK Stendal")
    STORMARN = (15, "LK Stormarn")
    STRAUBING = (248, "SK Straubing")
    STRAUBING_BOGEN = (256, "LK Straubing-Bogen")
    STUTTGART = (179, "SK Stuttgart")
    STAEDTEREGION_AACHEN = (82, "StädteRegion Aachen")
    SUHL = (382, "SK Suhl")
    SAECHSISCHE_SCHWEIZ_OSTERZGEBIRGE = (361, "LK Sächsische Schweiz-Osterzgebirge")
    SOEMMERDA = (392, "LK Sömmerda")
    SUEDLICHE_WEINSTRASSE = (175, "LK Südliche Weinstraße")
    SUEDWESTPFALZ = (178, "LK Südwestpfalz")
    TELTOW_FLAEMING = (342, "LK Teltow-Fläming")
    TIRSCHENREUTH = (267, "LK Tirschenreuth")
    TRAUNSTEIN = (244, "LK Traunstein")
    TRIER = (154, "SK Trier")
    TRIER_SAARBURG = (158, "LK Trier-Saarburg")
    TUTTLINGEN = (210, "LK Tuttlingen")
    TUEBINGEN = (215, "LK Tübingen")
    UCKERMARK = (343, "LK Uckermark")
    UELZEN = (43, "LK Uelzen")
    ULM = (217, "SK Ulm")
    UNNA = (116, "LK Unna")
    UNSTRUT_HAINICH_KREIS = (388, "LK Unstrut-Hainich-Kreis")
    UNTERALLGAEU = (316, "LK Unterallgäu")
    VECHTA = (59, "LK Vechta")
    VERDEN = (44, "LK Verden")
    VIERSEN = (77, "LK Viersen")
    VOGELSBERGKREIS = (135, "LK Vogelsbergkreis")
    VOGTLANDKREIS = (355, "LK Vogtlandkreis")
    VORPOMMERN_GREIFSWALD = (350, "LK Vorpommern-Greifswald")
    VORPOMMERN_RUEGEN = (348, "LK Vorpommern-Rügen")
    VULKANEIFEL = (157, "LK Vulkaneifel")
    WALDECK_FRANKENBERG = (141, "LK Waldeck-Frankenberg")
    WALDSHUT = (213, "LK Waldshut")
    WARENDORF = (97, "LK Warendorf")
    WARTBURGKREIS = (387, "LK Wartburgkreis")
    WEIDEN_OPF = (260, "SK Weiden i.d.OPf.")
    WEILHEIM_SCHONGAU = (245, "LK Weilheim-Schongau")
    WEIMAR = (383, "SK Weimar")
    WEIMARER_LAND = (395, "LK Weimarer Land")
    WEISSENBURG_GUNZENHAUSEN = (292, "LK Weißenburg-Gunzenhausen")
    WERRA_MEISSNER_KREIS = (142, "LK Werra-Meißner-Kreis")
    WESEL = (78, "LK Wesel")
    WESERMARSCH = (60, "LK Wesermarsch")
    WESTERWALDKREIS = (153, "LK Westerwaldkreis")
    WETTERAUKREIS = (130, "LK Wetteraukreis")
    WIESBADEN = (120, "SK Wiesbaden")
    WILHELMSHAVEN = (49, "SK Wilhelmshaven")
    WITTENBERG = (378, "LK Wittenberg")
    WITTMUND = (61, "LK Wittmund")
    WOLFENBUETTEL = (25, "LK Wolfenbüttel", NIEDERSACHSEN)
    WOLFSBURG = (19, "SK Wolfsburg", NIEDERSACHSEN)
    WORMS = (167, "SK Worms")
    WUNSIEDEL_FICHTELGEBIRGE = (280, "LK Wunsiedel i.Fichtelgebirge")
    WUPPERTAL = (73, "SK Wuppertal")
    WUERZBURG_SK = (295, "SK Würzburg")
    WUERZBURG_LK = (304, "LK Würzburg")
    ZOLLERNALBKREIS = (216, "LK Zollernalbkreis")
    ZWEIBRUECKEN = (168, "SK Zweibrücken")
    ZWICKAU = (356, "LK Zwickau")

    def __init__(self, lk_id: int, lk_name: str, land: Optional[str] = "", name: Optional[str] = None):
        """Inits a Landkreis.

        Args:
            id (int): ID used by the rki dashboard. Needs to be unique.
            lk_name (str): Landkreis name used by the rki dashboard. Needs to be unique.
            land (Optional[str]): Land where landkreis is located. Defaults to empty string.
            name (Optional[str]): String to display for user. Default will use lk_name and remove prefix 'LK ' and 'SK '
        """
        self._lk_name = lk_name
        if name is None:
            if lk_name.startswith("LK ") or lk_name.startswith("SK "):
                self._name = lk_name[3:]
            else:
                self._name = lk_name
        else:
            self._name = name
        self._value_ = lk_id
        self._land = land

    @property
    def name(self):
        return self._name

    @property
    def land(self):
        if not self._land:
            LOG.warning("%s does not have a land configured!", self.lk_name)
        return self._land

    @property
    def lk_name(self):
        return self._lk_name

    @property
    def id(self):
        return self._value_

    @staticmethod
    def find_by_id(lk_id) -> Optional["Landkreise"]:
        result = [lk for lk in Landkreise if lk.id == lk_id]
        return None if len(result) != 1 else result[0]

    @classmethod
    def find_by_ids(cls, lk_ids: Iterable[int]) -> List["Landkreise"]:
        """Will return a list of all Landkreise of the given ids.
        If an id does not exist, the None paramter returned by find_by_id will not be contained in this list.
        If lk_ids is None or does not contain a valid lk_id, the result will be an empty list.

        Args:
            lk_ids (Iterable[int]): lk_ids to convert to Landkreise

        Returns:
            list[Landkreise]: List of Landkreise
        """
        result = []
        for lk_id in lk_ids:
            landkreis = cls.find_by_id(lk_id)
            if landkreis is not None:
                result.append(landkreis)
        return result

    @staticmethod
    def find_by_lk_name(lk_name) -> Optional["Landkreise"]:
        result = [lk for lk in Landkreise if lk.lk_name == lk_name]
        return None if len(result) != 1 else result[0]

    @classmethod
    def find_by_lk_names(cls, lk_names: Iterable[str]) -> List["Landkreise"]:
        """Will return a list of all Landkreise of the given lk_names.
        If an lk_name does not exist, the None paramter returned by find_by_lk_name will not be contained in this list.
        If lk_names is None or does not contain a valid lk_name, the result will be an empty list.

        Args:
            lk_names (Iterable[str]): lk_names to convert to Landkreise

        Returns:
            list[Landkreise]: List of Landkreise
        """
        result = []
        for lk_name in lk_names:
            landkreis = cls.find_by_lk_name(lk_name)
            if landkreis is not None:
                result.append(landkreis)
        return result

    def __str__(self):
        return self.name
