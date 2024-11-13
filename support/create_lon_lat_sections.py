from pathlib import Path

# Define the bounds
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180
MIN_LATITUDE = -90
MAX_LATITUDE = 90

# Define the number of sections (50 in this case)
sections = 50

# Calculate the step sizes for longitude and latitude
longitude_step = (MAX_LONGITUDE - MIN_LONGITUDE) / sections
latitude_step = (MAX_LATITUDE - MIN_LATITUDE) / sections

# Open a file to write the coordinates
files_path = Path(__file__).parent / "files"
with open(f"{files_path}/map_sections.txt", "w") as file:
    for i in range(sections):
        # Calculate the longitude range for each section
        lon_min = MIN_LONGITUDE + i * longitude_step
        lon_max = lon_min + longitude_step

        # For simplicity, we’re keeping the latitude range constant
        lat_min = MIN_LATITUDE
        lat_max = MAX_LATITUDE

        # Write to file in the format: MIN_LONGITUDE, MIN_LATITUDE, MAX_LONGITUDE, MAX_LATITUDE
        file.write(f"{lon_min},{lat_min},{lon_max},{lat_max}\n")
