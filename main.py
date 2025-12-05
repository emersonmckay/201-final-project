# Charlotte 

def main():
    print("Starting Ticket Trend Tracking...\n")

    # Load API keys
    lastfm_key = input()
    ticketmaster_key = input()

    # Gather data from APIs
    print("Gathering listener data from Last.fm...")
    listener_dict = listener_data(lastfm_key)

    print("Gathering ticket data from Ticketmaster...")
    ticket_dict = ticket_data(ticketmaster_key) 

    # Create database / store data
    print("Creating database...")
    db_name = "ticket_trends.sqlite"
    create_database(db_name)

    # Run calculations 
    print("Running calculations...")
    calculation_results = calculations(db_name)

    # Save results to text file 
    print("Saving calculation results...")
    final_calculation_results(calculation_results)

    # Create visualizations 
    print("Creating bar chart...")
    create_bar_chart(calculation_results)

    print("Creating scatter plot...")
    create_scatter_plot(calculation_results)

    print("\nTicket Trend Tracking Complete!")