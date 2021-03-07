import itertools
import pandas as pd


class LatexSubfigureArray:
    def __init__(self, nrow, ncol, height=2, incgraphics=None, command="[ht]", master_caption=""):

        self.ct = 0
        self.idxs = list(itertools.product(range(nrow), range(ncol)))
        self.data = {}
        self.captions = {}
        self.labels = {}
        self.incgraphics_list = {}
        self.width = round((1./ncol) * 0.98, 2)
        self.ncol = ncol
        self.nrow = nrow
        self.command = command

        self.incgraphics = "height=%scm" % height
        if incgraphics is not None:
            self.incgraphics = incgraphics
        self.master_caption = master_caption
        self.template = r"""\begin{figure}%(command)s
\centering
%(text)s
\caption{%(master_caption)s}
\end{figure}
 """
        pass

    @classmethod
    def init_from_list(cls, ncol, fnames, **kwargs):
        import math
        nrows = math.ceil(len(fnames) / ncol)
        return cls(nrow=nrows, ncol=ncol)

    def count_rows(self):
        nrows = 0
        breaks = []
        last_ct = 0
        for ct in range(0, self.ct, 1):
            if (ct + 1) % self.ncol == 0:
                breaks.append([last_ct, ct + 1])
                nrows += 1
                last_ct = ct + 1
                pass
            pass
        return nrows, breaks

    def create(self, obj):
        nrows, breaks = self.count_rows()
        figtxt = ''
        if nrows > 6:
            iteration_list = list(range(0, len(breaks), 6))
            for j in iteration_list[:-1]:
                first_break = breaks[iteration_list[j]]
                last_break = breaks[iteration_list[j + 1] - 1]
                ctmin = first_break[0]
                ctmax = last_break[-1]
                figtxt += self.template % dict(
                    text=self.get_text(ctmin=ctmin, ctmax=ctmax), command=self.command, master_caption=self.master_caption)
                figtxt += "\clearpage"
                pass
            first_break = breaks[iteration_list[-1]]
            last_break = breaks[-1]
            ctmin = first_break[0]
            ctmax = last_break[-1]
            figtxt += self.template % dict(
                text=self.get_text(ctmin=ctmin, ctmax=ctmax), command=self.command, master_caption=self.master_caption)
            figtxt += r'\clearpage'
            pass

        else:
            figtxt = self.template % dict(
                text=self.get_text(), command=self.command, master_caption=self.master_caption)
        return figtxt

    def add_figure(self, fname, caption="", incgraphics=None, label=None):
        idx = self.idxs[self.ct]
        self.ct += 1
        self.data[idx] = fname
        self.captions[idx] = caption
        if label is None:
            label = "a%(ct)s" % dict(ct=self.ct)
        self.labels[idx] = label
        if incgraphics is None:
            incgraphics = self.incgraphics

        self.incgraphics_list[idx] = incgraphics

    def get_text(self, ctmin=0, ctmax=None):

        text = ""
        if ctmax is None:
            ctmax = self.ct
        lines = []
        last_marker = ctmax - 1
        for ct in range(ctmin, ctmax, 1):
            if (ct + 1) % self.ncol == 0:
                marker = r"\\"
            else:
                marker = r"\hfill"

            fname = self.data[self.idxs[ct]]
            caption = self.captions[self.idxs[ct]]
            label = self.labels[self.idxs[ct]]
            incgraphics = self.incgraphics_list.get(
                self.idxs[ct], self.incgraphics)
            line = r"""\subfloat[%(caption)s]{\label{fig:%(label)s}\includegraphics[%(incgraphics)s]{%(fname)s}}%(marker)s
""" % dict(width=self.width,
                fname=fname,
                label=label,
                incgraphics=incgraphics,
                caption=caption,
                ct=ct,
                marker=marker)
            excess = (ct + 1) % self.ncol
            if marker == r"\\":
                last_marker = ct

            lines.append(line)

        if excess != 0:
            for c, l in enumerate(lines[last_marker:]):
                lines[last_marker + c] = lines[last_marker +
                                               c].replace(r'\hfill', r'\qquad')

            additional = self.ncol - excess
            for j in range(additional):
                line = r"""\raggedright"""
                lines.append(line)
                break
        text = ''.join(lines)
        return text
