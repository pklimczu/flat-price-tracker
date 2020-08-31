# flat-price-tracker
Aplikacja do monitorowania cen mieszkań na podstawie alertów mailowych z serwisu OtoDom.

## Sposób użycia

  0. Zasubskrybować alerty w serwisie OtoDom na wybrany adres e-mail. Utworzyć wirtualne środowisko Pythona i zainstalować zależności z pliku `requirements.txt`.

  1. Aktywować GMail API (https://developers.google.com/gmail/api/quickstart/python). Pobrać plik `credentials.json` i umieścić go w folderze `secret`. Uruchomić `secret.py` w celu uzyskania tokenu (`token.pickle`). Token posłuży do autoryzacji i uwierzytelnienia w usługach Google.
  
  2. Aplikację można umieścić na serwerze, używając wiedzy z tego poradnika: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04#step-6-%E2%80%94-configuring-nginx-to-proxy-requests
  
  3. Głównym plikiem jest `controller.py` - odpowiada za parsowanie maili, parsowanie stron z ofertami, utrzymywanie historii sprawdzanych ofert. `scheduler.py` służy do cyklicznego uruchamiania funkcji do sprawdzania poczty i aktualizacji statusu ofert.

**Przykładowe działanie:**
https://flat-price.pklimczu.pl/

![screenshot](https://i.imgur.com/3epS16V.png)
