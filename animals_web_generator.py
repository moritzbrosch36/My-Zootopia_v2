from pathlib import Path
import requests

def fetch_animal_data(animal_name, api_key):
    """
    Fetch animal data from API Ninjas (Animals API) for a given animal name.

    Args:
        animal_name (str): Common name or partial name of the animal to search.
        api_key (str): Your valid API Ninjas key.

    Returns:
        list[dict]: Parsed JSON list of animal data, or empty list on error.
    """
    url = "https://api.api-ninjas.com/v1/animals"
    params = {'name': animal_name}
    headers = {'X-Api-Key': api_key}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API error {response.status_code}: {response.text}")
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
    return []


def load_template(template_path):
    """
    Load the HTML template from a file.

    Args:
        template_path (str): Path to the template file.

    Returns:
        str: Template content, or a minimal fallback HTML if loading fails.
    """
    try:
        return Path(template_path).read_text(encoding = "utf-8")
    except FileNotFoundError:
        print(f"❌ Template '{template_path}' not found.")
        return "<html><body><h1>Error: template missing</h1></body></html>"


def generate_cards_html(animal_data):
    """
    Dynamically generate HTML for each animal in the list.

    Args:
        animal_data (list[dict]): List of animal data dictionaries.

    Returns:
        str: HTML string containing <li> elements for each animal.
    """
    html_output = ""
    for data in animal_data:
        info = {
            "Name": data.get("name", "Unknown"),
            **data.get("characteristics", {}),
        }
        if locations := data.get("locations"):
            info["Locations"] = ", ".join(locations)

        html_output += '<li class="cards__item">\n'
        html_output += f'  <h2 class="card__title">{info.get("Name")}</h2>\n'
        html_output += '  <div class="card__text">\n'
        for key, value in info.items():
            if key != "Name" and value:
                html_output += f'    <p><strong>{key}:</strong> {value}</p>\n'
        html_output += '  </div>\n</li>\n'

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
