"""Test Skytap Environments API access."""
import json
import os
import sys

sys.path.append('..')
from skytap.Environments import Environments  # nopep8

environments = Environments()
things_to_check = 25


def test_str_vs_contents():
    """Ensure str() returns the contents."""
    count = 0
    for e in environments:
        if e.id != 7085376:
            continue

        count += 1
        assert str(e.user_data) == str(e.user_data.contents)

        e.user_data.add("rick", "sanchez")
        assert e.user_data.data["rick"] == "sanchez"
        e.user_data.delete("rick")

        e.user_data.add_line("Wubba lubba dub dub!", 0)
        return

        # assert e.user_data.get_line(0) == "Wubba lubba dub dub!"
        #
        # e.user_data.delete_line("Wubba lubba dub dub!")
        # assert e.user_data.get_line(0) != "Wubba lubba dub dub!"

        return

        for v in e.vms:
            if count > things_to_check:
                return
            count += 1
            assert str(v.user_data) == str(v.user_data.contents)
