# remote_pc_monitor
allows to monitor the activity on a pc. For instance my sons gaming pc, to visualize the amount of gaming he does. 
further to show the usage of all our pcs and raspis on one glance.

# auto start
Um das Python-Skript automatisch beim Start eines Windows-PCs auszuführen, können Sie es zu den Autostart-Programmen hinzufügen. Hier sind die Schritte, die Sie befolgen können:

Methode 1: Verknüpfung im Autostart-Ordner
Erstellen einer Batch-Datei:

Erstellen Sie eine neue Textdatei und benennen Sie sie z.B. start_script.bat.
Fügen Sie den folgenden Inhalt hinzu, um das Python-Skript auszuführen:
```
  @echo off
  python "C:\Pfad\zu\Ihrem\skript.py"
```

Speichern Sie die Datei.
Hinzufügen zum Autostart-Ordner:

Drücken Sie Win + R, um den Ausführen-Dialog zu öffnen.
Geben Sie shell:startup ein und drücken Sie Enter. Dies öffnet den Autostart-Ordner.
Verschieben oder kopieren Sie die erstellte start_script.bat-Datei in diesen Ordner.
Methode 2: Aufgabenplanung (Task Scheduler)
Task Scheduler öffnen:

Drücken Sie Win + S und suchen Sie nach "Aufgabenplanung" oder "Task Scheduler".
Öffnen Sie die Aufgabenplanung.
Neue Aufgabe erstellen:

Klicken Sie auf "Aufgabe erstellen" in der rechten Spalte.
Geben Sie der Aufgabe einen Namen, z.B. "Start Python Script".
Trigger hinzufügen:

Wechseln Sie zum Reiter "Trigger" und klicken Sie auf "Neu".
Wählen Sie "Beim Start" aus der Dropdown-Liste unter "Aufgabe starten".
Klicken Sie auf "OK".
Aktionen hinzufügen:

Wechseln Sie zum Reiter "Aktionen" und klicken Sie auf "Neu".
Wählen Sie "Programm starten" aus der Dropdown-Liste.
Geben Sie den Pfad zur python.exe ein (z.B. C:\Pfad\zu\python.exe).
Geben Sie den Pfad zu Ihrem Skript in das Feld "Argumente hinzufügen (optional)" ein:
"C:\Pfad\zu\Ihrem\skript.py"

Klicken Sie auf "OK".
Einstellungen überprüfen:

Wechseln Sie zum Reiter "Einstellungen" und stellen Sie sicher, dass "Aufgabe so schnell wie möglich nach einem verpassten Start ausführen" und "Wiederholen Sie den Vorgang alle" deaktiviert sind, es sei denn, Sie haben besondere Anforderungen.
Klicken Sie auf "OK", um die Aufgabe zu erstellen.
# skript verstecken
Schritt 1: Erstellen der Batch-Datei
Erstellen Sie eine Batch-Datei start_script.bat mit folgendem Inhalt:

```
@echo off
python "C:\Pfad\zu\Ihrem\skript.py"
```

Schritt 2: Erstellen des VBS-Skripts
Erstellen Sie eine neue Datei start_script.vbs mit folgendem Inhalt:
```
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "C:\Pfad\zu\start_script.bat" & chr(34), 0
Set WshShell = Nothing
```
Das , 0 am Ende der WshShell.Run-Zeile sorgt dafür, dass die Batch-Datei unsichtbar im Hintergrund ausgeführt wird.

Schritt 3: Hinzufügen zum Autostart-Ordner
Öffnen des Autostart-Ordners:

Drücken Sie Win + R, um den Ausführen-Dialog zu öffnen.
Geben Sie shell:startup ein und drücken Sie Enter. Dies öffnet den Autostart-Ordner.
VBS-Skript hinzufügen:

Verschieben oder kopieren Sie die start_script.vbs-Datei in den Autostart-Ordner.
Alternative Methode: Task Scheduler
Falls Sie den Task Scheduler verwenden möchten, um das Skript im Hintergrund auszuführen, können Sie direkt eine Aufgabe erstellen, die die Python-Interpreter.exe im Hintergrund ausführt.

Hier sind die Schritte:

Task Scheduler öffnen:

Drücken Sie Win + S und suchen Sie nach "Aufgabenplanung" oder "Task Scheduler".
Öffnen Sie die Aufgabenplanung.
Neue Aufgabe erstellen:

Klicken Sie auf "Aufgabe erstellen" in der rechten Spalte.
Geben Sie der Aufgabe einen Namen, z.B. "Start Python Script".
Trigger hinzufügen:

Wechseln Sie zum Reiter "Trigger" und klicken Sie auf "Neu".
Wählen Sie "Beim Start" aus der Dropdown-Liste unter "Aufgabe starten".
Klicken Sie auf "OK".
Aktionen hinzufügen:

Wechseln Sie zum Reiter "Aktionen" und klicken Sie auf "Neu".
Wählen Sie "Programm starten" aus der Dropdown-Liste.
Geben Sie den Pfad zur pythonw.exe ein (z.B. C:\Pfad\zu\pythonw.exe). pythonw.exe ist die Version des Python-Interpreters, die keine Konsole öffnet.
Geben Sie den Pfad zu Ihrem Skript in das Feld "Argumente hinzufügen (optional)" ein:
"C:\Pfad\zu\Ihrem\skript.py"

Klicken Sie auf "OK".
Einstellungen überprüfen:

Wechseln Sie zum Reiter "Einstellungen" und stellen Sie sicher, dass "Aufgabe so schnell wie möglich nach einem verpassten Start ausführen" und "Wiederholen Sie den Vorgang alle" deaktiviert sind, es sei denn, Sie haben besondere Anforderungen.
Klicken Sie auf "OK", um die Aufgabe zu erstellen.
Überprüfung
