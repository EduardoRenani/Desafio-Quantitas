class HashMap:     #hashmap de registro multiplo. Se a chave bruta (pré hashe) já consta na hash, ela armazena numa lista encadeada de valores)
    def __init__(self): #nota: a hash é um vetor com expansao em lista para tratar colisoes. A já existencia de registro com a mesma chave bruta não é colisao, é dupla entrada. Em determinados casos,
        self.store = [None for _ in range(16)] #todos os valores serão de interesse e por isso não se pode sobrescrever valores de entrada com mesma chave bruta (chave pré hash)
        self.size = 0

    def get(self, key):
        key_hash = self._hash(key)
        index = self._position(key_hash)
        if not self.store[index]:
            return None
        else:
            list_at_index = self.store[index]
            for i in list_at_index:
                if i.key == key:
                    return i.value
            return None

    def getObj(self, key):
        key_hash = self._hash(key)
        index = self._position(key_hash)
        if not self.store[index]:
            return None
        else:
            list_at_index = self.store[index]
            for i in list_at_index:
                if i.key == key:
                    return i
            return None

    def put(self, key, value):
        p = Node(key, value)
        key_hash = self._hash(key)
        index = self._position(key_hash)
        if not self.store[index]:
            self.store[index] = [p]
            self.size += 1
        else:
            list_at_index = self.store[index]
            if p not in list_at_index:
                list_at_index.append(p)
                self.size += 1
            else:
                for i in list_at_index:
                    if i == p:
                        i.listValues.append(value)
                        break

    def __len__(self):
        return self.size

    def _hash(self, key):
        if isinstance(key, int):
            return key
        result = 5381
        for char in key:
            result = 33 * result + ord(char)
        return result

    def _position(self, key_hash):
        return key_hash % 15


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.listValues = []
        self.listValues.append(value)

    def __eq__(self, other):
        return self.key == other.key

    def print(self):
        print("key: " +self.key)
        for i in range(1, len(self.listValues), 1):
            print(" Values: " +self.listValues[i])