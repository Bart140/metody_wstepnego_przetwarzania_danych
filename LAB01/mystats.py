from typing import List, Any


def median(lista: List)-> float | None | Any:
    n = len(lista)
    if(n % 2 != 0):
        return lista[(n+1)/2]
    elif(n % 2 == 0):
        return (lista[(n)/2]+ lista[(n+1)/2])/2
    else:
        print("cos ty wymyslil")

def mean_windsor(lista: List, p: int)->float:
    n = len(lista)
    return sum(list[p+1:n-p])/(n-2*p)

