# My-Zootopia_v2

Animal Cards Project
====================

This Python script generates an HTML file with animal maps.
The data is loaded using the `data_fetcher` module, inserted into a template,
and saved as a finished web page.

Functions:
- load_template(): Loads an HTML template.
- generate_cards_html(): Dynamically creates cards for animals.
- save_html(): Saves the finished HTML file.

Usage:
1. Run the script with `python main.py`.
2. Enter the name of an animal.
3. The data is retrieved and saved as an HTML file (`animals.html`).
4. Open the file in your browser to view the results.

Files:
- animals_template.html → Template with placeholder `{{cards}}`.
- animals.html → Output with the generated animal cards.
- data_fetcher.py → Module that retrieves the animal data.

Requirements:
- Python 3.x
- The `data_fetcher` module must be present in the project.