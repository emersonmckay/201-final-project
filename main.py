# Charlotte 

from Data_Collection.listener_data import listener_data
from Data_Collection.ticketmaster_data import ticket_data
from Database.create_database import create_database
from Analysis.calculations import calculations
from Analysis.write_calculation_results import write_results
from Visualizations.visualizations import create_bar_chart, create_scatter_plot 


def main():
    print("Starting Ticket Trend Tracking...\n")

    # Load API keys
    lastfm_key = "e7daacfe434e52e4cfd7c8f6b1004d29"
    ticketmaster_key = "lfCVtbiZSWpr7HmZUUGWa8C1chUvuvpU"

    # Create database / store data
    print("Creating database...")
    create_database()

    # Gather data from APIs
    print("Gathering listener data from Last.fm...")
    listener_data(lastfm_key)

    print("Gathering ticket data from Ticketmaster...")
    ticket_data(ticketmaster_key) 

    # Run calculations 
    print("Running calculations...")
    calculation_results = calculations("ticket_trends.sqlite")

    # Save results to text file 
    print("Saving calculation results...")
    write_results(calculation_results)

    # Filtered results
    filtered_results = [
        row for row in calculation_results
        if row[1] is not None and row[1] != 0
    ]

    # Convert results to list of tuples for scatter plot
    scatter_plot_data = [
        (row[0], row[1], row[2])
        for row in filtered_results
    ]

    # Convert results to dict for bar chart
    bar_chart_data = {
        row[0]: {"listeners": row[1], "events": row[2]}
        for row in filtered_results
    }

    # Create visualizations 
    print("Creating bar chart...")
    create_bar_chart(bar_chart_data)

    print("Creating scatter plot...")
    create_scatter_plot(scatter_plot_data)

    print("\nTicket Trend Tracking Complete!")


if __name__ == "__main__":
    main()