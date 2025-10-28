from browser import Browser
from htmlParser import HTMLParser, print_tree
from url import URL
import tkinter


if __name__ == "__main__":
    import sys
    import os
    working_directory = os.getcwd()
    path_to_html = working_directory + "/example.html"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "file://" + path_to_html

    Browser().load(URL(url))
    #body = URL(url).request()
    #nodes = HTMLParser(body).parse()
    #print_tree(nodes)
    tkinter.mainloop()
