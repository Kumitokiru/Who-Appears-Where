from flask import Flask, render_template, request
import spacy
import pandas as pd

# Load the trained NER model
nlp = spacy.load("Character_NER_Model")  # Adjust path if necessary

# Load the dataset
csv_path = "Friends_Journey_Dataset.csv"
df = pd.read_csv(csv_path)
df.fillna("", inplace=True)  # Handle NaN values

app = Flask(__name__)

# ================================
# 🔥 Character Search with Chapter Count
# ================================
def find_character_chapters(character_name, story_chapters=None):
    """
    Searches the dataset or scraped story for character appearances.
    Returns the chapters and the number of chapters.
    """
    if story_chapters:
        chapters = story_chapters.get(character_name, ["Not found"])
        return chapters, len(chapters) if chapters != ["Not found"] else 0

    # Search dataset
    mask = df["Character Names"].str.contains(character_name, case=False, na=False)

    if mask.any():
        results = df.loc[mask, ["Season Number", "Chapter Number"]]
        chapters = [f"Season {row['Season Number']} Chapter {row['Chapter Number']}" for _, row in results.iterrows()]
        return chapters, len(chapters)
    else:
        return ["Not found"], 0

# ================================
# 🔥 Flask Routes
# ================================
@app.route("/", methods=["GET", "POST"])
def index():
    chapters = None
    character_name = ""
    chapter_count = 0

    if request.method == "POST":
        character_name = request.form["character_name"]
        chapters, chapter_count = find_character_chapters(character_name)

    return render_template("index.html", character_name=character_name, chapters=chapters, chapter_count=chapter_count)

# ================================
# 🔥 Start the App
# ================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
