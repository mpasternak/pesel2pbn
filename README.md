# pesel2pbn

![travis-ci status builda](https://travis-ci.org/mpasternak/pesel2pbn.svg)

Program działający pod Windows, do konwersji wielu numerów PESEL na identyfikatory PBN ID używane przez system POL-on i Polską Bibliografię Naukową.

Program działa na komputerze lokalnym, wykorzystując publiczne API Polskiej Bibliografii Naukowej, https://pbn.nauka.gov.pl/help/pl/specyfikacje-techniczne/specyfikacja-publicznego-api

Numery PESEL wysyłane są do PBN szyfrowanym protokołem HTTPS. 

Celem istnienia programu jest to, aby osoby zajmujące się przetwarzaniem danych osobowych mogły skorzystać z niego celem zamiany PESELi na PBN ID i taką informację (czyli identyfikator PBN) wysyłać dalej. W ten sposób numery PESEL nie są wysyłane w sposób zabezpieczony nieadekwatnie. 

Praca z programem może odbywać się wg następującego schematu:
 - pozyskanie tokenu autoryzacyjnego z [PBN](http://pbn.nauka.gov.pl)
 - wybranie listy kodów PESEL z zewnętrznego źródła danych (np. zaznaczenie ich w arkuszu kalkulacyjnym lub bazie danych i skopiowanie do schowka systemu operacyjnego)
 - uruchomienie programu pesel2pbn,
 - wpisanie tokenu autoryzacyjnego, 
 - wklejenie numerów PESEL do odpowiedniego pola,
 - kliknięcie przycisku "Wykonaj",
 - kliknięcie przycisku "Skopiuj PBN IDs do schowka"
 - tak pozyskane numery PBN można przekleić np. do arkusza kalkulacyjnego lub bazy danych.

Oprogramowanie PESEL2PBN działa pod Windows 7 i wyższych.

Możliwe jest uruchomienie programu pod Linux lub Mac OS X. 

## Bezpieczeństwo

Program zapisuje wartosć token w Rejestrze systemu operacyjnego Windows.

Program *nie* *zapisuje* nigdzie przetwarzanych numerów PESEL oraz PBN, sa one przetrzymywane w pamieci. 

Numery PESEL do PBN przesylane sa za pomoca protokolu HTTPS, czyli sa zaszyfrowane podczas przesylania ich w siec. 
