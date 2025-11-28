# Live Cricket Scores Flask Application

This is a simple Python Flask application that fetches live cricket scores from an RSS feed and displays them in a user-friendly interface. The application includes features like filtering by match type and region, a responsive design, and a modern theme with hover animations.

## Features

*   **Live Score Display**: Fetches and displays live cricket match scores from `https://static.cricinfo.com/rss/livescores.xml`.
*   **Filtering**: Allows users to filter matches by:
    *   **Match Type**: (e.g., T20, ODI, Test, Women's, Domestic) inferred from match titles.
    *   **Region/Team**: (e.g., Hyderabad, Punjab, Brisbane Heat Women) inferred from team names in match titles.
*   **Responsive Design**: Adapts layout for various screen sizes (desktops, tablets, mobiles).
*   **Theming**: Features a custom color theme with a white background, dark green and beige accents, and gold highlights.
*   **UI Enhancements**: Includes centered titles, increased card heights, scaling and hover animations for match cards.
*   **Interactive Elements**: Uses dropdowns for filtering and buttons for links to match details.

## Technologies Used

*   **Backend**: Python with Flask
*   **RSS Parsing**: `feedparser` library
*   **Frontend**: HTML, CSS (with CSS Grid for layout and responsive media queries)
*   **Dependencies**: Flask, feedparser

## Setup and Installation

1.  **Clone the Repository** (If applicable):
    ```bash
    git clone https://github.com/M-fatimaZohra/Live-Cricket-Match-Reader-Gemini 
    cd <project-directory>
    ```
    *(Note: If you are working directly with the files, you can skip this step and ensure you are in the project's root directory.)*

2.  **Set up a Virtual Environment** (Recommended):
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    The project uses a `requirements.txt` file to manage dependencies. Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```
    *(This command will install Flask and feedparser.)*

4.  **Run the Application**:
    Start the Flask development server:
    ```bash
    python app.py
    ```

5.  **Access the Application**:
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

Once the application is running, you will see a list of live cricket scores. You can use the dropdown menus at the top to filter the displayed matches by:

*   **Match Type**: Select from options like 'T20', 'ODI', 'Test', 'Women's', 'Domestic', etc.
*   **Region**: Select from known team/region names like 'Hyderabad (India)', 'Punjab', 'Brisbane Heat Women', etc.

Select 'All' in either filter to view all matches.

## Project Structure

```
live_criket_match_gemini_01/
├── app.py                  # Main Flask application logic
├── requirements.txt        # List of project dependencies
├── templates/
│   └── scores.html         # HTML template for displaying scores
└── .git/
    └── ...                 # Git repository files (if applicable)
```
