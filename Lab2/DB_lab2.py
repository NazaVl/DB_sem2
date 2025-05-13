def name_to_hash(name: str) -> int:
    name = name.lower()
    hash_value = 0
    name_len = len(name)
    for i, char in enumerate(name):
        if 'a' <= char <= 'z':
            char_index = ord(char) - ord('a') + 10
            power = 2 * (name_len - i)
            hash_value += char_index * (10 ** power)
        else:
            raise ValueError(f"Invalid character in name: {char}")
    hash_str = str(hash_value).ljust(40, '0')
    return int(hash_str)

class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf
        self.parent = None
        self.next_leaf = None

class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusTreeNode(is_leaf=True)
        self.order = order

    def _find_leaf(self, key):
        current = self.root
        while not current.is_leaf:
            i = 0
            while i < len(current.keys) and key >= current.keys[i]:
                i += 1
            current = current.children[i]
        return current

    def insert(self, name, phone):
        key = name_to_hash(name)
        leaf = self._find_leaf(key)
        i = 0
        while i < len(leaf.keys) and (leaf.keys[i][0] < key or (leaf.keys[i][0] == key and leaf.keys[i][1] < name)):
            i += 1
        leaf.keys.insert(i, (key, name, phone))
        if len(leaf.keys) == self.order:
            self._split_node(leaf)

    def _split_node(self, node):
        mid = self.order // 2
        new_node = BPlusTreeNode(is_leaf=node.is_leaf)
        new_node.keys = node.keys[mid:]
        node.keys = node.keys[:mid]

        if node.is_leaf:
            new_node.next_leaf = node.next_leaf
            node.next_leaf = new_node
            new_node.parent = node.parent
            if node.parent is None:
                new_root = BPlusTreeNode()
                new_root.keys = [new_node.keys[0][0]]
                new_root.children = [node, new_node]
                node.parent = new_root
                new_node.parent = new_root
                self.root = new_root
            else:
                self._insert_in_parent(node, new_node.keys[0][0], new_node)
        else:
            split_key = node.keys[mid]
            new_node.keys = node.keys[mid+1:]
            node.keys = node.keys[:mid]
            new_node.children = node.children[mid+1:]
            node.children = node.children[:mid+1]
            for child in new_node.children:
                child.parent = new_node
            self._insert_in_parent(node, split_key, new_node)

    def _insert_in_parent(self, node, key, new_node):
        parent = node.parent
        i = 0
        while i < len(parent.children) and parent.children[i] != node:
            i += 1
        parent.keys.insert(i, key)
        parent.children.insert(i + 1, new_node)
        new_node.parent = parent
        if len(parent.keys) == self.order:
            self._split_node(parent)

    def search(self, name):
        key = name_to_hash(name)
        leaf = self._find_leaf(key)
        for k, n, phone in leaf.keys:
            if k == key and n == name:
                return phone
        return None

    def range_search(self, name, comparison='>'):
        word_len = len(name)
        significance = 10 ** (40 - 2 * word_len)
        results = []
        current = self.root
        while not current.is_leaf:
            current = current.children[0]
        while current:
            for k, n, phone in current.keys:
                if (comparison == '>' and k % significance != 0) or (comparison == '<' and k % (significance * 100) == 0):
                    results.append((n, phone))
            current = current.next_leaf
        return results




    def delete(self, name):
        key = name_to_hash(name)
        leaf = self._find_leaf(key)
        for i, (k, n, phone) in enumerate(leaf.keys):
            if k == key and n == name:
                leaf.keys.pop(i)
                return True
        return False

    def print_tree(self):
        def _print_node(node, level=0):
            indent = "  " * level
            if node.is_leaf:
                print(f"{indent}Leaf: {[f'{n}({k})' for k, n, _ in node.keys]}")
            else:
                print(f"{indent}Internal: {node.keys}")
                for child in node.children:
                    _print_node(child, level + 1)
        _print_node(self.root)



if __name__ == "__main__":
    phone_book = BPlusTree()

    phone_book.insert("Anna", "11111111")
    phone_book.insert("Bohdan", "22222222")
    phone_book.insert("Clara", "33333333")
    phone_book.insert("Danylo", "44444444")
    phone_book.insert("Eugene", "55555555")
    phone_book.insert("Fedor", "66666666")
    phone_book.insert("Greg", "77777777")
    phone_book.insert("Kit", "88888888")
    
    print(phone_book.search("Eugene"))

    

    for name, phone in phone_book.range_search("Fedor"):
        print(f"{name}: {phone}")
    print("------")

    for name, phone in phone_book.range_search("Anna", "<"):
        print(f"{name}: {phone}")
    phone_book.print_tree()
    phone_book.delete("Fedor")
    print(phone_book.search("Fedor"))