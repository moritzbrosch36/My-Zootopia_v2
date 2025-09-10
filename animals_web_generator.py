from pathlib import Path
import data_fetcher


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
    if not animal_data:
        return f"""
            <li class="cards__item">
              <h2 class="card__title">No results</h2>
              <div class="card__text">
                <p>❌ No animal with the name "<strong>{animal_name}
                </strong>" was found. ❌</p>
              </div>
            </li>
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
    template_file = "animals_template.html"
    output_file = "animals.html"

    animal_name = input("🔍 Enter the name of an animal: ").strip()

    # Fetch data
    animal_data = data_fetcher.fetch_data(animal_name)
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
