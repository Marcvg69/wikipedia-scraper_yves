# src/main.py

import time
from src.leaders_scraper import WikipediaScraper
from utils.print_utils import PrintUtils, BgColor, Color


def run_scraper(use_multithreading=False):
    """
    Run the Wikipedia scraping pipeline with optional multithreading.

    Parameters:
    - use_multithreading (bool): If True, fetch leaders using multithreading.
    """
    bg_color = BgColor.BLUE if use_multithreading else BgColor.GREEN
    PrintUtils.print_bg_color(f"Run scraper (multithreading={use_multithreading})", bg_color)
         
    
    scraper = WikipediaScraper()
    start_time = time.time()

    # limit_per_country ===========================================================================
    scraper.fetch_leaders(limit_per_country=2, verbose=True, use_multithreading=use_multithreading)
    # limit_per_country ===========================================================================

    scraper.to_json_file("leaders_data.json")

    duration = time.time() - start_time
    PrintUtils.print_bg_color(f"Execution time (multithreading={use_multithreading}): {duration:.2f} seconds",bg_color)
    print("\n")
    
    return duration

# Main function that runs the scraping pipeline
def main():

    # Run with multithreading enabled
    use_multithreading = True
    exec_time_thread_true = run_scraper(use_multithreading=use_multithreading)

    # Run with multithreading disabled
    use_multithreading = False
    exec_time_thread_false = run_scraper(use_multithreading=use_multithreading)

    # Display comparison
    PrintUtils.print_color("\nExecution Time Comparison:", Color.CYAN)
    PrintUtils.print_bg_color(f"- With multithreading:    {exec_time_thread_true:.2f} seconds", BgColor.BLUE)
    PrintUtils.print_bg_color(f"- Without multithreading: {exec_time_thread_false:.2f} seconds", BgColor.GREEN)

    # Optional: compute and print the speed gain
    if exec_time_thread_false > exec_time_thread_true:
        gain = exec_time_thread_false / exec_time_thread_true
        PrintUtils.print_color(f"\nMultithreading was ~{gain:.2f}x faster\n", Color.MAGENTA)
    else:
        PrintUtils.print_color(
        "\nMultithreading was slower — the API might be blocking concurrent requests.\n"
        "Sequential execution may be more efficient when servers limit parallel access.",
        Color.MAGENTA
    )


# Entry point of the script when executed directly (e.g., python main.py)
if __name__ == "__main__":
    main()
