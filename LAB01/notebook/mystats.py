from typing import List, Any, Sequence


def median(lista: Sequence[Any]) -> float:
    """
    Oblicza medianę z przekazanej listy wartości numerycznych.

    :param lista: lista wartości numerycznych
    :return: mediana
    """

    posortowana = sorted(lista)
    n = len(posortowana)

    if n % 2 != 0:
        return float(posortowana[n // 2])
    else:
        return (posortowana[n // 2 - 1] + posortowana[n // 2]) / 2.0


def trimmed_mean(lista: Sequence[Any], p: int) -> float:
    """
    Oblicza średnią ucinaną (trimmed mean) z parametrem p.
    Odcina p elementów z każdego końca posortowanej listy.

    :param lista: lista wartości numerycznych
    :param p: liczba elementów odcinanych z każdego końca (p >= 0)
    :return: średnia ucięta
    """
    n = len(lista)
    if 2 * p >= n:
        raise ValueError(
            f"Parametr p={p} jest za duży – po ucięciu nie zostają żadne elementy "
            f"(długość listy: {n})."
        )

    posortowana: List[Any] = sorted(lista)
    ucięta: List[Any] = [posortowana[i] for i in range(p, n - p)]
    return sum(ucięta) / len(ucięta)


def main():
    """ tu uruchamiaj kod testowy """
    lista_parzysta = [3, 1, 4, 1, 5, 9, 2, 6]
    lista_nieparzysta = [7, 2, 10, 9, 1]
    lista_jedna = [42]

    print(f"Lista (parzysta):    {sorted(lista_parzysta)}, mediana = {median(lista_parzysta)}")
    print(f"Lista (nieparzysta): {sorted(lista_nieparzysta)}, mediana = {median(lista_nieparzysta)}")
    print(f"Lista jednoelementowa: [{lista_jedna[0]}], mediana = {median(lista_jedna)}")

    try:
        median([])
    except ValueError as e:
        print(f"Pusta lista -> ValueError: {e}")

    try:
        median([1, "a", 3])
    except ValueError as e:
        print(f"Wartosci nienumeryczne -> ValueError: {e}")

    print("\n=== Zadanie 2: trimmed_mean ===")
    dane = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
    print(f"Dane: {dane}")
    for p in [0, 1, 2, 3]:
        print(f"  p={p} -> trimmed_mean = {trimmed_mean(dane, p):.4f}")

    try:
        trimmed_mean(dane, p=5)
    except ValueError as e:
        print(f"  p=5 -> ValueError: {e}")


if __name__ == '__main__':
    main()