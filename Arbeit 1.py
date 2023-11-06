import matplotlib.pyplot as plt
import numpy as np

# Definition einer Klasse Parallelepiped zur Darstellung eines Quaders
class Parallelepiped:
    def __init__(self, origin, v1, v2, v3):
        # Alle Koordinaten des Ursprungs und der Vektoren müssen im ersten Oktanten liegen.
        # Das bedeutet, dass sie grösser oder gleich Null sein müssen.
        if not all(coord >= 0 for coord in origin) or not all(coord >= 0 for coord in v1) or not all(coord >= 0 for coord in v2) or not all(coord >= 0 for coord in v3):
            raise ValueError("Alle Punkte müssen im ersten Oktanten mit positiven Koordinaten liegen.")
        
        # Initialisierung der Eigenschaften des Quaders
        self.origin = origin  # Ursprungspunkt des Quaders
        # Berechnung der Eckpunkte des Quaders durch Addition der Vektoren zu dem Ursprung
        self.v1 = (origin[0] + v1[0], origin[1] + v1[1], origin[2] + v1[2])
        self.v2 = (origin[0] + v2[0], origin[1] + v2[1], origin[2] + v2[2])
        self.v3 = (origin[0] + v3[0], origin[1] + v3[1], origin[2] + v3[2])
        # Berechnung aller Eckpunkte des Quaders
        self.vertices = self._compute_vertices()
    
    def _compute_vertices(self):
        # Die Methode berechnet alle Eckpunkte des Quaders, basierend auf den gegebenen drei Vektoren.
        o = self.origin
        p1 = self.v1
        p2 = self.v2
        p3 = self.v3
        # Berechnung der übrigen Punkte des Quaders durch Addition und Subtraktion der Vektoren
        p4 = (p1[0] + p2[0] - o[0], p1[1] + p2[1] - o[1], p1[2] + p2[2] - o[2])
        p5 = self.v3
        p6 = (p5[0] + p1[0] - o[0], p5[1] + p1[1] - o[1], p5[2] + p1[2] - o[2])
        p7 = (p5[0] + p2[0] - o[0], p5[1] + p2[1] - o[1], p5[2] + p2[2] - o[2])
        p8 = (p3[0] + p4[0] - o[0], p3[1] + p4[1] - o[1], p3[2] + p4[2] - o[2])

        # Rückgabe einer Liste von Flächen, wobei jede Fläche als Liste von vier Eckpunkten dargestellt wird
        return [
            [o, p1, p4, p2], # Untere Fläche
            [o, p1, p6, p5], # Vordere Fläche
            [o, p2, p7, p5], # Linke Fläche
            [p8, p6, p1, p4], # Hintere Fläche
            [p8, p6, p5, p7], # Obere Fläche
            [p8, p4, p2, p7]  # Rechte Fläche
        ]

# Funktion zur Projektion des Quaders auf die xy-Ebene aus der Sicht einer Kamera
def project_to_xy(parallelepiped, camera):
    # Die Kamera muss ebenfalls im ersten Oktanten liegen.
    if not all(coord > 0 for coord in camera):
        raise ValueError("Das Projektionszentrum muss im ersten Oktanten liegen.")

    # Überprüfung, ob der Quader vollständig zwischen Kamera und xy-Ebene liegt.
    for face in parallelepiped.vertices:
        for vertex in face:
            # Überprüfung, ob ein Punkt des Quaders hinter der Kamera liegt.
            if any(c >= cc for c, cc in zip(vertex, camera)):
                raise ValueError("Das Parallelepiped muss vollständig zwischen der Kamera und der Ebene z=0 liegen.")

    # Berechnung der Projektion der Eckpunkte des Quaders auf die xy-Ebene
    projected_vertices = []
    for face in parallelepiped.vertices:
        projected_face = []
        for vertex in face:
            # Perspektivische Projektion der Punkte auf die xy-Ebene
            projected_x = camera[2] * (vertex[0] - camera[0]) / (vertex[2] - camera[2]) + camera[0]
            projected_y = camera[2] * (vertex[1] - camera[1]) / (vertex[2] - camera[2]) + camera[1]
            projected_face.append((projected_x, projected_y))
        projected_vertices.append(projected_face)

    return projected_vertices

# Funktion zum Plotten der projizierten Eckpunkte
def plot_projection(projected_vertices):
    fig, ax = plt.subplots()
    # Zeichnen jeder Fläche des projizierten Quaders
    for face in projected_vertices:
        xs, ys = zip(*face)  # Extraktion der x und y Koordinaten in separate Listen
        xs += (face[0][0],)  # Hinzufügen des ersten Punktes am Ende, um die Fläche zu schliessen
        ys += (face[0][1],)
        ax.plot(xs, ys, "o-")  # Zeichnen der Punkte und Verbinden mit Linien

    # Einstellungen für das Diagramm
    plt.grid(True)          # Aktivierung des Gitters im Diagramm
    plt.xlabel('x')         # Beschriftung der x-Achse
    plt.ylabel('y')         # Beschriftung der y-Achse
    plt.show()              # Anzeigen des Diagramms

# Erstellen einer Instanz des Parallelepiped mit Ursprung und drei Richtungsvektoren
parallelepiped = Parallelepiped((1, 1, 1), (2, 0, 0), (0, 2, 0), (0, 0, 2))

# Definition zweier verschiedener Positionen für die Kamera
camera1 = (6, 6, 6)
camera2 = (8, 8, 5)

# Projektion des Quaders von beiden Kamerapositionen aus und deren Plots
projected_vertices1 = project_to_xy(parallelepiped, camera1)
projected_vertices2 = project_to_xy(parallelepiped, camera2)

# Ausgabe der Projektionen und deren Visual
print("Projektion mit Kameraposition", camera1)
plot_projection(projected_vertices1)

print("Projektion mit Kameraposition", camera2)
plot_projection(projected_vertices2)