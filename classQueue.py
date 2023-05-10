class Queue:
    '''Cola implementada utilizando una lista nativa de Python'''
    def __init__(self):
        '''Construye una instancia de la clase Cola'''
        self._items = []
    def enqueue(self, item):
        '''Agrega un elemento recibido como pámetro al final de la Cola'''
        self._items.insert(0, item)
    def dequeue(self):
        '''Elimina un elemento al frente de la Cola y lo retorna'''
        return self._items.pop()
    def peek(self):
        '''Método propio: Retorna el elemento al frente de la Cola sin eliminarlo'''
        return self._items[-1]
    def size(self):
        '''Retorna la cantidad de elementos presentes en la Cola'''
        return len(self._items)
    def isEmpty(self):
        '''Retorna un booleano que indica si la Cola esta vacía o no'''
        return not bool(self._items)
    def search(self,item):
        '''Método propio: Determina si un elemento esta en la cola'''
        return item in self._items
    def copy(self):
        '''Método propio: Retorna una copia de la cola'''
        copia=Queue()
        for item in reversed(self._items):
            copia.enqueue(item)
        return copia
    def clear(self):
        '''Método propio: Vacía la cola, es decir, la deja sin elementos'''
        self._items = []