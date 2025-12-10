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
    plt.show()

        

def create_barchart(calculation_results):
    pass 

