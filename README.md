# Corona script

[![unittest](https://github.com/Omega1902/corona/actions/workflows/python-unittest.yml/badge.svg?branch=main)](https://github.com/Omega1902/corona/actions/workflows/python-unittest.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Ziel

Aktuell überprüft sehr viele Menschen (so auch ich) annähernd täglich die Corona-Inzidenzzahlen an. Um jedoch genau die Zahlen zu bekommen, die mich wirklich interessieren und das schnell, habe ich dieses Skript geschrieben.

## Vorraussetzungen

Das skript wurde mit python versionen von 3.7 bis 3.10 entwickelt und getestet. Das aiohttp Modul wird zusätzlich benötigt.

```pip install aiohttp```

Für corona_histroy.py werden außerdem die Module matplotlib, numpy, pandas und openpyxl benötigt.

## Danksagung

Danke für das Heise Team, die in ihrer CT Zeitschrift die API erklärt haben. [PHP-Beispiel](http://ct.de/yw1c)

## Lizenz

Dieses Projekt steht unter der GPL
