from fpdf import FPDF
import json
import os


IMG_DIR = "../../img/"
TEAM_ORDER = ["Townsfolk", "Outsider", "Minion", "Demon","Traveller", "Fabled"]
TEAM_IGNORE = ["Traveller", "Fabled"]
TEAM_TRANSLATED = {"Townsfolk": "Mieszczanie", "Outsider": "Przybysze", "Minion": "Sługusi", "Demon": "Demony"}
FONT_PATH = "fonts/DejaVuSans.ttf"
FONT_BOLD_PATH = "fonts/DejaVuSans-Bold.ttf"

class PDF(FPDF):
    def header(self):
        pass
    
    def top(self,title,author):
        self.set_font("DejaVu", "B", size=12)
        self.cell(0, 5, f"   {title}   autorstwa   {author}", ln=True, align="C")
        self.ln(2)
    
    def chapter_title(self, title):
        self.set_font("DejaVu", "B", size=10)
        self.line(10, self.get_y()+2, 165, self.get_y()+2)
        self.set_x(170)
        self.cell(0, 5, title, ln=True, align="L")
        self.ln(2)

    def character_row(self, img_path, name : str, ability):
        if os.path.exists(img_path):
            self.image(img_path, x=5, y=self.get_y()-4, w=10)
        self.set_x(15)
        self.set_font("DejaVu", "B", size=8)
        y1 = self.get_y() -1
        self.multi_cell(22, 3, name)
        y2 = self.get_y() +3
        self.set_y(y1)
        self.set_x(37)
        self.set_font("DejaVu", size=8)
        self.multi_cell(0, 4, ability)
        if self.get_y() < y2: self.set_y(y2)
        self.ln(2)
        print("Przetwarzam",name)

# Wczytaj dane z JSON

def work():
    input_json_file = [f for f in os.listdir() if f.endswith('_PL.json')]
    if len(input_json_file) != 1:
        print("Folder musi zawierać dokładnie jeden plik _PL.json z przetłumaczonym skryptem.")
        return
        
    input_json_file = input_json_file[0]
    with open(input_json_file, "r", encoding="utf-8") as f:
        characters = json.load(f)

    
    # Posortuj postacie według drużyny
    header_data = characters[0]
    sorted_characters = sorted(characters[1:], key=lambda x: TEAM_ORDER.index(x["team"]))

    pdf = PDF()
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.add_font("DejaVu", "B", FONT_BOLD_PATH, uni=True)
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    pdf.top(header_data.get("name", "Nowy skrypt"), header_data.get("author", "?"))

    

    current_team = None
    for char in sorted_characters:
        if char["team"] in TEAM_IGNORE:
            continue
        if char["team"] != current_team:
            current_team = char["team"]
            pdf.chapter_title(TEAM_TRANSLATED[current_team])
        
        img_path = os.path.join(IMG_DIR, f"Icon_{char['id'].replace('pl_PL_', '')}.png")
        pdf.character_row(img_path, char["name"], char["ability"])

    filename = f"{ header_data.get('name', 'Nowy skrypt') }_PL.pdf"
    pdf.output(filename)
    print("PDF wygenerowany jako",filename)

if __name__ == "__main__":
    work()