import os
from latex_reports.latex_text import LatexText
from latex_reports.latex_figure import LatexFigure


class LatexDoc:
    doc = r"""
\documentclass[12pt]{article}
%(preamble)s
%(variables)s
\begin{document}
%(contents)s
\end{document}
    """

    def __init__(self, fname, preamble=None):
        self.preamble = []
        self.contents = []
        self.variables = []

        fname = self.clean_fname(fname)
        self.fname = fname
        self.fig_count = 0

        self.preamble = r"""
        \usepackage{graphicx}
        \usepackage{booktabs}
        \usepackage{fullpage}
        \usepackage{hyperref}
        \usepackage[T1]{fontenc}
        \usepackage{subfig}"""
        if preamble is not None and isinstance(preamble, str):
            self.preamble = preamble
        pass

    def clean_fname(self, fname):
        if fname[-4:] == ".tex":
            fname = fname[:-4]
        if fname[-4:] == ".pdf":
            fname = fname[:-4]
        return fname

    def pdfname(self):
        return self.fname + ".pdf"

    def add_figure(self, figname, caption=None, label=None, width=1):
        self.add_contents(LatexFigure(
            figname, caption=caption, label=label, width=width))

    def add_preamble(self, txt):
        self.preamble.append(txt)

    def add_clearpage(self):
        self.add_contents(r"\clearpage")

    def insert_contents(self, txt, pos):
        if isinstance(txt, str):
            self.insert_contents(LatexText(txt), pos)
            return

        self.contents.insert(pos, txt)

    def add_contents(self, txt):
        if isinstance(txt, str):
            self.add_contents(LatexText(txt))
            return

        self.contents.append(txt)

    def add_variables(self, txt):
        self.variables.append(txt)

    def write(self):
        contents = ""
        for c in self.contents:
            contents += c.create(self) + "\n"
        contents = contents[:-1]
        doc = self.doc % dict(preamble=self.preamble,
                              contents=contents,
                              variables='\n'.join(self.variables))
        f = open(self.fname + ".tex", "w")
        f.write(doc)
        f.close()
        print(f.name)
        dirname = os.path.dirname(self.fname)
        if dirname == '':
            dirname = '.'

        info = dict(d=dirname,
                    t=self.fname + '.tex')
        for j in range(2):
            out = os.system("pdflatex -output-directory %(d)s %(t)s" % info)
            if out == 0:
                continue
        if out == 0:
            return self.fname + '.pdf'
