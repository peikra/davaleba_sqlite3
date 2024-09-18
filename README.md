# SQLite Book and Author Database

This project creates an SQLite database with two tables: `authors` and `books`. It populates these tables with randomly generated data using the `Faker` library.
After the data is generated, several queries are performed to retrieve information about the authors and books.

## Features

- Randomly generate 500 authors and 1000 books using the `Faker` library.
- Stores the authors in the `authors` table with details like:
  - First name
  - Last name
  - Date of birth
  - Place of birth
- Stores the books in the `books` table with details like:
  - Title
  - Category
  - Number of pages
  - Date of publication
  - Author ID (linked to `authors` table)
- Performs the following queries:
  - Find the book with the most pages.
  - Calculate the average number of pages in all books.
  - Find the youngest author based on their date of birth.
  - List all authors who do not have any books.
  - Find authors who have written more than 3 books.

## Prerequisites

- Python 3.x
- SQLite3
- Required libraries:
  - `Faker`
  - `random`

### Install Required Libraries

To install the required libraries, run:

```bash
pip install faker
