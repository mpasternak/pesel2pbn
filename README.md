# pesel2pbn
Program działający pod Windows, do konwersji wielu numerów PESEL na identyfikatory PBN ID używane przez system [POL-on](http://polon.nauka.gov.pl/) i [Polską Bibliografię Naukową](https://pbn.nauka.gov.pl/).

Program działa na komputerze lokalnym, wykorzystując [publiczne API Polskiej Bibliografii Naukowej](https://pbn.nauka.gov.pl/help/pl/specyfikacje-techniczne/specyfikacja-publicznego-api).

Numery PESEL wysyłane są do PBN szyfrowanym protokołem HTTPS. 

Celem istnienia programu jest to, aby osoby zajmujące się przetwarzaniem danych osobowych mogły skorzystać z niego celem zamiany PESELi na PBN ID i taką informację (czyli identyfikator PBN) wysyłać dalej. W ten sposób numery PESEL nie są wysyłane w sposób zabezpieczony nieadekwatnie. 

Oprogramowanie PESEL2PBN działa pod Windows 7 i wyższych.

Możliwe jest uruchomienie programu pod Linux lub Mac OS X. 
