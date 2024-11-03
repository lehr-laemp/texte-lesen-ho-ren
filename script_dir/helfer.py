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
import pysbd

import os
import re
from random import choice
import subprocess
import datetime
import time
import webbrowser


# -----------------------------------------------------------------------------
APP = gz.App(title='Training Verstehen', width=230, height= 350)
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

Bitte gib die Fragen als html-Liste zurück und nummeriere sie.
Zum Beispiel so: 
<h2>Fragen</h2>
<p>
<ol>
    <li>Wer ist Ute?</li>
    <li>Wo arbeitet Ute am Morgen?</li>
</ol>
</p>

Und dann noch als html-Liste mit den Frage-Antwort-Paaren.
Zum Beispiel so: 
<h2>Antworten</h2>
<p>
    <details>
        <ol>
            <li>Wer ist Ute? <br>
                Ute ist ein Bauern-Mädchen im Mittelalter.</li>
            <li>Wo arbeitet Ute am Morgen? <br>
                Sie arbeitet im Garten.</li>
        </ol>
    </details>
</p>

Das ist der Text: 

"""

HTML_KOPF = """
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="de" xml:lang="de">
<head>
<title>Training: Lesen und hören</title>
<meta charset="utf-8">
<meta name="description" content="Training: Lesen und hören">
<meta name="author" content="Hansruedi Meyer">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<style>html{line-height:1.7;font-family:Helvetica,sans-serif;font-size:20px;color:black;background-color:white} body{margin:0 auto;max-width:33em;padding:50px;hyphens:none;overflow-wrap:break-word;text-rendering:optimizeLegibility;font-kerning:normal} @media(max-width:600px){body{font-size:.9em;padding:1em}h1{font-size:1.8em}} @media print{body{background-color:transparent;color:black;font-size:12pt} p,h2,h3{orphans:3;widows:3} h2,h3,h4{page-break-after:avoid}}p{margin:1em 0} a{color:green; margin-left: 0%;} img{max-width:100%}h1,h2,h3{margin-top:1.4em;color: green;} ol,ul{padding-left:1.7em;margin-top:1em} li>ol,li>ul{margin-top:0}hr{background-color:black;border:0;height:1px;margin:1em 0} summary{font-weight:bolder;color:black;padding:1.2rem;margin-bottom:1.2rem;border-radius:.5rem;cursor:pointer}
</style>
</head>
<body>

"""


# -----------------------------------------------------------------------------
def erstelle_html_audio(toml_dateiname: str) -> bool:
    """
    Erstellt aus der toml-Datei die Seite zum Hören.
        Sie wird im Ordner 'mat' gespeichert.
    :return: True, wenn alles OK    
    """

    print(f'\t\t erstelle_html_audio aus {toml_dateiname}')

    # toml-Datei einlesen
    with open(file=os.path.join(WORKING_DIR, 'texte', toml_dateiname), 
                mode='r', encoding='utf-8') as file:
        toml_content = file.read()
    toml_doc = tomlkit.parse(toml_content)

    # Test, ob Audio-Datei zu diesem Text schon vorhanden ist, sonst Abbruch
    pfad_zu_audiodatei = os.path.join(WORKING_DIR, 'mat', toml_doc['dateiname'] + '.mp3')
    if not os.path.exists(pfad_zu_audiodatei):
        print()
        print(f'ACHTUNG: Audiodatei zu {toml_dateiname} fehlt.')
        return False
    
    # Inhalte für html-Datei zusammenstellen
    html_inhalt = HTML_KOPF
    html_inhalt += f'<h1>{toml_doc['titel']}</h1> \n'
    html_inhalt += """
<p>
    <ul>
        <li>Mache dir <strong>Notizen.</strong></li>
        <li>Tipp: Du kannst den Hörtext stoppen und dann schreiben.</li>
        <li>Du kannst den Text auch nochmals hören.</li>
        <li>Beantworte die Fragen <strong>nach</strong> dem Hören schriftlich.</li>
        <li>Schreibe ganze Sätze als Antworten.</li>
        <li>Kontrolliere deine Antworten, vielleicht musst du den Text nochmals hören.</li>
    </ul>
</p>

"""

    # Muster auswählen
    muster_liste = ['muster1.png', 'muster2.png', 'muster3.png', 'muster4.png',]
    html_inhalt += f'\n<p><img src="{choice(muster_liste)}" alt="Muster" width="100%"></p> \n\n'

    html_inhalt += f'<p><a href="{toml_doc['dateiname']}.mp3" target="_blank">Hörtext</a></p> \n\n'

    # Muster auswählen
    html_inhalt += f'\n<p><img src="{choice(muster_liste)}" alt="Muster" width="100%"></p> \n\n'

    html_inhalt += toml_doc['fragen']

    html_inhalt += f'\n<p><img src="{choice(muster_liste)}" alt="Muster" width="100%"></p> \n\n'

    html_inhalt += toml_doc['antworten']

    html_inhalt += f'\n<p><img src="{choice(muster_liste)}" alt="Muster" width="100%"></p> \n\n'

    html_inhalt += '</body> \n</html> \n'

    # und speichern
    datei_name = os.path.join(WORKING_DIR, 'mat', toml_doc['dateiname'] + '-audio.html')
    with open(file=datei_name, mode='w', encoding='utf-8') as datei:
        datei.write(html_inhalt)


    return True


# -----------------------------------------------------------------------------
def erstelle_html_text(toml_dateiname: str) -> bool:
    """
    Erstellt aus der toml-Datei die Seite zum Lesen.
        Sie wird im Ordner 'mat' gespeichert.
    :return: True, wenn alles OK    
    """

    print(f'\t\t erstelle_html_text aus {toml_dateiname}')

    # toml-Datei einlesen
    with open(file=os.path.join(WORKING_DIR, 'texte', toml_dateiname), 
                mode='r', encoding='utf-8') as file:
        toml_content = file.read()
    toml_doc = tomlkit.parse(toml_content)

    # Inhalte für html-Datei zusammenstellen
    html_inhalt = HTML_KOPF
    html_inhalt += f'<h1>{toml_doc['titel']}</h1> \n'
    html_inhalt += """
<p>
    <ul>
        <li>Lies den Text genau und mache dir <strong>Notizen.</strong></li>
        <li>Du kannst den Text auch nochmals lesen.</li>
        <li>Beantworte die Fragen <strong>nach</strong> dem Lesen schriftlich.</li>
        <li>Schreibe ganze Sätze als Antworten.</li>
        <li>Kontrolliere deine Antworten, vielleicht musst du den Text nochmals lesen.</li>
    </ul>
</p>

"""

    # Muster auswählen
    muster_liste = ['muster1.png', 'muster2.png', 'muster3.png', 'muster4.png',]
    html_inhalt += f'\n<p><img src="{choice(muster_liste)}" alt="Muster" width="100%"></p> \n\n'

    html_inhalt += '<h2>Text</h2> \n'
    html_inhalt += formatiere_text(text_roh=toml_doc['text'])

    # Muster auswählen
    html_inhalt += f'\n<p><img src="{choice(muster_liste)}" alt="Muster" width="100%"></p> \n\n'

    html_inhalt += toml_doc['fragen']

    html_inhalt += f'\n<p><img src="{choice(muster_liste)}" alt="Muster" width="100%"></p> \n\n'

    html_inhalt += toml_doc['antworten']

    html_inhalt += f'\n<p><img src="{choice(muster_liste)}" alt="Muster" width="100%"></p> \n\n'

    html_inhalt += '</body> \n</html> \n'

    # und speichern
    datei_name = os.path.join(WORKING_DIR, 'mat', toml_doc['dateiname'] + '-text.html')
    with open(file=datei_name, mode='w', encoding='utf-8') as datei:
        datei.write(html_inhalt)

    return True



# -----------------------------------------------------------------------------
def erstelle_index_html() -> bool:
    """
    Erstellt die Datei index.html
        Sammelt aus dem Ordner texte alle Infos
        und stellt daraus den Inhalt zusammen.
    :return: True, wenn alles OK
    """

    print('\t\t erstelle_index_html')

    # Inhalt von index.html zusammenstellen
    index_inhalt = HTML_KOPF
    index_inhalt += '<h1>Training: Lesen und hören</h1> \n'
    index_inhalt += """
<p>
    Hier kannst du Texte lesen oder hören. <br>
    Und dann Fragen dazu beantworten.
    <br><br>
</p>

"""

    # Muster auswählen
    muster_liste = ['mat/muster1.png', 'mat/muster2.png', 'mat/muster3.png', 'mat/muster4.png',]
    index_inhalt += f'<p><img src="{choice(muster_liste)}" alt="Muster" width="100%"></p> \n'
    index_inhalt += '<br> \n\n'

    # Abfragen, welche Dateien im Ordner texte sind
    dateien = os.listdir(os.path.join(WORKING_DIR, 'texte'))
    # OK print(dateien) # ['.DS_Store', 'landleben.toml', 'test.toml']

    # Dateien durchgehen
    for datei in dateien:
        # .DS_Store ausschliessen
        if datei != '.DS_Store':
            
            # toml-Datei einlesen
            with open(file=os.path.join(WORKING_DIR, 'texte', datei), 
                      mode='r', encoding='utf-8') as file:
                toml_content = file.read()
            toml_doc = tomlkit.parse(toml_content)

            # Test, ob Audio-Datei zu diesem Text schon vorhanden ist, sonst Abbruch
            pfad_zu_audiodatei = os.path.join(WORKING_DIR, 'mat', toml_doc['dateiname'] + '.mp3')
            if not os.path.exists(pfad_zu_audiodatei):
                print()
                print(f'ACHTUNG: Audiodatei zu {datei} fehlt.')
                return False    

            # Links zu den Seiten zusammenstellen
            index_inhalt += '<p> \n'
            index_inhalt += f'{toml_doc['titel']} \n'
            index_inhalt += f'<a href="mat/{toml_doc['dateiname']}-text.html" target="_blank"> Lesen</a> &nbsp; \n'
            index_inhalt += f'<a href="mat/{toml_doc['dateiname']}-audio.html" target="_blank"> hören</a> \n'
            index_inhalt += '</p> \n\n'

            # toml_doc wieder bereit machen für die nächste Datei
            toml_doc = ''

            # die verlinkten Dateien erstellen
            erstelle_html_audio(toml_dateiname=datei)
            erstelle_html_text(toml_dateiname=datei)


    # noch ein Muster
    index_inhalt += '<br> \n'
    index_inhalt += f'<p><img src="{choice(muster_liste)}" alt="Muster" width="100%"></p> \n\n'

    # Abschluss der html-Datei
    index_inhalt += '</body>\n</html>\n' 

    # index.html speichern
    with open(file='index.html', mode='w') as datei:
        datei.write(index_inhalt)       

    return True


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
    toml_doc.add(tomlkit.comment('Name der toml-Datei'))
    toml_doc.add('dateiname', '')
    
    toml_doc.add(tomlkit.nl())
    toml_doc.add(tomlkit.comment('Titel des Textes'))
    toml_doc.add('titel', '')

    toml_doc.add(tomlkit.nl())
    toml_doc.add(tomlkit.comment('Quelle des Textes'))
    toml_doc.add('quelle', '')

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
def formatiere_text(text_roh: str) -> str:
    """
    Formatiert den Text für die html-Datei.
        Abschnitte werden mit <p></p> umgeben.
        Abstände mit <br> markiert

    :param text_roh: der unformatierte Text
    :return: den formatierten Text 
    """

    print('\t\t\t formatiere_text')

    # der formatierte Text wird stückweise zusammengesetzt
    text_formatiert = '<p>\n'

    # satzweise durch den Text gehen
    text_saetze = text_roh.split('\n')
    for satz in text_saetze:
        # print(satz)
        if satz == '':
            text_formatiert += '</p>\n<p>\n'
        else:
            text_formatiert += satz + '\n'
    text_formatiert += '</p>'        

    return text_formatiert


# -----------------------------------------------------------------------------
def normalisiere_text(text_roh: str) -> str:
    """
    Normalisiert den Text: 
        Jeder Satz kommt auf eine neue Linie.
        Alle '\n' dazwischen werden gelöscht 
    

    :param text_roh: der unformatierte Text
    :return: den formatierten Text 
    """

    print('\t\t\t normalisiere_text')

    # print(text_roh[0:500], '\n\n')

    text_return = ''

    # alle 'wilden' \n ersetzen
    text_roh = text_roh.replace('\n', ' ')

    # Text in Sätze zerlegen
    # Infos: https://github.com/nipunsadvilkar/pySBD/tree/master
    seg = pysbd.Segmenter(language="de", clean=False)
    saetze = seg.segment(text=text_roh)
    # print(saetze)

    for satz in saetze:
        text_return += satz + '\n'

    # print(text_return)    
    return text_return


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

    print('\n\t klicke_button_fragen_suchen')

    # Datei wählen
    pfad_zu_textdatei = waehle_text_datei()
    
    # wenn keine Datei gewählt
    if pfad_zu_textdatei == '':
        print('Keine Datei gewählt.')
        return False

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

    print('\n\t klicke_button_text_bearbeiten')

    # Datei wählen
    pfad_zu_textdatei = waehle_text_datei()
    
    # wenn keine Datei gewählt
    if pfad_zu_textdatei == '':
        print('Keine Datei gewählt.')
        return False

    # Fenster zum Bearbeiten öffnen
    zeige_fenster_extern(pfad_zu_toml_datei=pfad_zu_textdatei)
    # zeige_fenster_fuer_texte(titel='Text bearbeiten',
    #                          pfad_zur_toml_datei=pfad_zu_textdatei)

    return True


# -----------------------------------------------------------------------------
def klicke_button_text_erstellen() -> bool:
    """
    Startet alle Prozesse, wenn der Button "Text erstellen" geklickt wird
    :return: True, wenn alles OK
    """

    print('\n\t klicke_button_text_erstellen')

    # leere Text-Datei (im toml-Format) erstellen
    pfad_zur_neuen_datei = erstelle_leere_text_datei()

    # leere Text-Datei zum Bearbeiten öffnen
    zeige_fenster_fuer_texte(titel='Neuer Text erstellen',
                             pfad_zur_toml_datei=pfad_zur_neuen_datei)

    return True


# -----------------------------------------------------------------------------
def klicke_button_text_normalisieren() -> bool:
    """
    Startet alle Prozesse, wenn der Button "Texte normalisieren" geklickt wird.
        Normalisieren meint: Der Text ist so gespeichert, 
            dass jeder Satz auf einer neuen Linie beginnt.
    :return: True, wenn alles OK
    """

    print('\n\t klicke_button_text_normalisieren')

    # zu normalisierenden Text auswählen
    # Datei wählen
    pfad_zu_textdatei = waehle_text_datei()

    # wenn keine Datei gewählt
    if pfad_zu_textdatei == '':
        print('Keine Datei gewählt.')
        return False

    # Lesen die Text-Datei
    with open(pfad_zu_textdatei, 'r') as datei:
        toml_content = datei.read()

    # Parsen des TOML-Inhalts
    toml_doc = tomlkit.parse(toml_content)
    text_roh = toml_doc['text']   

    # Text normalisieren,
    text_normalisiert = normalisiere_text(text_roh=text_roh)

    # in die Toml-Datei schreiben
    toml_doc['text'] = tomlkit.string(text_normalisiert, multiline=True)
    toml_content = tomlkit.dumps(toml_doc)

    # und speichern
    with open(pfad_zu_textdatei, 'w') as datei:
        datei.write(toml_content)

    return True


# -----------------------------------------------------------------------------
def klicke_button_text_zu_audio() -> bool:
    """
    Wandelt den Text in eine Audio-Datei um.
    :return: True, wenn alles OK.
    """

    print('\n\t klicke_button_text_zu_audio')

    # Datei wählen
    pfad_zu_textdatei = waehle_text_datei()

    # wenn keine Datei gewählt
    if pfad_zu_textdatei == '':
        print('Keine Datei gewählt.')
        return False

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
    pfad_zu_audiodatei = os.path.join(WORKING_DIR, 'mat', datei_name + '.mp3')

    # Anfrage an edge_tts
    communicate = edge_tts.Communicate(text=text_roh, voice=stimme)
    communicate.save_sync(audio_fname=pfad_zu_audiodatei)

    warte_fenster.destroy()

    return True


# -----------------------------------------------------------------------------
def klicke_button_texte_ins_internet() -> bool:
    """
    Stellt die Texte ins Internet.

    :return: True, wenn alles OK.
    """

    print('\n\t klicke_button_texte_ins_internet')

    aktuelle_zeit = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")

    mache_lokalen_commit(kommentar=aktuelle_zeit)

    mache_push_zu_github()

    # warte etwas und zeige dann die erstellte Seite
    
    gz.info(title='Info', text='Bis die Seiten aktualisiert sind, dauert es einige Minuten')

    webbrowser.open(url='https://lehr-laemp.github.io/texte-lesen-ho-ren/')


    return True


# -----------------------------------------------------------------------------
def klicke_button_texte_zu_html() -> bool:
    """
    Erstellt aus allen Texten index.html und 
        die zugehörigen Seiten im Ordnern mat.

    :return: True, wenn alles OK.
    """

    print('\n\t klicke_button_texte_zu_html')

    erstelle_index_html()

    return True


# -----------------------------------------------------------------------------
def mache_lokalen_commit(kommentar: str) -> bool:
    """
    Mach ein Commit der lokalen Dateien
    :param kommentar: Kommentar für den commit
    :return: True, wenn alles OK
    """

    print('\t mache_lokalen_commit')

    repo_pfad = WORKING_DIR

    try:
        # Schritt 0: git config --global user.name "user.name" - User bestimmen
        # Schritt 0: git config --global user.email "user.email" - User bestimmen
        # git_befehl = ['git', 'config', '--global', 'user.name', constanten.GIT_USER]
        # subprocess.run(git_befehl, check=True)
        # git_befehl = ['git', 'config', '--global', 'user.email', constanten.GIT_USER_MAIL]
        # subprocess.run(git_befehl, check=True)

        # Schritt 1: git add . - Alle Änderungen hinzufügen
        git_befehl = ["git", "-C", repo_pfad, "add", "."]
        subprocess.run(git_befehl, check=True)

        # Schritt 2: git commit -m "Nachricht" - Änderungen committen
        git_befehl = ["git", "-C", repo_pfad, "commit", "-m", kommentar]
        subprocess.run(git_befehl, check=True)

        print("\n\t Änderungen erfolgreich committed")

        return True

    except subprocess.CalledProcessError as e:
        print(f"\t Achtung: Fehler beim Ausführen von Git: {e}")

        return False


# -----------------------------------------------------------------------------
def mache_push_zu_github() -> bool:
    """
    Macht einen Push des git-Ordners nach Github
    :return: True, wenn alles OK
    """

    print('\t mache_push_zu_github')

    repo_pfad = WORKING_DIR
    repo_name = 'texte-lesen-ho-ren'
    GIT_USER = 'lehr-laemp'
    GITHUB_ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')

    try:
        
        # Schritt 1: git push
        # git_befehl = ['git', 'push', 'origin', 'master']
        git_url = (f'https://{GITHUB_ACCESS_TOKEN}@github.com'
                   f'/{GIT_USER}/{repo_name}')
        git_befehl = ['git', 'remote', 'set-url', 'origin', git_url]
        # print(git_befehl)
        subprocess.run(git_befehl, check=True)
        # ddd
        git_befehl = ['git', 'push', '--set-upstream', 'origin', 'master']
        subprocess.run(git_befehl, check=True)

        print('\n\t Änderungen erfolgreich gepusht.')

        return True

    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen von Git: {e}")

        return False


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
    
    if pfad_zu_textdatei == '':
        return ''

    return pfad_zu_textdatei


# -----------------------------------------------------------------------------
def zeige_fenster_extern(pfad_zu_toml_datei: str) -> bool: 
    """
    Zeige ein neues Fenster von Visual-Code mit der Datei pfad_zu_toml_datei

    :return: True, wenn alles OK
    """

    print('\t\t zeige_fenster_extern')

    # Befehl für subprocess
    run_befehl = ['code', '-n', pfad_zu_toml_datei]
    subprocess.run(args=run_befehl)

    return True



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
            titel_roh = str(text_feld.tk.get('4.13', '4.end- 1 chars'))
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

            # Text normalisieren beim Speichern
            # Lesen die Text-Datei
            with open(pfad_zur_toml_datei_neu, 'r') as datei:
                toml_content = datei.read()

            # Parsen des TOML-Inhalts
            toml_doc = tomlkit.parse(toml_content)
            text_roh = toml_doc['text']    

            # Text normalisieren
            toml_doc['text'] = tomlkit.string(normalisiere_text(text_roh=text_roh), multiline=True)

            # toml-Daten dumpen ...
            toml_content = tomlkit.dumps(toml_doc)

            # und speichern
            with open(pfad_zur_toml_datei_neu, 'w') as datei:
                datei.write(toml_content)
            
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

        keywort_liste = ['dateiname =', 'titel =', 'quelle =', 'text =', 'fragen =', 'antworten =', 'ki_antwort =']

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
        toml_string = datei.read()

    # -------------------------------------------------------------------------
    # Fenster erstellen
    text_fenster = gz.Window(master=APP, title=titel,
                             width=600, height=700)

    text_feld = gz.TextBox(master=text_fenster, text=toml_string,
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

