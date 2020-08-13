import tempfile
import pytest
class Helpers:
    @classmethod
    def fakefig(cls):
        _, g = tempfile.mkstemp()
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1,1)
        ax.scatter([0, 1, 2], [0, 1, 2])
        figname = g + ".png"
        fig.savefig(figname)
        return figname
        
    
@pytest.fixture
def helpers():
    return Helpers

@pytest.fixture
def fakedoc(monkeypatch):
    faketext = "Test1"
    yield faketext
    
