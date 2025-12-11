import matplotlib.pyplot as plt

# Emerson -- Scatterplot
def create_scatter_plot(calculation_results):
    artists = [row[0] for row in calculation_results]
    listeners = [row[1] for row in calculation_results]
    num_concerts = [row[2] for row in calculation_results]

    plt.figure(figsize = (10, 6))
    plt.scatter(listeners, num_concerts)

    # label points with artist name
    for i, artist in enumerate(artists):
        plt.text(listeners[i] + 0.05, num_concerts[i] + 0.05, artist, fontsize=8)

    plt.title("Listeners vs Number of Concerts")
    plt.xlabel("Listeners (Last.fm)")
    plt.ylabel("Number of Concerts (Ticketmaster)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("scatter_plot.png")
    print("Scatter plot saved as scatter_plot.png")

    plt.show()

        
# Charlotte -- Barchart 
def create_bar_chart(calculation_results):
    artists = list(calculation_results.keys())
    listeners = [calculation_results[a]["listeners"] for a in artists]
    events = [calculation_results[a]["events"] for a in artists]

    x = range(len(artists))
    bar_width = 0.4

    fig, ax1 = plt.subplots(figsize=(18,8))

    # First axis for listeners
    ax1.bar([p - bar_width/2 for p in x], listeners, 
            width=bar_width, label="Listeners", color="steelblue")

    ax1.set_ylabel("Listeners", color="steelblue")
    ax1.tick_params(axis='y', labelcolor="steelblue")

    # Second axis for number of events
    ax2 = ax1.twinx()
    ax2.bar([p + bar_width/2 for p in x], events, 
            width=bar_width, label="Number of Events", color="darkorange")

    ax2.set_ylabel("Number of Events", color="darkorange")
    ax2.tick_params(axis='y', labelcolor="darkorange")
    
    # Titles and labels
    plt.title("Comparison of Artist Listener Count and Event Count")
    plt.xticks(x, artists, rotation=45, ha="right")

    plt.tight_layout
    plt.savefig("bar_chart.png")
    print("Bar chart saved as bar_chart.png")

    plt.show()




