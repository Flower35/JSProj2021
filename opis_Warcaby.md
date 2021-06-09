# 5. Warcaby

## Opis zadania

 * Okno z <u>siatką przycisków</u> <b>8x8</b> oraz <u>przyciskiem do resetowania gry</u>.

 * Przyciski reprezentują pola planszy do gry w warcaby.
   * <b>Pola puste</b>: <u>przyciski bez tekstu</u>.
   * Pola z pionkami <b>gracza pierwszego</b>: <u>przycisk z tekstem „<b>`C`</b>”</u>.
   * Pola z pionkami <b>gracza drugiego</b>: <u>przycisk z tekstem „<b>`B`</b>”</u>.
   * <b>Damki</b> oznaczane są <u>dodatkową literą „<b>`d`</b>”</u> („<i>`Cd`</i>”, „<i>`Bd`</i>”).

 * Nad planszą wyświetlana jest informacja: „<b>`Tura gracza 1`</b>” lub „<b>`Tura gracza 2`</b>”.

 * Gracz wybiera pionka (<i>tekst pola zmienia się z „<b>`C`</b>” na „<b>`[C]`</b>” lub z „<b>`B`</b>” na „<b>`[B]`</b>”</i>), a potem pole na które chce wykonać ruch. Jeśli ruch jest dozwolony, pionek jest przestawiany. Jeśli nie, to wyświetlany jest komunikat: „<b>`ruch niedozwolony`</b>”.

 * Zasady jak w dowolnym wariancie gry „<b>Warcaby</b>”: [https://pl.wikipedia.org/wiki/Warcaby]. Zwykłe pionki i damki mają być obiektami <u>dwóch różnych klas</u> dziedziczących po klasie „<b>`Pionek`</b>”.

 * Gdy gra się skończy, wyświetlane jest okienko z napisem „<b>`Wygrał gracz 1`</b>” lub „<b>`Wygrał gracz 2`</b>” – oczywiśie zależnie kto wygrał grę. <u>Możliwe jest zresetowanie planszy bez zamykania głównego okna</u>.

## Testy
1. Wykonanie po dwa ruchy przez każdego z graczy.
2. Niepowodzenie błędnego ruchu pionkiem.
3. Wykonanie bicia pojedynczego pionka.
4. Wykonanie bicia przynajmniej dwóch pionków.
5. Zamiana pionka w damkę.
6. Bicie damką.
7. Wygrana gracza grającego czarnymi pionkami.
8. Rozpoczęcie nowej gry po zwycięstwie jednego z graczy.

<i>Wskazane jest przygotowanie specjalnych początkowych rozstawień pionków dla testów **[4]**, **[5]**, **[6]**, **[7]**, **[8]**.</i>
