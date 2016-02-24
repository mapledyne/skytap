"""Test Skytap Environments API access."""
import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.Environments import Environments  # nopep8


class TestNotes(unittest.TestCase):

    """Unittest class to test notes."""

    def setUp(self):
        """Build the environment set we want to test with.

        This can generate a lot of API calls, so in the typical case, it's
        better not to "check all". Set notes_to_check to the limit to count.
        """
        self.environments = Environments()
        self.notes_to_check = 25

    def test_basic_userdata(self):
        """Run some simple checks of UserData."""
        note_count = 0
        for e in self.environments:
            note_count += 1
            for n in e.notes:
                if note_count > self.notes_to_check:
                    return
                note_count += 1
                self.check_note(n)
            for v in e.vms:
                note_count += 1
                for n in v.notes:
                    if note_count > self.notes_to_check:
                        return
                    note_count += 1
                    self.check_note(n)

    def check_note(self, note):
        """Test one note."""
        self.assertTrue(note.id > 0, 'No note ID found.')
        self.assertTrue(len(note.text) > 0, "Note [" + str(note.id) +
                        "] empty.")
        self.assertTrue(note.text == str(note), "Note [" + str(note.id) +
                        "] mismatching.")
        self.assertTrue(note.created_at <= note.updated_at,
                        "Note [" + str(note.id) +
                        "] updated before it was created.")
