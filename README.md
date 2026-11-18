# Feelings Group interview session

Three FreeCAD mounting concepts for the display, paw-shaped monitor and triangular camera. Start with the display assembly to see the 300 mm support height. All lengths are in millimetres.

| Design | Native assembly | Exchange file | Design intent |
|---|---|---|---|
| Elevated display stand | [FreeCAD](task1/DisplayStand.FCStd) | [STEP](task1/DisplayStand.step) | Anchored foot, square mast and lift-out saddle |
| Tabletop paw dock | [FreeCAD](task1/PawDock.FCStd) | [STEP](task1/PawDock.step) | Open-front pocket with underside cable access |
| Camera pan stand | [FreeCAD](task1/CameraPanStand.FCStd) | [STEP](task1/CameraPanStand.step) | Strap-retained V-seat, vertical pivot and servo pushrod |

## Submission status

These assemblies address the external mounting work discussed in the lab. The written brief also describes an internal PCB enclosure, battery drawer and sections through the USB port and switch. Those items remain outside this submission. The PCB reference model was unavailable during this work.

The modeled solids passed validity and pairwise overlap checks in the saved position. Physical fit, anchoring loads, retention under motion and powered pan travel still need testing. No physical measurements were supplied for the three housings.

## Review notes

- [Dimension log and assumptions](notes/assumptions.md)
- [Clearance table](task1/clearances.md)
- [Assembly and hardware notes](notes/assembly.txt)
- [Geometry source with nominal dimensions](notes/geometry-source.py)
- [Design reflection](reflection.md)
- [AI assistance record](AI_links.md)
