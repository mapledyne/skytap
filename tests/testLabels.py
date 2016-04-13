import json
import sys

sys.path.append('..')
from skytap.Labels import Labels  # noqa

labels = Labels()


def test_labels():
    """Peform tests relating to labels."""
    sys.exit()

    #labels.create("barf", True)

    for l in labels:
        print l
