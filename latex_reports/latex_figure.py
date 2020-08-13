from latex_reports.latex_obj_base import LatexObjBase
from latex_reports.latex_utilities import make_latex_safe

class LatexFigure(LatexObjBase):
    def __init__(self, fname, width=1, caption=None, label=None):
        LatexObjBase.__init__(self)
        self.fname = fname
        self.width = 1
        self.caption = caption
        self.label = label

    def create(self, obj):
        obj.fig_count += 1
        if self.label is None:
            label = "ct_%d" % obj.fig_count
        else:
            label = self.label
        if self.caption is None:
            caption = ""
        else:
            caption = self.caption

        return r"""
\begin{figure}
\centering
\includegraphics[width=%(width)s\textwidth]{%(fname)s}
\caption{%(caption)s}
\label{fig:%(label)s}
\end{figure}""" % dict(fname=self.fname, width=self.width, caption=make_latex_safe(caption), label=label)
