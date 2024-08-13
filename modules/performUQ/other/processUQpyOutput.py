from pathlib import Path  # noqa: CPY001, D100, INP001

import numpy as np


def output_function(index):  # noqa: ARG001, D103
    filePath = Path('./results.out').resolve()  # noqa: N806
    return np.atleast_2d(np.genfromtxt(filePath))
