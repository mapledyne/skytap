import json
import sys

sys.path.append('..')
from skytap.Environments import Environments  # noqa
from skytap.Labels import Labels  # noqa

envs = Environments()
labels = Labels()

vms_to_check = 10


def test_vm_labels():
    """Ensure VM has a label object."""
    vm_count = 0
    for e in envs:
        for v in e.vms:
            vm_count += 1
            if vm_count > vms_to_check:
                return
            for l in v.labels:
                assert len(str(l)) > 0, ('Label ' + str(l) + ' from VM '
                                         + v.name + ' has no length.')


def test_lables():
    """Get list of label categories."""
    for l in labels:
        assert len(str(l)) > 0, 'Zero length label (or error) found.'
