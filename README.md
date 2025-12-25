# Pokémon Card Inventory & Deck Manager

## Overview
This project is a Python-based command-line application designed to manage a personal Pokémon Trading Card Game (TCG) collection and validate deck lists against owned inventory. It allows users to store cards persistently, organize them into multiple storage containers, import full deck lists, and determine whether a deck can be built with available cards.

The system emphasizes structured data handling, validation logic, and modular design, making it suitable as a portfolio project demonstrating practical Python skills.

---

## Features

- **Persistent Inventory Storage**  
  Stores card data in a JSON file located in the user’s home directory, ensuring inventory persists across sessions.

- **Multi-Storage Support**  
  Create and manage multiple named storage containers (e.g., Main Storage, Deck Lists, custom collections).

- **Card Management (CRUD)**  
  - Add cards with automatic quantity tracking
  - Increment or decrement card counts
  - Delete individual cards, entire storage containers, or the full inventory file

- **Advanced Search & Browsing**  
  - View full storage contents
  - Search by card name
  - Filter by card set

- **Deck List Parsing**  
  Converts formatted deck lists into structured data categorized by Pokémon, Trainer, and Energy cards.

- **Deck Validation Engine**  
  Checks whether a deck can be built using available inventory:
  - Identifies missing cards
  - Detects insufficient quantities
  - Suggests alternative card versions from other owned sets

- **Deck Importing**  
  Add all cards from a deck list directly into storage with quantity aggregation.

- **Card Image Fetching**  
  Dynamically retrieves and displays high-resolution card images using HTTP requests and image processing libraries.

---

## Technologies Used

- **Python 3**
- **Standard Library**: `json`, `os`, `pathlib`, `io`
- **Third-Party Libraries**:
  - `requests` – HTTP requests for card images
  - `Pillow (PIL)` – Image processing and display

---

## Data Model

Cards are stored as dictionaries with the following structure:

```
{
  "CardName": "Gholdengo ex",
  "CardSet": "PAR",
  "CardNumber": 139,
  "Amount": 4
}
```

Storage is maintained as a dictionary of named collections:

```
{
  "Main Storage": [ ... ],
  "Deck Lists": [ ... ],
  "Custom Storage": [ ... ]
}
```

---

## How It Works

1. **Startup**  
   The application loads existing inventory from a JSON file or initializes a new one if none exists.

2. **User Navigation**  
   A menu-driven interface allows users to select storage containers and perform actions such as adding cards, browsing inventory, or validating decks.

3. **Deck Validation**  
   Deck lists are parsed line-by-line and compared against inventory using dictionary-based lookups for efficiency.

4. **Image Retrieval**  
   Card metadata is mapped to an external asset repository, where images are fetched and displayed locally.

---

## Example Use Cases

- Track a growing Pokémon TCG collection across multiple sets
- Verify whether a competitive deck can be built before purchasing cards
- Identify missing or insufficient cards and owned alternatives
- Maintain clean, structured inventory data for future expansion

---

## Setup & Usage

1. Install dependencies:

```
pip install requests pillow
```

2. Run the application:

```
python main.py
```

3. Follow the interactive prompts to manage storage, input cards, or validate deck lists.

---

## Future Enhancements

- Refactor deck lists into named, nested structures
- Export deck and inventory reports
- GUI or web-based interface
- Improved error handling and automated testing

---

## License

This project is for educational and portfolio purposes. External card images and data are sourced from public Pokémon TCG asset repositories and remain the property of their respective owners.

