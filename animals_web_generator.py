import json

def load_data(file_path):
    """
    Load a JSON file and return its contents as a Python object.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list[dict]: Parsed JSON data as a list of dictionaries.
                    Returns an empty list if the file is missing or invalid.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error: File '{file_path}' is not valid JSON.")
        return []


def generate_cards_html(animal_data):
    """
    Generate HTML markup for a list of animal cards.

    Each card contains:
      - Name (as the card title)
      - Diet
      - Locations
      - Type

    Args:
        animal_data (list[dict]): List of animal dictionaries.

    Returns:
        str: HTML string with <li> elements for all animals.
    """
    html_output = ""
    for data in animal_data:
        info = {
            "Name": data.get("name"),
            "Diet": data.get("characteristics", {}).get("diet"),
            "Locations": ", ".join(data.get("locations", [])) if data.get("locations") else None,
            "Type": data.get("characteristics", {}).get("type")
        }

        html_output += '<li class="cards__item">\n'
        html_output += f'  <h2 class="card__title">{info["Name"]}</h2>\n'
        html_output += '  <div class="card__text">\n'
        for key, value in info.items():
            if key != "Name" and value is not None:
                html_output += f'    <p><strong>{key}:</strong> {value}</p>\n'
        html_output += "  </div>\n</li>\n"

    return html_output


if __name__ == "__main__":
    """
    Main entry point:
      1. Load animal data from JSON file.
      2. Generate HTML card markup.
      3. Load the external HTML template.
      4. Insert cards into the template at {{cards}} placeholder.
      5. Save the final HTML to 'animals.html'.
    """
    # Load data
    animal_data = load_data("../My-Zootopia/animals_data.json")
    cards_html = generate_cards_html(animal_data)

    # Load template
    with open("animals_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Replace placeholder with generated cards
    final_html = template.replace("{{cards}}", cards_html)

    # Save final HTML
    with open("animals.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("✅ HTML has been generated and saved to animals.html")
