from typing import Self
import re


class Node():
    def __init__(self, value):
        self.value = value
        self.left: Self = None
        self.right: Self = None

    def __str__(self):
        if not self.left and not self.right:
            return str(self.value)
        
        left_str = str(self.left) if self.left else ""
        right_str = str(self.right) if self.right else ""
        
        return f"{self.value} ({left_str}, {right_str})"
    
def deserialize_tree(data: str) -> Node:
    if not data:
        return None

    tokens = re.findall(r'-?\d+|[(),]', data)
    
    iterator = iter(tokens)
    
    # Храним текущий токен, на который "смотрит" парсер
    # next(iterator, None) вернет None, когда токены закончатся
    current_token = next(iterator, None)

    def consume():
        """Передвигает указатель на следующий токен"""
        nonlocal current_token
        current_token = next(iterator, None)

    def parse_node():
        # Базовый случай: если токенов нет или мы встретили разделитель
        # Значит, в этой позиции узла не существует (например, "4(,5)" -> левый None)
        if current_token in (None, ',', ')'):
            return None

        # Мы ожидаем, что сейчас current_token - это число
        val = int(current_token)
        node = Node(val)
        consume()  # Мы использовали число, идем дальше

        # Если после числа сразу идет '(', значит у узла есть дети
        if current_token == '(':
            consume()  # Пропускаем открывающую скобку

            # Рекурсивно парсим левое поддерево
            node.left = parse_node()

            # Если видим запятую, значит есть правое поддерево
            if current_token == ',':
                consume()  # Пропускаем запятую
                node.right = parse_node()

            # Обязательно должна быть закрывающая скобка
            if current_token == ')':
                consume()  # Пропускаем закрывающую скобку
        
        return node

    # Запускаем парсинг
    return parse_node()


def find_node(node: Node, value: int) -> bool:
    if node is None:
        return False

    if node.value == value:
        return True
    
    elif value < node.value:
        return find_node(node.left, value)
    else:
        return find_node(node.right, value)

def add_node(tree, value) -> Node:
    if tree is None:
        return Node(value)
    if value == tree.value:
        return tree
    elif value < tree.value:
        tree.left = add_node(tree.left, value)
    else:
        tree.right = add_node(tree.right, value)
    return tree

def del_node(node: Node, value: int) -> Node:
    if node is None:
        return None
    
    if value < node.value:
        node.left = del_node(node.left, value)
    elif value > node.value:
        node.right = del_node(node.right, value)
    else:
        if (node.left is None) and (node.right is None):
            return None
        elif node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        else:
            succesor = node.right
            while succesor.left is not None:
                succesor = succesor.left
            node.value = succesor.value
            node.right = del_node(node.right, succesor.value)
    
    return node

# options = {
#     1: find_node,
#     2: add_node,
#     3: del_node
# }

print("Welcome!\nPlease enter a binary tree: ", end='')
tree = deserialize_tree(input())
while True:
    print("Select one of the options:")
    print("1) Check if the value is in the binary tree")
    print("2) Add an element to the binary tree")
    print("3) Remove an element from the binary tree")
    print("4) Exit")

    choice = int(input())

    if choice == 1:
        value_to_find = int(input("Enter a value to search for: "))
        if find_node(tree, value_to_find):
            print("Value was found in the binary tree!")
        else:
            print("Value was NOT found in the binary tree :(")
    elif choice == 2:
        value_to_add = int(input("Enter a value to add to the tree: "))
        tree = add_node(tree, value_to_add)
        print("Value has been succesfully added to the tree!")
    elif choice == 3:
        value_to_del = int(input("Enter a value to remove from the tree: "))
        tree = del_node(tree, value_to_del)
        print("Value has been removed from the tree (if it was there initially).")
    elif choice == 4:
        print("Exiting the programm...")
        break

    print("-"*40)

print(str(tree))