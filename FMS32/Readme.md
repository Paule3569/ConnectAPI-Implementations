# FMS32Pro - Connect

Dieses Script wird von User **esche888** aus dem [Feuersoftware Forum](https://feuersoftware.com/forum/) eingesetzt um den Fahrzeugstatus der von FMS32Pro empfangen wird, über die [Connect API](http://dokumentation.feuersoftware.com:8090/pages/viewpage.action?pageId=2490428) zu setzen.

Thread: [Link](https://feuersoftware.com/forum/index.php?thread/2189-wunsch-tetracontrol-schnitstelle-für-fms32-verwenden/)

#Setup

[FMS32Pro](https://www.heirue-soft.de/software/fms32) ist eine Windows Software, daher läuft das Script auch auf einem Windows Rechner.
Dies ist allerdings kein Muss! Das Script kann auch auf jedem anderen Rechner im selben Netz laufen, Dazu muss lediglich IP/Port.

Man installiert [Python](https://www.python.org/downloads/) in einer Version > 3.6. 
Wichtig ist das bei der Installation der Haken bei "Add Python to PATH" gesetzt ist.

Das Script wird an einen beliebeigen Ort gespeichert, z.B. C:\Programme\FMS32status\fms32status.py
Der Token muss in einen File Namens apitoken ohne Endung im selben Verzeichnis platziert werden.

Wir dieses dann z.B. von einem CMD aus gestartet `python  C:\Programme\FMS32status\fms32status.py` läuft das Script soweit.

Da ich keine Ahnung habe wie man unter Windows ein Script als Service einrichtet, warte ich darauf das jemand dafür eine Löung findet. 
Pull-Requests sind herzlich willkommen ;-)
