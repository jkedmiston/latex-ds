from latex_reports.latex_obj_base import LatexObjBase

class LatexText(LatexObjBase):
    def __init__(self, text):
        LatexObjBase.__init__(self)
        self.text = text

    def create(self, obj):
        return self.text
