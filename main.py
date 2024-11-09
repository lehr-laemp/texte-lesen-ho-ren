"""
main.py

    Startet das Programm

        fehlende Module:
            (pyinstaller), tomlkit, guizero, openai, edge-tts

        mit pyinstaller: pyinstaller --onefile --windowed main.py

"""
# -----------------------------------------------------------------------------
import guizero as gz
import tomlkit

from script_dir import helfer


# -----------------------------------------------------------------------------
def main() -> bool:
    """
    Startet die GUI
    :return: True, wenn alles OK
    """

    print()
    print(60 * 'x')
    print('Starte GUI')

    # Funktion, die aufgerufen wird, wenn ein Button gedrückt wird
    def button_clicked(button_text):
        print(f"Button '{button_text}' wurde geklickt!")

    # Hauptfenster erstellen
    app = helfer.APP

    # kann nicht vergrössert werden
    app.tk.resizable(False, False)

    # Fonts
    app.font = ('Helvetica')
    app.text_size = 20

    # Button: neuer Text erstellen
    gz.PushButton(master=app, text='Texte erstellen', width=100,
                  command=helfer.klicke_button_text_erstellen)
    
    # # Button: bestehender Text normalisieren
    # gz.PushButton(master=app, text='Texte normalisieren', width=100,
    #              command=helfer.klicke_button_text_normalisieren)

    # Button: bestehender Text bearbeiten
    gz.PushButton(master=app, text='Texte bearbeiten', width=100,
                  command=helfer.klicke_button_text_bearbeiten)
    
    # Button: Text vereinfachen
    gz.PushButton(master=app, text='Texte vereinfachen', width=100,
                  command=helfer.klicke_button_text_vereinfachen)

    # Button: Fragen zu Text suchen
    gz.PushButton(master=app, text='Fragen suchen', width=100,
                  command=helfer.klicke_button_fragen_suchen)
    
    # Button: Text zu Audio
    gz.PushButton(master=app, text='Text zu Audio', width=100,
                  command=helfer.klicke_button_text_zu_audio)
    
    # Button: Erstelle alle html-Inhalte
    gz.PushButton(master=app, text='Texte zu html', width=100,
                  command=helfer.klicke_button_texte_zu_html)
    
    # Button: Speichere die Texte im Internet
    gz.PushButton(master=app, text='Texte ins Internet', width=100,
                  command=helfer.klicke_button_texte_ins_internet)
    
    # Button: Budget bei OpenAI
    gz.PushButton(master=app, text='Budget bei OpenAI', width=100,
                  command=helfer.klicke_button_texte_ins_internet)

    # Buttons erstellen und hinzufügen
    # button1 = gz.PushButton(app, text="Button 1", command=lambda: button_clicked("Button 1"))

    # Startet das Hauptfenster
    app.display()

    return True


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # helfer.teste_start()

    # helfer.erstelle_index_html()
    main()

    # # Lesen die Text-Datei
    # with open('./texte/landleben.toml', 'r') as f:
    #     toml_content = f.read()

    # # Parsen des TOML-Inhalts
    # toml_doc = tomlkit.parse(toml_content)
    # text = toml_doc['text']    

    # print(helfer.berechne_text_schwierigkeit(text=text))

    # text -> text.html
    # helfer.erstelle_html_text(toml_dateiname='landleben.toml')

#     text = """
# Dies ist ein Text von Klexikon - das Kinderlexikon

# Das Fest Halloween ist schon sehr alt und wird jedes Jahr am 31. Oktober gefeiert. 
# Das ist der Abend vor dem 1. November, also vor Allerheiligen. 
# Der Name „Halloween“ kommt aus dem Englischen und ist eine Abkürzung für „All Hallows‘ Evening“. 
# Übersetzt bedeutet das: „der Abend vor Allerheiligen“.  

# Eigentlich kommt Halloween aus Irland, also aus Europa. 
# Dort feierten die Einwohner Irlands, die Kelten, schon vor vielen Hundert Jahren dieses Fest. 
# Sie glaubten, dass am Abend des 31. Oktobers die Toten auf die Erde zurückkehrten, um den Lebenden Streiche zu spielen. 
# Deswegen sind die meisten Halloweenkostüme gruselig. 
# Die Kelten hofften, dass die Toten dann an ihnen vorbeigehen und sie nicht als Lebende erkennen.  

# Das Fest wurde dann in den USA beliebt. 
# Es ist dort ähnlich wichtig wie woanders Fastnacht. 
# Um das Jahr 2000 kam Halloween langsam auch zu uns. 
# Manche Leute mögen es, weil sie sonst keine eigenen Traditionen mehr im Herbst haben.  

# Wie feiert man Halloween?  

# Bisher war das Gruselfest vor allem in den USA sehr beliebt. 
# Inzwischen feiern auch viele Menschen in Deutschland Halloween. 
# Besonders Kindern macht es Spass, sich als Hexen und Geister zu verkleiden und andere zu erschrecken. 
# Sie gehen dann abends von Haustüre zu Haustüre und klingeln. 
# Wenn jemand aufmacht, rufen sie „Süsses, sonst gibt’s Saures!“. 
# Meistens bekommen die Kinder dann Süßigkeiten.  

# Besonders beliebt ist auch die Kürbislaterne, die oft schon an den Tagen vor Halloween hergestellt wird. 
# Dazu höhlt man einen Kürbis aus und schnitzt ein Gesicht hinein. 
# Dann legt man eine Kerze in den Kürbis und kann ihn in den Garten oder auf einen Balkon stellen. 
# Damit man das ausgehöhlte Fruchtfleisch nicht wegwerfen muss, kann man daraus eine Kürbissuppe kochen.  

# In den USA ist es auch üblich, dass junge Leute zu Halloween-Partys einladen. 
# Man bittet die Gäste, in einem passenden Kostüm zu kommen. 
# Sie spielen dann Spiele oder erzählen einander gruselige Geschichten. 
# """

#     helfer.berechne_text_schwierigkeit(text=text)
