import tkinter
from constants import HEIGHT, WIDTH, SCROLL_STEP, VSTEP
from block_layout import paint_tree, style
from document_layout import DocumentLayout 
from html_parser import HTMLParser#, print_tree
from css_parser import CSSParser
from element import Element

DEFAULT_STYLE_SHEET = CSSParser(open("./src/browser.css").read()).parse()

class Browser:

    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT,
            bg="white",
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        
    def load(self, url):
        body = url.request()
        self.nodes = HTMLParser(body).parse()

        rules = DEFAULT_STYLE_SHEET.copy()

        links = [node.attributes["href"]
             for node in tree_to_list(self.nodes, [])
             if isinstance(node, Element)
             and node.tag == "link"
             and node.attributes.get("rel") == "stylesheet"
             and "href" in node.attributes]

        for link in links:
          style_url = url.resolve(link)
          try:
              body = style_url.request()
          except:
              continue
          rules.extend(CSSParser(body).parse())

        style(self.nodes, sorted(rules, key=cascade_priority))

        self.document = DocumentLayout(self.nodes)
        self.document.layout()
        #print_tree(self.nodes)

        self.display_list = []
        paint_tree(self.document, self.display_list)
        self.draw()
    
    def draw(self):
        self.canvas.delete("all")
        for cmd in self.display_list:
            if cmd.top > self.scroll + HEIGHT:
                continue
            if cmd.bottom < self.scroll:
                continue
            cmd.execute(self.scroll, self.canvas)

    def scrolldown(self, e):
        max_y = max(self.document.height + 2*VSTEP - HEIGHT, 0)
        self.scroll = min(self.scroll + SCROLL_STEP, max_y)
        self.draw()

def tree_to_list(tree, list):
    list.append(tree)
    for child in tree.children:
        tree_to_list(child, list)
    return list

def cascade_priority(rule):
    selector, body = rule
    return selector.priority