from browser import Browser
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
    tkinter.mainloop()
