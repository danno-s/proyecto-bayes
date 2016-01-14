#!/usr/bin/python


# Genera tuplas de tamaño 'repeat' con los índices consecutivos extraidos de 'indices'.


def consecutiveIdxs(indices, repeat):
    for i in indices[:-repeat+1]:
        yield tuple(x for x in range(i,i+repeat))

# Generador de las subsecuencias posibles a partir de una sesión.


def subsequences(iterable):
    pool=tuple(iterable)
    n= len(pool)
    if n > 1:
        for r in range(2,n):
            inGen = (x for x in consecutiveIdxs(range(n), repeat=r))
            for indices in inGen:
                yield ' '.join(tuple(pool[i] for i in indices))

    yield ' '.join(pool)

# Funcion que verifica si una subsecuencia 'shortest' esta contenida dentro de la subsecuencia 'longest'.
# Si son iguales, retorna False.


def contains(shortest, longest):
    if shortest == longest:
        return False
    for i in range(len(longest)-len(shortest)+1):
        for j in range(len(shortest)):
            if longest[i+j] != shortest[j]:
                break
        else:
            return True
    return False

# Funcion que verifica si una secuencia 'item' esta subcontenida dentro de algun elemento
# de la lista de secuencias 'iterable'.


def isSubContained(item, iterable):
    for i,val in enumerate(iterable):
        if contains(item,val):
            return True
    return False