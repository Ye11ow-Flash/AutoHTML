from __future__ import print_function
from __future__ import absolute_import

import string
import random

TEXT_PLACE_HOLDER = "[]"

class Dom:

    def __init__(self, key, parent_node, content_holder):
        self.key = key
        self.parent = parent_node
        self.children = []
        self.content_holder = content_holder
    
    def random_text(self,length_text=10, space_number=1, with_upper_case=True):
        results = []
        while len(results) < length_text:
            char = random.choice(string.ascii_letters[:26])
            results.append(char)
        if with_upper_case:
            results[0] = results[0].upper()

        current_spaces = []
        while len(current_spaces) < space_number:
            space_pos = random.randint(2, length_text - 3)
            if space_pos in current_spaces:
                break
            results[space_pos] = " "
            if with_upper_case:
                results[space_pos + 1] = results[space_pos - 1].upper()

            current_spaces.append(space_pos)

        return ''.join(results)
    
    def add_child(self, child):
        self.children.append(child)

    def show(self):
        for child in self.children:
            child.show()

    def rendering_function(self, key, value):
        if key.find("btn") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, self.random_text())
        elif key.find("title") != -1:
            value = value.replace(TEXT_PLACE_HOLDER, self.random_text(length_text=5, space_number=0))
        elif key.find("text") != -1:
            value = value.replace(TEXT_PLACE_HOLDER,
                                  self.random_text(length_text=56, space_number=7, with_upper_case=False))
        return value

    def render(self, mapping, rendering_function=None):
        content = ""
        for child in self.children:
            placeholder = child.render(mapping, self.rendering_function)
            if placeholder is None:
                self = None
                return
            else:
                content += placeholder

        value = mapping.get(self.key, None)

        if value is None:
            self = None
            return None

        if rendering_function is not None:
            value = self.rendering_function(self.key, value)

        if len(self.children) != 0:
            value = value.replace(self.content_holder, content)

        return value