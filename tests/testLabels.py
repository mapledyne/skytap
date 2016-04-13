import json
import sys

sys.path.append('..')
from skytap.Labels import Labels  # noqa

labels = Labels()


def test_labels():
    """Peform tests relating to labels."""

    labels.create("barf", True)

    for l in labels:
        print l


if __name__ == "__main__":
    test_labels()
