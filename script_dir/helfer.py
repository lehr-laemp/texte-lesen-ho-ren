"""
helfer.py
    alle nötigen Funktionen
"""
# -----------------------------------------------------------------------------
# import
import tomlkit
import guizero as gz
from openai import OpenAI
import edge_tts

import os
import re
from random import choice


# -----------------------------------------------------------------------------
APP = gz.App(title='Training Verstehen', width=230, height= 270)
WORKING_DIR = os.getcwd()
# Welches Modell? https://openai.com/api/pricing/ 
OPENAI_MODELL = 'gpt-4o-mini'


KI_SYSTEM_PROMPT = """
Du bist eine Lehrerin, die für 10-jährige bis 12-jährige Schüler schreibt.
Du schreibst in einfacher, gut verständlicher Sprache mit wenigen Fachwörtern.
Wenn doch Fachwörter vorkommen, dann erklärst du sie.
Du verwendest die deutsch-schweizer Rechtschreibung mit ss statt ß.

Denke über die Aufgabe nach, bevor du eine Antwort gibst. 
Notiere deine Gedanken vor der jeweiligen Antwort.
"""

KI_USER_PROMPT = """
Bitte schreibe zu folgenden Text 12 Fragen.
Sie sollen zum genauen Lesen und Nachdenken anregen.

Bitte gib die Fragen als python-Liste zurück und nummeriere sie.
Zum Beispiel so: ["1. Wer ist Ute?", "2. Wo arbeitet Ute am Morgen?"]

Und dann noch als python-Liste mit den Frage-Antwort-Paaren.
Zum Beispiel so: ["1. Wer ist Ute? Ute ist ein Bauern-Mädchen im Mittelalter.", "2. Wo arbeitet Ute am Morgen? Sie arbeitet 
im Garten."]

Das ist der Text: 

"""


# -----------------------------------------------------------------------------
def erstelle_leere_text_datei() -> str:
    """
    Erstellt eine leere Text-Datei im toml-Format.
        Speichert sie im Script-Ordner als vorlage.toml.
    :return: Pfad zur Datei
    """

    print('\t\t erstelle_leere_text_datei')

    toml_doc = tomlkit.document()
    toml_doc.add(tomlkit.comment('##########################################'))

    toml_doc.add(tomlkit.nl())
    toml_doc.add(tomlkit.comment('Titel des Textes'))
    toml_doc.add('titel', '')

    toml_doc.add(tomlkit.nl())
    toml_doc.add(tomlkit.comment('Quelle des Textes'))
    toml_doc.add('quelle', '')

    toml_doc.add(tomlkit.nl())
    toml_doc.add(tomlkit.comment('eventuell Adresse zu einem Bild'))
    toml_doc.add('bild', '')

    toml_doc.add(tomlkit.nl())
    toml_doc.add(tomlkit.comment('Hier kommt der Text'))
    toml_doc['text'] = tomlkit.string(raw='xxx', multiline=True)

    toml_doc.add(tomlkit.nl())
    toml_doc.add(tomlkit.comment('Fragen zum Text (von KI erzeugt)'))
    toml_doc['fragen'] = tomlkit.string(raw='xxx', multiline=True)

    toml_doc.add(tomlkit.nl())
    toml_doc.add(tomlkit.comment('Antworten zu den Fragen'))
    toml_doc['antworten'] = tomlkit.string(raw='xxx', multiline=True)
    
    toml_doc.add(tomlkit.nl())
    toml_doc.add(tomlkit.comment('Rückmeldung der KI'))
    toml_doc['ki_antwort'] = tomlkit.string(raw='xxx', multiline=True)    

    # Ausgeben der TOML-Daten
    toml_string = tomlkit.dumps(toml_doc)

    # toml-Datei speichern
    datei_name_pfad = os.path.join(WORKING_DIR, 'texte', 'vorlage.toml')
    with open(datei_name_pfad, 'w') as f:
        f.write(toml_string)

    return datei_name_pfad


# -----------------------------------------------------------------------------
def hole_fragen_von_openai(text: str) -> bool:
    """
    Übergibt den Text an Openai mit dem Auftrag,
        12 Fragen und 12 Fragen-Antworten zurückzugeben.
    :param text: Text, zu dem Fragen gesucht werden sollen.
    :return: Text mit den 12 Fragen und 12 Fragen-Antworten
    """

    print('\t\t hole_fragen_von_openai')

    # Openai initialisieren
    api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key, )

    completion = client.chat.completions.create(
        model=OPENAI_MODELL,
        messages=[
            {'role': 'system', 'content': KI_SYSTEM_PROMPT},
            {'role': 'user', 'content': KI_USER_PROMPT + text}
        ]
    )

    return completion.choices[0].message.content


# -----------------------------------------------------------------------------
def klicke_button_fragen_suchen() ->bool:
    """
    Startet alle Prozesse, wenn der Button "Fragen suchen" geklickt wird
    :return: True, wenn alles OK
    """

    print('\t klicke_button_fragen_suchen')

    # Datei wählen
    pfad_zu_textdatei = waehle_text_datei()
    # OK print(pfad_zu_textdatei)

    # Lesen die Text-Datei
    with open(pfad_zu_textdatei, 'r') as datei:
        toml_content = datei.read()

    # Parsen des TOML-Inhalts
    toml_doc = tomlkit.parse(toml_content)
    text_roh = toml_doc['text']

    # Zeigt ein Fenster mit einem Hinweis
    warte_fenster = gz.Window(master=APP,
                              title='Die KI sucht Fragen: Das dauert einen Moment.',
                              width=500, height=20)

    # Macht eine Anfrage an Openai
    ki_antwort = hole_fragen_von_openai(text=text_roh)
    toml_doc['ki_antwort'] = tomlkit.string(ki_antwort, multiline=True)
    # OK print(toml_doc['ki_antwort'])
    
    # toml-Daten dumpen ...
    toml_content = tomlkit.dumps(toml_doc)
    # OK print(toml_string)

    # und speichern
    with open(pfad_zu_textdatei, 'w') as datei:
        datei.write(toml_content)

    warte_fenster.destroy()    
    
    return True


# -----------------------------------------------------------------------------
def klicke_button_text_bearbeiten() -> bool:
    """
    Startet alle Prozesse, wenn der Button "Text bearbeiten" geklickt wird
    :return: True, wenn alles OK
    """

    print('\t klicke_button_text_bearbeiten')

    # Datei wählen
    pfad_zu_textdatei = waehle_text_datei()
    # OK print(pfad_zu_textdatei)

    # Fenster zum Bearbeiten öffnen
    zeige_fenster_fuer_texte(titel='Text bearbeiten',
                             pfad_zur_toml_datei=pfad_zu_textdatei)

    return True


# -----------------------------------------------------------------------------
def klicke_button_text_erstellen() -> bool:
    """
    Startet alle Prozesse, wenn der Button "Text erstellen" geklickt wird
    :return: True, wenn alles OK
    """

    print('\t klicke_button_text_erstellen')

    # leere Text-Datei (im toml-Format) erstellen
    pfad_zur_neuen_datei = erstelle_leere_text_datei()

    # leere Text-Datei zum Bearbeiten öffnen
    zeige_fenster_fuer_texte(titel='Neuer Text erstellen',
                             pfad_zur_toml_datei=pfad_zur_neuen_datei)

    return True


# -----------------------------------------------------------------------------
def klicke_button_text_zu_audio() -> bool:
    """
    Wandelt den Text in eine Audio-Datei um.
    :return: True, wenn alles OK.
    """

    print('\t klicke_button_text_zu_audio')

    # Datei wählen
    pfad_zu_textdatei = waehle_text_datei()

    # Lesen die Text-Datei
    with open(pfad_zu_textdatei, 'r') as datei:
        toml_content = datei.read()

    # Parsen des TOML-Inhalts
    toml_doc = tomlkit.parse(toml_content)
    text_roh = toml_doc['text']    

    # Zeigt ein Fenster mit einem Hinweis
    warte_fenster = gz.Window(master=APP,
                              title='Der Text wird in eine Audio-Datei umgewandelt: Das dauert einen Moment.',
                              width=550, height=20)

    # edge-tts einrichten
    
    # Stimme zufällig auswählen
    stimmen_zur_auswahl = ['de-DE-SeraphinaMultilingualNeural', 'de-DE-FlorianMultilingualNeural']
    stimme = choice(stimmen_zur_auswahl)

    # Name der toml-Datei bestimmen, ohne Endung
    datei_name = os.path.basename(pfad_zu_textdatei)[:-5]
    # OK print(datei_name)

    # Pfad der Audio-Datei
    pfad_zu_audiodatei = os.path.join(WORKING_DIR, 'audio', datei_name + '.mp3')

    # Anfrage an edge_tts
    communicate = edge_tts.Communicate(text=text_roh, voice=stimme)
    communicate.save_sync(audio_fname=pfad_zu_audiodatei)

    warte_fenster.destroy()

    return True


# -----------------------------------------------------------------------------
def waehle_text_datei() -> str:
    """
    Wählt eine Text-Datei aus - Format soll txt sein.
    :return: Pfad zur Text-Datei
    """

    print('\t\t wähle_text')

    pfad_zu_textdatei = gz.select_file(title='Wähle eine Text-Datei',
                                       folder=WORKING_DIR,
                                       filetypes=[['toml-Dateien', '*.toml']])

    return pfad_zu_textdatei


# -----------------------------------------------------------------------------
def zeige_fenster_fuer_texte(titel: str, pfad_zur_toml_datei: str) -> bool:
    """
    Zeigt ein Fenster für die Texte an.

        Es gibt 2 Möglichkeiten:
            - Der Text ist neu: vorlage.toml wird angezeigt.
                - Die Datei muss mit einem neuen Namen gespeichert werden
                - vorlage.toml muss gelöscht werden
            - Der Text muss bearbeitet werden:
                - eine bestehende Datei wird gezeigt
                - und auch wieder gespeichert

    :param pfad_zur_toml_datei: der Pfad zur leeren Text-toml-Datei
    :param titel: je nach Aufgabe: 'Neuer Text erstellen' oder 'Text bearbeiten'
    :return: True, wenn alles OK ist
    """

    print('\t\t zeige_fenster_fuer_texte')

    # -------------------------------------------------------------------------
    # innere Funktion
    def klicke_abbrechen() -> bool:
        """
        Schliesst das Fenster ohne Änderungen zu machen
        :return: True, wenn alles OK
        """

        text_fenster.destroy()

        # lösche vorlage.toml
        if titel == 'Neuer Text erstellen':
            os.remove(pfad_zur_toml_datei)

        return True

    # -------------------------------------------------------------------------
    # innere Funktion
    def klicke_speichern() -> bool:
        """
        Bestimmt den Dateinamen aus dem Titel des Textes.
        Speichert die geänderte Datei.
        Löscht vorlage.toml
        Schliesst das Fenster
        :return: True, wenn alles OK
        """

        # wenn neuer Text
        if titel == 'Neuer Text erstellen':

            # Bestimme neuen Dateiname aus dem Titel
            titel_roh = str(text_feld.tk.get('4.9', '4.end- 1 chars'))
            pfad_zur_toml_datei_neu = os.path.join(WORKING_DIR, 'texte', titel_roh + '.toml')

            # wenn Titel schon vorhanden?
            if os.path.exists(pfad_zur_toml_datei_neu):
                gz.warn(title='Achtung', text='Datei mit diesem Titel ist schon vorhanden.')
                return False

            # neue Datei speichern
            with open(pfad_zur_toml_datei_neu, 'w') as datei:
                datei.write(text_feld.tk.get('1.0', 'end'))

            # Vorlage löschen
            os.remove(pfad_zur_toml_datei)

        # wenn bestehender Text
        else:
            # Datei speichern
            with open(pfad_zur_toml_datei, 'w') as datei:
                datei.write(text_feld.tk.get('1.0', 'end'))

        # Fenster schliessen
        text_fenster.destroy()

        return True

    # -------------------------------------------------------------------------
    # innere Funktion
    def markiere_den_text():
        """
        Markiere den Text mit Farbe
        :return: True, wenn fertig
        """

        anzahl_linien = int(text_feld.tk.index('end').split('.')[0]) - 1

        # entfernt alle Tags
        text_feld.tk.tag_remove('kommentar', '1.0', 'end')
        text_feld.tk.tag_remove('keywords', '1.0', 'end')
        text_feld.tk.tag_remove('textzeichen', '1.0', 'end')

        # definiert Tags
        text_feld.tk.tag_config('kommentar', background='white', foreground='gray')
        text_feld.tk.tag_config('keywords', background='white', foreground='green')
        text_feld.tk.tag_config('textzeichen', background='white', foreground='red')

        keywort_liste = ['titel =', 'quelle =', 'bild =', 'text =', 'fragen =', 'antworten =']

        for i in range(1, anzahl_linien):
            buchstabe_1 = str(i) + '.0'  # erster Buchstabe der Linie i
            buchstabe_ende = str(i) + '.end'  # letzter Buchstabe der Linie i
            # OK print(i, ': ', anzeige_text.get(index1=buchstabe_1, index2=buchstabe_ende))

            # Macht die Kommentar-Linien grau
            if text_feld.tk.get(buchstabe_1) == '#':
                text_feld.tk.tag_add('kommentar', buchstabe_1, buchstabe_ende)

            # Macht die Keyworte grün
            for keywort in keywort_liste:
                buchstabe_2 = f'{i}.{len(keywort)}'  # letzter Buchstabe des Keywortes
                if keywort in text_feld.tk.get(buchstabe_1, buchstabe_ende):
                    text_feld.tk.tag_add('keywords', buchstabe_1, buchstabe_2)

            # Markiert die """ rot
            sentence = text_feld.tk.get(buchstabe_1, buchstabe_ende)
            word = '"""'
            for match in re.finditer(word, sentence):
                # OK print(match.start(), match.end())
                text_feld.tk.tag_add('textzeichen', f'{i}.{match.start()}', f'{i}.{match.end()}')

        return True

    # -------------------------------------------------------------------------
    # Lese die toml-Datei ein
    with open(pfad_zur_toml_datei, 'r') as datei:
        toml_inhalt = datei.read()

    # -------------------------------------------------------------------------
    # Fenster erstellen
    text_fenster = gz.Window(master=APP, title=titel,
                             width=600, height=700)

    text_feld = gz.TextBox(master=text_fenster, text=toml_inhalt,
                           align='top', width='fill', height=28,
                           multiline=True, scrollbar=True)

    markiere_den_text()
    text_feld.update_command(markiere_den_text)

    # Container für die Buttons unten
    button_container = gz.Box(master=text_fenster, align='bottom')
    gz.PushButton(master=button_container, text='Speichern',
                  align='left', command=klicke_speichern)
    gz.PushButton(master=button_container, text='Abbrechen',
                  align='left', command=klicke_abbrechen)

    text_fenster.show(wait=True)

    return True

