# -*- coding: utf-8 -*-
""" Get information about opening changes in this project.

To get all options available for the user, run the script with the shift key pressed. """
__title__ = "Tracking\nOpenings"
__author__ = "BPM"
__highlight__ = "new"

# -------------------------------
# ------------IMPORTS------------
# -------------------------------

from ServerUtils import ServerPermissions  # type: ignore
from pyrevit import forms

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "ui"))
from TrackingOpeningsDialog import TrackingOpeningsDialog  # type: ignore

# -------------------------------
# -------------MAIN--------------
# -------------------------------

uidoc = __revit__.ActiveUIDocument  # type: ignore
doc = uidoc.Document


# --------------------------------
# -------------SCRIPT-------------
# --------------------------------


def run():
    if not doc.IsModelInCloud:
        forms.alert(
            "אפשרות זו זמינה רק עבור פרויקטים בענן",
            title="פרויקט לא בענן",
        )
        return
    server_permissions = ServerPermissions(doc)
    openings_tracking_permission = server_permissions.get_openings_tracking_permission()
    if not openings_tracking_permission:
        forms.alert(
            "אין לפרויקט זה גישה לאפשרות זו",
            title="אין גישה לפרויקט",
        )
        return
    dialog = TrackingOpeningsDialog(uidoc)

    if __shiftclick__:  # type: ignore
        dialog.allow_transactions = True
        dialog.ShowDialog()
    else:
        dialog.Show()


run()
