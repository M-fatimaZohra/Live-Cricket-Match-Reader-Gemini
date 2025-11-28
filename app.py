from flask import Flask, render_template, request
import feedparser
import re # Import regular expression module
import os # Import os module

app = Flask(__name__)

RSS_FEED_URL = "https://static.cricinfo.com/rss/livescores.xml"

# Function to extract potential match types from title
def extract_match_types(title):
    title_lower = title.lower()
    match_types = []
    # Basic patterns for common cricket formats
    if 't20' in title_lower or 'twenty20' in title_lower:
        match_types.append('T20')
    if 'odi' in title_lower or 'one day international' in title_lower:
        match_types.append('ODI')
    if 'test' in title_lower:
        match_types.append('Test')
    if 'womens' in title_lower or 'women' in title_lower:
        match_types.append('Women')
    if 'ipl' in title_lower: # Example: Indian Premier League
        match_types.append('IPL')
    if 'bbl' in title_lower: # Example: Big Bash League
        match_types.append('BBL')
    if 'npl' in title_lower: # Example: Nepal Premier League from current feed items
        match_types.append('NPL')
    # Add more patterns as needed for other formats/leagues
    
    # If no specific types found, attempt to infer from team names or general context
    # This part is less reliable for match types than for regions
    if not match_types:
        # Simple check for domestic-sounding teams based on common knowledge
        domestic_keywords = [
            'hyderabad', 'maharashtra', 'kerala', 'railways', 'haryana', 'punjab', 'rajasthan', 'tripura',
            'andhra', 'odisha', 'bihar', 'madhya pradesh', 'baroda', 'puducherry', 'delhi', 'tamil nadu',
            'manipur', 'meghalaya', 'mizoram', 'sikkim', 'jammu & kashmir', 'uttar pradesh', 'himachal pradesh',
            'services', 'saurashtra', 'uttarakhand', 'assam', 'chhattisgarh', 'chandigarh', 'goa', 'bengal',
            'gujarat', 'jharkhand', 'karnataka', 'arunachal pradesh', 'nagaland'
        ]
        if any(keyword in title_lower for keyword in domestic_keywords):
            match_types.append('Domestic')
        else:
            match_types.append('Other')
        
    return list(set(match_types)) # Return unique types

# Predefined list of regions/teams to filter by, based on common cricket knowledge and feed content.
# This list can be expanded for more comprehensive filtering.
KNOWN_REGIONS = [
    "Hyderabad (India)", "Maharashtra", "Kerala", "Railways", "Haryana", "Punjab", "Rajasthan", "Tripura",
    "Andhra", "Odisha", "Bihar", "Madhya Pradesh", "Baroda", "Puducherry", "Delhi", "Tamil Nadu",
    "Manipur", "Meghalaya", "Mizoram", "Sikkim", "Jammu & Kashmir", "Uttar Pradesh", "Himachal Pradesh",
    "Services", "Saurashtra", "Uttarakhand", "Assam", "Chhattisgarh", "Chandigarh", "Goa", "Bengal",
    "Gujarat", "Jharkhand", "Karnataka", "Arunachal Pradesh", "Nagaland",
    "Brisbane Heat Women", "Sydney Sixers Women", # WBBL
    "Kathmandu Gorkhas", "Chitwan Rhinos", # NPL related
    "Ajman Titans", "UAE Bulls", # UAE related
    "Matabeleland Tuskers", "Mid West Rhinos", "Mashonaland Eagles", "Mountaineers", # Zimbabwe related
    "Biratnagar Kings", "Karnali Yaks", # NPL related
    "Quetta Qavalry", "Royal Champs", "Vista Riders", "Deccan Gladiators" # Other leagues
]

# Function to extract potential regions/teams from title
def extract_regions_from_title(title):
    regions_found = set()
    title_lower = title.lower()
    for region in KNOWN_REGIONS:
        # Check if the region name (case-insensitive) is present in the title.
        # This is a simple string containment check. More complex parsing might be needed for ambiguous titles.
        if region.lower() in title_lower:
            regions_found.add(region) # Use the original casing from KNOWN_REGIONS for display
    return list(regions_found)


@app.route('/')
def index():
    # Fetch and parse the RSS feed
    feed = feedparser.parse(RSS_FEED_URL)
    
    # Extract relevant information (e.g., entries which are the matches)
    all_matches = feed.entries
    
    # --- Match Type Filtering --- 
    all_match_types = set()
    for match in all_matches:
        extracted_types = extract_match_types(match.title)
        all_match_types.update(extracted_types)
    
    # Sort match types alphabetically, with 'All' first
    sorted_match_types = sorted(list(all_match_types))
    display_match_type_options = ['All'] + sorted_match_types

    # Get the selected match type from query parameters, default to 'All'
    selected_match_type = request.args.get('match_type', 'All')
    
    # Filter matches by match type if a specific type is selected
    matches_filtered_by_type = []
    if selected_match_type == 'All':
        matches_filtered_by_type = all_matches
    else:
        for match in all_matches:
            match_types_in_title = extract_match_types(match.title)
            if selected_match_type in match_types_in_title:
                matches_filtered_by_type.append(match)

    # --- Region Filtering ---
    all_regions = set()
    for match in matches_filtered_by_type: # Filter regions based on already type-filtered matches
        extracted_regions = extract_regions_from_title(match.title)
        all_regions.update(extracted_regions)
    
    # Sort regions alphabetically, with 'All' first
    sorted_regions = sorted(list(all_regions))
    display_region_options = ['All'] + sorted_regions

    # Get the selected region from query parameters, default to 'All'
    selected_region = request.args.get('region', 'All')
    
    # Filter matches by region if a specific region is selected
    final_matches = []
    if selected_region == 'All':
        final_matches = matches_filtered_by_type
    else:
        for match in matches_filtered_by_type:
            if selected_region in extract_regions_from_title(match.title):
                final_matches.append(match)

    # Render the HTML template with the match data and filter options
    return render_template(
        'scores.html',
        matches=final_matches,
        match_types=display_match_type_options,
        selected_match_type=selected_match_type,
        regions=display_region_options,
        selected_region=selected_region
    )

if __name__ == '__main__':
    # Ensure the templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(debug=True)
