# BosMon - Connect

Dieses Script wird von User **marcosteeb** aus dem [Feuersoftware Forum](https://feuersoftware.com/forum/) eingesetzt um den Fahrzeugstatus der von BosMon empfangen wird, über die [Connect API](http://dokumentation.feuersoftware.com:8090/pages/viewpage.action?pageId=2490428) zu setzen.

Thread: [Link](https://feuersoftware.com/forum/index.php?thread/2189-wunsch-tetracontrol-schnitstelle-für-fms32-verwenden/)

[BosMon](https://www.bosmon.de/) ist eine Windows Software, weshalb das Python Script auch auf dem Windows Rechner laufen muss.

# Setup

Man installiert [Python](https://www.python.org/downloads/) in einer Version > 3.6. 
Wichtig ist das bei der Installation der Haken bei "Add Python to PATH" gesetzt ist.

Nun die notwendigen Pakete installieren, dazu ein CMD öffnen und folgendes eingeben:
```
pip install requests
```

Das Script wird an einen beliebeigen Ort gespeichert, z.B. C:\Programme\BosMonStatus\bosmonstatus.py
Der Token muss in einen File Namens apitoken ohne Endung im selben Verzeichnis platziert werden.

** Under Construction **
