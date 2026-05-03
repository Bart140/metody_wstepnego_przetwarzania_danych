# ZADANIE 08: Analiza Głównych Składowych (PCA) - Redukcja Wymiarowości

## Cel ćwiczenia
Głównym celem tego ćwiczenia jest zbadanie problemu wysokiej wymiarowości ("klątwy wymiarowości") i zapoznanie się w praktyce z jedną z najpopularniejszych metod redukcji wymiarowości – **Analizą Głównych Składowych (Principal Component Analysis - PCA)**.

W przeciwieństwie do selekcji cech (wybierania konkretnych istniejących wymiarów), PCA to transformacja polegająca na poszukiwaniu zupełnie nowych, sztucznych osi (składowych głównych) w danych, które zachowują jak najwięcej oryginalnej wariancji, pozwalając tym samym na radykalne skompresowanie informacji i zredukowanie rozmiaru zbioru danych.

## Zadania do wykonania w środowisku Jupyter Notebook
1. **Wczytanie zbioru danych:** Załadowanie bazy danych na temat jakości białego wina (`winequality-white.csv`).
2. **Podział i standaryzacja danych:** 
   - Wyodrębnienie cech analitycznych ($X$) i zmiennej docelowej opisującej jakość wina ($y$).
   - Przeskalowanie danych wejściowych za pomocą obiektu `StandardScaler`. Standaryzacja jest **bezwzględnie konieczna**, ponieważ algorytm PCA opiera się na analizie wariancji. Jeżeli różne cechy posiadają różną skalę (np. tysiące względem ułamków dziesiętnych), wyniki będą całkowicie zdominowane przez te liczbowo większe w oryginalnej dziedzinie.
3. **Analiza PCA:** 
   - Aplikacja estymatora `PCA` i zredukowanie wszystkich kilkunastu cech oryginalnych do zaledwie **2 składowych głównych** (`n_components=2`).
   - Porównanie wymiarów przed i po transformacji. Macierz przed kompresją jest długa, szeroka i wysoce skorelowana. Po zastosowaniu rzutowania przestrzennego otrzymujemy całkowicie nowe wartości w zupełnie innej skali.
4. **Obliczenie wariancji składowych i wizualizacja:**
   - Wyświetlenie rozkładu punktów z użyciem nowo wygenerowanych "Principal Component 1" oraz "Principal Component 2". Pozwala to na prezentację wielowymiarowego układu próbek w zaledwie dwóch wymiarach na wykresie.
   - Odczyt i weryfikacja statystyki `explained_variance_ratio_`. Analiza pozwala stwierdzić ile sumarycznie procent całkowitej, oryginalnej informacji informacyjnej z wielu cech zachowało się po sprowadzeniu całego zbioru do dwóch sztucznych składowych.

## Wnioski z uzyskanych wyników
Dzięki algorytmowi PCA i skompresowaniu danych odciążyliśmy potencjalny model uczący z kilkunastu zmiennych, które w przeciwnym razie byłyby wykorzystane podczas trenowania, przyśpieszając drastycznie ten proces.
Nawet 2 nowo zdefiniowane składowe (Component 1 i 2) pozwalają z zachowaniem dość wysokiej dawki wariancji analizować podział win pod kątem oceny końcowej, a wszystko to bez straty fundamentalnego kontekstu ogólnych danych. Składowe PCA w procesie inżynierii cech pozostają ze sobą nieskorelowane (są ortogonalne), co eliminuje dodatkowo powszechny problem wielowspółliniowości.
