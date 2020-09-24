
class BagOfWords:
    def __init__(self, text=None, values=None):
        if text == "": # Recibe un diccionario
            self.values = values
        else: # Recibe un texto a convertir en diccionario
            self.values = string_to_bag_of_words(text)
    def __str__(self):
        # Devuelve un string representando al objeto
        return str(self.values)
    def __len__(self):
        # Devuelve el tamaño del diccionario
        return len(self.values)
    def __iter(self):
        """
            Devuelve un iterador que devuelve la clave y el valor
            de los elementos.
        """
        return iter(self.values.viewitems())
    def intersection(self, other):
        # Intersecta dos bag-of-words
        intersected_bag = { x: self.values[x] for x in self.values if x in other.values }
        return BagOfWords(values=intersected_bag)
    def union(self, other):
        # Une dos bag-of-words
        unionized_bag = dict(other.values, **self.values)
        return BagOfWords(values=unionized_bag)





