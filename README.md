# Dzwon Audytu / Audit Bell

Statyczne archiwum Roberta Jordana: polskie publikacje źródłowe oraz angielskie strony i robocze tłumaczenia do przeglądu. Strona działa w GitHub Pages pod `/dzwon-audytu/`; nie wymaga instalowania zależności do wyświetlania.

## Wersje językowe

- Polski: `index.html`, `teksty/`, `kontakt/`, `prawo-do-komentarza/`, `dokumenty/`.
- English: `en/`, including `en/articles/`, `en/readings/`, `en/pdf/` and `en/documents/`.
- `pdf/` oraz `zrodla/` zawierają zachowane polskie oryginały i dotychczasowe pakiety archiwalne. Angielskie wydania do czytania nie zastępują oryginałów: ich uwagi opisują zakres przekładu, datę źródła oraz reprodukcje pozostające w polskim PDF-ie.
- `dokumenty/documents.json` jest spisem plików do pobrania wraz z językiem, statusem, rozmiarem i SHA-256.

## Kontrola przed publikacją

Po zmianie plików uruchom:

```sh
python3 tools/update_manifest.py
python3 tools/check_site.py
```

Manifest nie zawiera własnego hasha. Przed zatwierdzeniem nowej publikacji sprawdź również treść, załączniki i zakres udostępnienia. Istnienie dokumentu w zbiorze roboczym nie powoduje automatycznie dodania go do publicznego archiwum.

Podgląd lokalny: uruchom `python3 -m http.server 8000 --directory ..` w katalogu repozytorium i otwórz `http://localhost:8000/dzwon-audytu/`.

GitHub Pages publikuje gałąź skonfigurowaną w ustawieniach repozytorium. Samo utworzenie pull requestu nie zmienia strony produkcyjnej. Plik `_headers` pozostaje częścią wcześniejszego archiwum; jego obecność nie dowodzi, że GitHub Pages stosuje te nagłówki HTTP.

## English

This is Robert Jordan's static public archive. Polish source publications remain available alongside English overview pages and draft reading translations. Each translation states its source date and limitations. Public downloads are listed with language, status, size and SHA-256. Run the two Python commands above after changing files; review content before publishing new documents.
