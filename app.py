from flask import Flask, render_template, request
import spacy
import pandas as pd

# Load the trained NER model
nlp = spacy.load("Character_NER_Model")  # Adjust path if necessary

# Load the dataset (Ensure this CSV is inside WHOAPPEARSWHERE/)
csv_path = "Friends_Journey_Dataset.csv"
df = pd.read_csv(csv_path)
df.fillna("", inplace=True)  # Handle NaN values

app = Flask(__name__)

def find_character_chapters(character_name):
    """
    Searches the dataset for chapters where the given character appears.
    """
    mask = df["Character Names"].str.contains(character_name, case=False, na=False)
    chapters = df.loc[mask, "Chapter Number"].unique()

    return list(chapters) if chapters.any() else ["Not found"]

@app.route("/", methods=["GET", "POST"])
def index():
    chapters = None
    character_name = ""

    if request.method == "POST":
        character_name = request.form["character_name"]
        chapters = find_character_chapters(character_name)

    return render_template("index.html", character_name=character_name, chapters=chapters)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
