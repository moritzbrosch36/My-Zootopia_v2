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
    except requests.RequestException as error_network:
        print(f"❌ Network error: {error_network}")
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
    Only includes: Name, Diet, Locations, and Type.

    Args:
        animal_data (list[dict]): List of animal data dictionaries.

    Returns:
        str: HTML string containing <li> elements for each animal.
    """
    html_output = ""
    for data in animal_data:
        info = {
            "Name": data.get("name", "Unknown"),
            "Diet": data.get("characteristics", {}).get("diet"),
            "Locations": ", ".join(data.get("locations", []))
            if data.get("locations") else None,
            "Type": data.get("characteristics", {}).get("type")

        }

        html_output += '<li class="cards__item">\n'
        html_output += f'  <h2 class="card__title">{info["Name"]}</h2>\n'
        html_output += '  <div class="card__text">\n'
        for key, value in info.items():
            if key != "Name" and value:
                html_output += f'    <p><strong>{key}:</strong> {value}</p>\n'
        html_output += '  </div>\n</li>\n'

    return html_output


def save_html(output_path, content):
    """
    Save the final HTML content to a file.

    Args:
        output_path (str): File path to write HTML content into.
        content (str): Complete HTML markup.
    """
    try:
        Path(output_path).write_text(content, encoding = "utf-8")
        print(f"✅ HTML successfully saved to {output_path}")
    except Exception as error_HTML:
        print(f"❌ Could not save HTML: {error_HTML}")


if __name__ == "__main__":
    api_key = "MrMUawMRUvQsI/dVxqEXdQ==FMVMuB2VCKdBcIk4"
    template_file = "animals_template.html"
    output_file = "animals.html"

    animal_name = input("🔍 Enter the name of an animal: ").strip()

    # Fetch data
    animal_data = fetch_animal_data(animal_name, api_key)
    if not animal_data:
        print("⚠️ No animal data received; HTML will be empty.")

    # Generate the HTML cards
    cards_html = generate_cards_html(animal_data)

    # Load the template
    template = load_template(template_file)

    # Insert generated cards
    final_html = template.replace("{{cards}}", cards_html)

    # Save final HTML
    save_html(output_file, final_html)
