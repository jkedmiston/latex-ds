"""
Basic pdf construction example 
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from latex_reports.latex_doc import LatexDoc
basefile = os.path.basename(__file__).replace('.py', '')
fname = "examples/%s.pdf" % basefile
obj = LatexDoc(fname)
fig, ax = plt.subplots(1, 1)
xs = np.linspace(0, 0.1, 100)
ys = xs**3
ax.scatter(xs, ys)
figname = "examples/figures/%s_fig1.png" % basefile
fig.savefig(figname)
obj.add_contents(r"""\section{Section} 
In this section we look at a figure. \\ """)
obj.add_figure(figname, caption="Caption here")
obj.add_clearpage()
d = dict(varname='max(ys)', varvalue=max(ys))

obj.add_contents(r"""\section{Conclusion} Here we have demonstrated \begin{enumerate}
\item{We can plot}
\item{We can pdf}
\item{We can inject numbers like %(varname)s = %(varvalue).2e}
\item{We can insert conclusions back into the top of the document}
\end{enumerate}
""" % d)

obj.insert_contents(r"""\section{Executive Summary} Sometimes its good to put in summary findings back at the top of the page. The max value was %(varvalue).2e \clearpage""" % d, 0)

obj.write()
