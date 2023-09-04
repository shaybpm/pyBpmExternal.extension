# -*- coding: utf-8 -*-
""" This script iterates over all the openings (Generic Model from the BPM library) and dose the following:
- Copies the Elevation to a taggable parameter (useful in versions 20+21).
- Copies the Reference Level to a taggable parameter.
- Sets Mark to opening if it is missing.
- Defines whether the opening is located in the floor or not.
- Calculates the projected height of the opening.
- Calculates the absolute height of the opening. """
__title__ = 'Opening\nSetter'
__author__ = 'Ely Komm & Eyal Sinay'

# ------------------------------

import clr
clr.AddReference('RevitAPI')
clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('AdWindows')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System')
clr.AddReferenceByPartialName('System.Windows.Forms')

from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.UI import TaskDialog

max_elements = 5
gdict = globals()
uiapp = __revit__
uidoc = uiapp.ActiveUIDocument
if uidoc:
    doc = uiapp.ActiveUIDocument.Document

def alert(msg):
    TaskDialog.Show('BPM - Opening Update', msg)

from pyrevit import script
# ------------------------------------------------------------
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import OpeningSetter
# ------------------------------------------------------------

def print_results(results):
    output = script.get_output()
    output.print_html('<h1>Opening Setter</h1>')

    is_any_warning = "WARNING" in [result["status"] for result in results]
    if is_any_warning:
        output.print_html('<h2 style="color:red">End with warnings.</h2>')
        for result in results:
            if result["status"] == "WARNING":
                output.insert_divider()
                print(output.linkify(result["opening_id"]))
                for res in result["all_results"]:
                    if res["status"] == "WARNING":
                        output.print_html('<div style="color:red">{}</div>'.format(res["message"]))
    else:
        output.print_html('<h2 style="color:green">End successfully.</h2>')

def print_full_results(results):
    output = script.get_output()
    output.print_html('<h1>Opening Setter</h1>')
    for result in results:
        output.insert_divider()
        print(output.linkify(result["opening_id"]))
        for res in result["all_results"]:
            if res["status"] == "WARNING":
                output.print_html('<div style="color:red">{}</div>'.format(res["message"]))
            else:
                output.print_html('<div style="color:green">{}</div>'.format(res["message"]))

def run():
    all_openings = OpeningSetter.get_all_openings(doc)
    if len(all_openings) == 0:
        alert('No openings found.')
        return
    
    t = Transaction(doc, 'BPM | Opening Update')
    t.Start()
    
    results = []
    for opening in all_openings:
        opening_results = OpeningSetter.execute_all_functions(doc, opening)
        results.append(opening_results)
    
    if __shiftclick__:
        print_full_results(results)
    else:
        print_results(results)

    t.Commit()

run()
