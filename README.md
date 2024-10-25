---

# AI TaleCraft

A simple and fun web application that generates personalized stories based on keywords! Built with Flask, this app allows users to input keywords, and it then returns a story generated based on these inputs.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)


---

## Features

- **Interactive Story Generation**: Users enter keywords, and the app dynamically generates a story based on these inputs.
- **Flask Backend**: Handles the form submission and story generation process.
- **Easy-to-Use Interface**: Simple input field and story output display.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/NareshGusain/AI_Tailcraft_RBL
    cd story-generator
    ```

2. **Install dependencies**:
   Ensure you have Python and pip installed. Then, use the following command:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Start the Flask server:
   ```bash
   python app.py
   ```

4. **Access the app**:
   Open your browser and go to `http://localhost:8080` to see the app in action.

## Usage

1. Navigate to the main page.
2. Enter a few fun keywords (e.g., "dragon," "princess," "forest").
3. Click "Create Story" to generate a story based on the input keywords.
4. The generated story will appear below the input form.

## Project Structure

Here's a breakdown of the project's structure:

```plaintext
story-generator/
│
├── app.py               # Main Flask application file
├── api.py               # Story generation logic
├── requirements.txt     # Python dependencies
├── templates/
│   ├── index.html       # Main HTML template for the homepage
│   └── storytime.html   # Template for displaying generated stories
└── static/
    └── style.css        # CSS styling for the app (if any)
```

## Contributing

Contributions are welcome! If you’d like to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

---