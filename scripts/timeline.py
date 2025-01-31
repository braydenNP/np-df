import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define CSV file path
csv_path = "/home/kali/evidence/timeline/timeline.csv"

# Load CSV, skipping the incorrect header row
df = pd.read_csv(csv_path, skiprows=1, names=["Date", "Time", "Size", "MACB", "Permissions", "UID", "GID", "Metadata", "File"],
                 dtype=str, low_memory=False)

# Ensure Date & Time are strings and clean spaces
df["Date"] = df["Date"].astype(str).str.strip()
df["Time"] = df["Time"].astype(str).str.strip()

# Convert Date & Time to a proper Timestamp
df["Timestamp"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors='coerce')

# Drop invalid timestamps
df = df.dropna(subset=["Timestamp"])

# **Filter for only 2008 data**
df_2008 = df[(df["Timestamp"] >= "2008-01-01") & (df["Timestamp"] < "2009-01-01")]

# Debugging: Check filtered data
print("\nFirst 10 rows from 2008:\n", df_2008.head(10))
print("\nTotal events in 2008:", df_2008.shape[0])

# If no valid timestamps in 2008, exit
if df_2008.empty:
    print("\n❌ No valid timestamps found for 2008.")
    exit()

# Sort by Timestamp
df_2008 = df_2008.sort_values("Timestamp")

# Plot
plt.figure(figsize=(14, 6))
plt.plot(df_2008["Timestamp"], range(len(df_2008)), marker="o", markersize=4, linestyle="-", alpha=0.7, label="2008 File Events")

# Customize X-axis for better readability
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))  # Show Month-Day format
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Major ticks by month
plt.xticks(rotation=45)  # Rotate labels for readability

# Labels and title
plt.xlabel("Time (2008)", fontsize=12)
plt.ylabel("File Events", fontsize=12)
plt.title("Timeline of File System Events (2008)", fontsize=14)

# Enable grid for better visualization
plt.grid(True, linestyle="--", alpha=0.6)

# Show legend
plt.legend()

# Display the graph
plt.show()