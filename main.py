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

    # Button: Fragen zu Text suchen
    gz.PushButton(master=app, text='Fragen suchen', width=100,
                  command=helfer.klicke_button_fragen_suchen)
    
    # Button: Text zu Audio
    gz.PushButton(master=app, text='Text zu Audio', width=100,
                  command=helfer.klicke_button_text_zu_audio)
    
    # Button: Erstelle alle Internet-Inhalte
    gz.PushButton(master=app, text='Texte für Internet', width=100,
                  command=helfer.klicke_button_text_zu_audio)

    # Buttons erstellen und hinzufügen
    button1 = gz.PushButton(app, text="Button 1", command=lambda: button_clicked("Button 1"))

    # Startet das Hauptfenster
    app.display()

    return True


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # helfer.teste_start()

    # helfer.erstelle_index_html()
    main()

    # # Lesen die Text-Datei
    # with open('./texte/tttesssttt.toml', 'r') as f:
    #     toml_content = f.read()

    # # Parsen des TOML-Inhalts
    # toml_doc = tomlkit.parse(toml_content)
    # text = toml_doc['text']    

    # print(helfer.formatiere_text(text_roh=text))

    # text -> text.html
    # helfer.erstelle_html_text(toml_dateiname='landleben.toml')

