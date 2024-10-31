wenn mode aktiv (grüne LED):
   der Joystick macht Achsen 0 und 1, analog
   der Hat macht JOYHATMOTION events, wo eine der acht Positionen
       auf einem 3x3 Gitter herauskommt, als tuple
wenn mode nicht aktiv
   Hat und Joystick sind vertauscht
   der Hat macht Achsen 0 und 1, nur die Endwerte

Der Schieber (vorne rechts) macht Achse 2 (-> Zoom!)

Tasten vorne außen: 6 und 7
Tasten oben drauf: 3 4 5
                   0 1 2

Taste S: Button 8

(manchmal kommen beim Programmstart schon Tasten-Events, von einer Taste, die vorher mal gedrückt war -> irgendwie wegfiltern, z.B. alles was inner halb 0.1 sek nach STart reinkommt)



Zwei Möglichkeiten für den Joystick:
1) Achsenposition auf Absolutwert mappen
   zwei Winkel in einem bestimmten Bereich
   da muss man irgendwie das Gezappel wegfiltern (z.B. neuen Winkel rausschicken nur wenn Änderung um mindestens 0.02)

   oder höchstens soundsoviele Kamerabefehle pro Sekunde verschicken

2) Achsenposition auf Fahrgeschwindigkeit / Richtung mappen
   hier muss man am Anfang kalibrieren: die Null ablesen, und eine tote Zone darum definieren.

Man könnte das umschaltbar machen. Aber mal mit Nr. 2 anfangen.
   PtzCam.move(x_velocity, y_velocity)
  (Einheit? 1/sec vermutlich, also Wert Zwei wäre: von -1 nach +1 in einer Sekunde -> Ausprobieren)
   erster Versuch: Vollausschlag +1 des Joystick mal zwei -> velocity
   Joystick in toter Zone: PtzCam.stop() aufrufen
   (rate-limiting?? Dazu alle events, aus denen wir Fahrbefehle erzeugen würden, queuen,
   und dann zur "taktzeit" nur den neuesten ausführen.

Schieber (Achse 2): absolute zoom-position von 0 .. 1
   PtzCam.zoom(zoom)


Presets - Anfahren von in der Kamera gespeicherten presets ist hier wohl nicht vorgesehen.

 Also selber speichern: Linke vordere Taste (Feuertaste) halten, dann einen der 6 anderen Buttons drücken und wieder loslassen
zum Abrufen nur einen der 6 buttons drücken.

Presets sofort in separate yaml-Datei rausschreiben
