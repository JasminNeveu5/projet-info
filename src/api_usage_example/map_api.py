# Required imports for the implementation
import folium
from folium.plugins import MarkerCluster
import requests
import pandas as pd
from options.config import DATA_DIR

# Load circuit data from file
circuits = pd.read_csv(
    f"{DATA_DIR}/circuits.csv"
)  # Assuming circuits file contains latitude, longitude, and name fields

# Define base URL for the API
API_BASE_URL = "http://localhost:8000"

def generate_best_times_map():
    """
    Generate an interactive map showing the best lap time for each circuit.
    """
    # Initialize the map centered on the average coordinates
    m = folium.Map(
        location=[circuits["lat"].mean(), circuits["lng"].mean()], 
        zoom_start=2
    )
    
    # Create a marker cluster for better visualization
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers for each circuit
    for index, row in circuits.iterrows():
        # Extract information from the row
        circuit_name = row.get("name", "Unknown Circuit")
        lat, lng = row["lat"], row["lng"]
        
        try:
            # Make API request to get best time for this circuit
            encoded_name = requests.utils.quote(circuit_name)
            response = requests.get(
                f"{API_BASE_URL}/meilleur_temps_circuit_{encoded_name}"
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Create popup content with the circuit info and best time
                popup_content = (
                    f"<strong>Circuit:</strong> {data.get('name', circuit_name)}<br>"
                    f"<strong>Location:</strong> {data.get('location', 'N/A')}<br>"
                    f"<strong>Country:</strong> {data.get('country', 'N/A')}<br>"
                    f"<strong>Best Time:</strong> {data.get('best_time', 'N/A')}<br>"
                )
                
                # Add marker with the popup
                folium.Marker(
                    location=[lat, lng],
                    popup=folium.Popup(popup_content, max_width=300),
                    tooltip=circuit_name,
                ).add_to(marker_cluster)
            else:
                # If API request fails, add marker with error message
                error_message = f"Error {response.status_code}: Could not retrieve data"
                folium.Marker(
                    location=[lat, lng],
                    popup=folium.Popup(error_message, max_width=300),
                    tooltip=circuit_name,
                    icon=folium.Icon(color="red"),
                ).add_to(marker_cluster)
                
        except Exception as e:
            # Handle exceptions
            error_message = f"Error occurred: {str(e)}"
            folium.Marker(
                location=[lat, lng],
                popup=folium.Popup(error_message, max_width=300),
                tooltip=circuit_name,
                icon=folium.Icon(color="red"),
            ).add_to(marker_cluster)
    
    return m

# Generate the map
best_times_map = generate_best_times_map()

# Save the map to an HTML file
best_times_map.save("best_lap_times_map.html")
