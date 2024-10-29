import marimo

__generated_with = "0.9.1"
app = marimo.App()


@app.cell
def __():
    import requests
    from bs4 import BeautifulSoup
    import csv
    return BeautifulSoup, csv, requests


@app.cell
def __(BeautifulSoup, csv, requests):
    # Base URL with placeholders for the page numbers
    base_url = "https://www.swr-vote.de/swr1bw-hitparade-2024?p="

    # File to save the data
    output_file = "swr_hitparade_2024.csv"

    # Function to scrape a single page
    def scrape_page(page_number, starting_rank):
        url = base_url + str(page_number)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all song entries on the page
        songs = soup.find_all('li', class_='relative flex flex-col gap-0 p-4 hover:bg-background-600 bg-white border-b-1 border-[#D6D6D6]')

        song_data = []
        current_rank = starting_rank

        for song in songs:
            # Extract artist
            artist = song.find('p', class_='text-meta')
            artist_text = artist.get_text(strip=True) if artist else 'Unknown Artist'

            # Extract title
            title = song.find('p', class_='text-header-m')
            title_text = title.get_text(strip=True) if title else 'Unknown Title'

            # Use the current order as the ranking
            song_data.append([current_rank, artist_text, title_text])
            current_rank += 1

        return song_data, current_rank

    # Main script to loop through all pages and save the data
    def scrape_all_pages():
        all_songs = []
        rank = 1  # Start ranking from 1

        for page in range(1, 108):  # Loop through all 106 pages
            print(f"Scraping page {page}...")
            songs, rank = scrape_page(page, rank)  # Pass the current rank and update it as we go
            all_songs.extend(songs)

        # Write the data to a CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Rank", "Artist", "Title"])
            writer.writerows(all_songs)

        print(f"Data successfully written to {output_file}")

    # Start scraping
    scrape_all_pages()
    return base_url, output_file, scrape_all_pages, scrape_page


if __name__ == "__main__":
    app.run()
