import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Specify the path to the CSV file containing the timeline data.
csv_path = "/home/kali/evidence/timeline/timeline.csv"

# Load the CSV file into a DataFrame, explicitly naming columns and skipping the incorrect header.
df = pd.read_csv(csv_path, skiprows=1, names=["Date", "Time", "Size", "MACB", "Permissions", "UID", "GID", "Metadata", "File"],
                 dtype=str, low_memory=False)

# Clean leading and trailing spaces from the Date and Time columns.
df["Date"] = df["Date"].astype(str).str.strip()
df["Time"] = df["Time"].astype(str).str.strip()

# Combine the Date and Time columns into a single Timestamp column.
df["Timestamp"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors='coerce')

# Remove rows with invalid or missing Timestamps.
df = df.dropna(subset=["Timestamp"])

# Filter the data to include only events from the year 2008.
df_2008 = df[(df["Timestamp"] >= "2008-01-01") & (df["Timestamp"] < "2009-01-01")]

# Output the first 10 rows of the filtered data for debugging and verification.
print("\nFirst 10 rows from 2008:\n", df_2008.head(10))
print("\nTotal events in 2008:", df_2008.shape[0])

# Exit the script if no events were found for 2008.
if df_2008.empty:
    print("\n No valid timestamps found for 2008.")
    exit()

# Sort the 2008 DataFrame by Timestamp for chronological analysis.
df_2008 = df_2008.sort_values("Timestamp")

# Create a plot of the file events over time in 2008.
plt.figure(figsize=(14, 6))
plt.plot(df_2008["Timestamp"], range(len(df_2008)), marker="o", markersize=4, linestyle="-", alpha=0.7, label="2008 File Events")

# Format the X-axis to display dates as Month-Day and set major ticks to occur monthly.
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=45)  # Rotate the date labels for better readability.

# Add labels and a title to the plot.
plt.xlabel("Time (2008)", fontsize=12)
plt.ylabel("File Events", fontsize=12)
plt.title("Timeline of File System Events (2008)", fontsize=14)

# Enable a grid for easier visual analysis of the plot.
plt.grid(True, linestyle="--", alpha=0.6)

# Display a legend to clarify the plotted data.
plt.legend()

# Show the final plot.
plt.show()
