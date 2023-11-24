import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import itertools

# Function to be called when the mouse moves
def on_move(event):
    for line, annotation in zip(lines, annotations):
        if line.contains(event)[0]:
            annotation.set_visible(True)
            annotation.xy = (event.xdata, event.ydata)
        else:
            annotation.set_visible(False)
    plt.draw()

# Path to the directory containing Excel files
folder_path = "data/hunter/excel"  # Change this to your folder path
excel_files = glob.glob(f"{folder_path}/*.xlsx")

# Initialize a list to store data
all_data = []
plot_data = []  # List to store plot data for saving to a new Excel file
annotations = []  # List to store annotations

# Define line styles and colors for differentiation
line_styles = ['-', ':', '-.', 'dashed']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

# Create cycle iterators for styles and colors
style_cycler = itertools.cycle(line_styles)
color_cycler = itertools.cycle(colors)

# Increase the figure size for better visibility
fig, ax = plt.subplots(figsize=(16, 8))

lines = []  # Store the line objects

# Read each Excel file and store the data
for file in excel_files:
    df = pd.read_excel(file, header=None, names=["Time (BC)", "Probability"])
    all_data.append(df)

    # Extracting file name without extension for use as a label
    file_name = os.path.splitext(os.path.basename(file))[0]

    # Get the next style and color
    line_style = next(style_cycler)
    color = next(color_cycler)

    # Plot without markers and with thinner lines
    line, = ax.plot(df["Time (BC)"], df["Probability"], label=file_name, linestyle=line_style, color=color, linewidth=1)
    lines.append(line)

    # Create an annotation for each line
    annotation = ax.annotate(file_name, xy=(0,0), xytext=(20,20), textcoords="offset points",
                             bbox=dict(boxstyle="round", fc="w"),
                             arrowprops=dict(arrowstyle="->"))
    annotation.set_visible(False)
    annotations.append(annotation)

    # Adding data to plot_data list
    plot_data.append(df.assign(File_Name=file_name))

plt.xlabel('Time (BC)')
plt.ylabel('Probability')
plt.title('Probability vs. Time (BC)')

# Adjust the legend
plt.legend(loc='upper right', ncol=3, fontsize='small', title='File Names')

# Connect the event to the function
fig.canvas.mpl_connect('motion_notify_event', on_move)

# Save plot as an image
plt.savefig('data/hunter/' + '/plot_image.png')

plt.show()
