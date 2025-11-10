from constants import HSTEP, VSTEP, WIDTH
from block_layout import BlockLayout

class DocumentLayout:
    def __init__(self, node):
        self.node = node
        self.parent = None
        self.children = []

        self.x = HSTEP
        self.y = VSTEP
        self.width = WIDTH - 2*HSTEP
        self.height = 0

    def layout(self):
        child = BlockLayout(self.node, self, None)
        self.children.append(child)
        child.layout()
        self.height = child.height

    def paint(self):
        return []
        