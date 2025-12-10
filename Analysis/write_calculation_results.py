def write_results(results, filename="results.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Artist Calculations Summary\n")
        f.write("Format: artist name, listeners, number of concerts, number of unique venues\n")
            
        for row in results:
            f.write(str(row) + "\n")
            
    print(f"Results successfully written to {filename}")


# need to actually call the function, probably in main file? 