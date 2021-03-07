import itertools


class LatexSubfigureArray:
    def __init__(self, nrow, ncol, height=2, incgraphics=None, command="[ht]", master_caption=""):

        self.ct = 0
        self.idxs = list(itertools.product(range(nrow), range(ncol)))
        self.data = {}
        self.captions = {}
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
        import pandas as pd
        nrows = 0
        breaks = []
        last_ct = 0
        for ct in range(0, self.ct, 1):
            if (ct + 1) % self.ncol == 0:
                # will loop from last_ct: ct + 1
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

    def add_figure(self, fname, caption=" hi ", incgraphics=None):
        idx = self.idxs[self.ct]
        self.ct += 1
        self.data[idx] = fname
        self.captions[idx] = caption
        if incgraphics is None:
            incgraphics = self.incgraphics

        self.incgraphics_list[idx] = incgraphics

    def get_text(self, ctmin=0, ctmax=None):

        text = ""
        if ctmax is None:
            ctmax = self.ct
        lines = []
        last_marker = ctmax - 1
        #excess = 0
        for ct in range(ctmin, ctmax, 1):
            if (ct + 1) % self.ncol == 0:
                marker = r"\\"
            else:
                marker = r"\hfill"

            fname = self.data[self.idxs[ct]]
            caption = self.captions[self.idxs[ct]]
            incgraphics = self.incgraphics_list.get(
                self.idxs[ct], self.incgraphics)
            # width = %(width)s\textwidth,
            line = r"""\subfloat[%(caption)s]{\label{sfig:a%(ct)d}\includegraphics[%(incgraphics)s]{%(fname)s}}%(marker)s
""" % dict(width=self.width,
                fname=fname,
                incgraphics=incgraphics,
                caption=caption,
                ct=ct,
                marker=marker)
            excess = (ct + 1) % self.ncol
            #text += line
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
                #text += line
                break
        text = ''.join(lines)
        return text


class LatexSubfigureArrayGrid(LatexSubfigureArray):
    def __init__(self, nrow, ncol, original_fname, usable_paper_width=None):
        LatexSubfigureArray.__init__(self, nrow, ncol)
        self.aspect_ratio = {}
        self.ncol = ncol
        self.nrow = nrow
        self.width_px = {}
        self.height_px = {}
        self.original_fname = original_fname
        arr = cv2.imread(original_fname)
        self.npix_width_total = arr.shape[1]
        if usable_paper_width is None:
            self.usable_paper_width = 12
        else:
            self.usable_paper_width = usable_paper_width

    @classmethod
    def init_from_list(cls, ncol, fnames, **kwargs):
        master_fname = kwargs["master_fname"]
        import math
        nrows = math.ceil(len(fnames) / ncol)
        return cls(nrow=nrows,
                   ncol=ncol,
                   original_fname=master_fname)

    @classmethod
    def init_from_master(cls, ncol, fname, chunksize):
        fnames, gridmap = split_image(fname, chunksize=chunksize)
        out = cls.init_from_list(ncol=ncol,
                                 fnames=fnames,
                                 master_fname=fname,
                                 usable_paper_width=17)
        for kk, f in enumerate(fnames):
            out.add_figure(f)

        return out

    def add_figure(self, fname, caption=" hi "):
        idx = self.idxs[self.ct]
        self.ct += 1
        self.data[idx] = fname
        self.captions[idx] = caption

        arr = cv2.imread(fname)
        nrow = arr.shape[0]
        ncol = arr.shape[1]
        aspect_ratio = float(ncol) / nrow

        self.aspect_ratio[idx] = aspect_ratio
        self.width_px[idx] = ncol
        self.height_px[idx] = nrow

    def get_text(self):
        text = ""
        for ct in range(self.ct):
            if (ct + 1) % self.ncol == 0:
                marker = r"\\"
            else:
                marker = r"\hfill"

            fname = self.data[self.idxs[ct]]
            caption = self.captions[self.idxs[ct]]
            wpx = self.width_px[self.idxs[ct]]
            hpx = self.height_px[self.idxs[ct]]
            ncol = self.ncol
            cm_per_pixel = self.usable_paper_width/self.npix_width_total
            width_cm_local = wpx * cm_per_pixel
            height_cm_local = hpx * cm_per_pixel
            line = r"""\subfloat[%(caption)s]{\label{sfig:a%(ct)d}\includegraphics[width=%(width)scm,height=%(height)scm]{%(fname)s}}%(marker)s
""" % dict(
                width=width_cm_local,
                height=height_cm_local,
                fname=fname,
                caption=caption,
                ct=ct,
                marker=marker)

            text += line
        return text
