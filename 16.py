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


def iter_preorder(node: Node) -> None:
    stack = []
    stack.append(node)

    while len(stack) != 0:
        current_node = stack.pop()

        if current_node:
            print(current_node.value, end=" ")
            stack.append(current_node.right)
            stack.append(current_node.left)

test_input = '8 (3 (1, 6 (4,7)), 10 (, 14(13,)))'
tree = deserialize_tree(test_input)

# Результат: 8 3 1 6 4 7 10 14 13 
print("Итеративный прямой обход:")
iter_preorder(tree)
            