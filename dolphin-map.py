import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Load the Excel file
dolphin_data = pd.read_excel("dolphin_sightings.xlsx")

# Ensure the Excel file contains the necessary columns: 'DolphinID', 'Latitude', 'Longitude', 'Date'

# Filter data for a specific dolphin
def plot_dolphin_sightings(dolphin_id):
    filtered_data = dolphin_data[dolphin_data['DolphinID'] == dolphin_id]

    if filtered_data.empty:
        print(f"No sightings found for Dolphin ID: {dolphin_id}")
        return

    # Convert 'Date' column to datetime
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])

    # Sort by date
    filtered_data = filtered_data.sort_values('Date')

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(
        filtered_data,
        geometry=[Point(xy) for xy in zip(filtered_data['Longitude'], filtered_data['Latitude'])],
        crs="EPSG:4326"
    )
     # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    gdf.plot(
        ax=ax,
        column='Date',  # Use the 'Date' column to color points
        cmap='viridis',
        legend=True,
        legend_kwds={'label': "Older to Newer Dates"}
    )

    # Add a basemap (optional, requires contextily package)
    try:
        import contextily as ctx
        ctx.add_basemap(ax, crs=gdf.crs.to_string())
    except ImportError:
        print("contextily not installed; skipping basemap.")

    ax.set_title(f"Sightings of Dolphin ID: {dolphin_id}")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.show()

# Example usage: specify a DolphinID
plot_dolphin_sightings(dolphin_id="D123")
