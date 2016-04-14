import json
import sys

sys.path.append('..')
from skytap.Environments import Environments  # noqa
from skytap.Labels import Labels  # noqa

envs = Environments()
labels = Labels()


def test_labels():
    """Peform tests relating to labels."""
    pass
    # #labels.create("BEES!", False)
    # #labels.create("supafly", True)
    #
    # print json.dumps(labels.json())
    #
    # for e in envs:
    #     env_labels = e.labels
    #     #env_labels.add("lolhaha", "barf")
    #     #env_labels = e.labels
    #     for l in env_labels:
    #         print l
    #
    #     break


if __name__ == "__main__":
    test_labels()
