import os
import tempfile
from latex_reports.latex_doc import LatexDoc

def test_latex_doc(fakedoc, helpers):
    """assert it can be generated"""
    _, g = tempfile.mkstemp()
    tmp_doc = LatexDoc(g)
    tmp_doc.add_contents(fakedoc)
    tmp_doc.add_figure(helpers.fakefig())
    tmp_doc.write()
    assert os.path.isfile(g + ".pdf")


