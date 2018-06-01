import  carro
# Node class
class Node:
    # Function to initialise the node object
    def __init__(self, carro):
        self.fabricante = carro.fabricante
        self.modelo = carro.modelo
        self.empresa = carro.empresa
        self.ano = carro.ano
        self.preco = carro.preco
        self.kilometragem = carro.kilometragem
        self.id = carro.id
        self.next = None  # Initialize next as null


# Linked List class contains a Node object
class LinkedList:
    # Function to initialize head
    def __init__(self):
        self.head = None

    # Functio to insert a new node at the beginning
    def push(self, new_data):
        # 1 & 2: Allocate the Node &
        #        Put in the data
        new_node = Node(new_data)

        # 3. Make next of new Node as head
        new_node.next = self.head

        # 4. Move the head to point to new Node
        self.head = new_node

    # This function is defined in Linked List class
    # Appends a new node at the end.  This method is
    # defined inside LinkedList class shown above */
    def append(self, new_data):

        # 1. Create a new node
        # 2. Put in the data
        # 3. Set next as None
        new_node = Node(new_data)

        # 4. If the Linked List is empty, then make the
        #    new node as head
        if self.head is None:
            self.head = new_node
            return

        # 5. Else traverse till the last node
        last = self.head
        while (last.next):
            last = last.next

        # 6. Change the next of last node
        last.next = new_node

    # Utility function to print the linked list
    def printList(self):
        temp = self.head
        while temp != None:
            print(
                "\nLocadora: "+temp.empresa +
                "\nFabricante: "+temp.fabricante +
                "\nModelo:"+temp.modelo +
                "\nAno: "+temp.ano +
                "\nQuilometragem:"+temp.kilometragem +
                "\npreco: "+temp.preco +
                "\nFipe ID: "+str(temp.id)
            )
            temp = temp.next