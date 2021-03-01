class Endpoints {
    static API_URL: string = 'https://books.toadstool.su/api/v1';

    /**
     * Get all genres
     */
    static getGenres() {
        return `${Endpoints.API_URL}/genres/`;
    }

    /**
     * Find books by genres
     */
    static getGenresBooks(genre: string) {
        return `${Endpoints.API_URL}/books/by_genre/${genre}`;
    }

    /**
     * Get list of books by author id
     */
    static getAuthorsBooks(author: string) {
        return `${Endpoints.API_URL}/books/by_author/${author}`;
    }

    /**
     * Get authors list from first letters of last name
     */
    static getAuthorsStartWith(text: string, limit: number, skip: number) {
        return `${Endpoints.API_URL}/authors/start_with/${text}?limit=${limit}&skip=${skip}`;
    }

    /**
     * Get book by ID
     */
    static getBooksById(bookId: string) {
        return `${Endpoints.API_URL}/books/${bookId}`;
    }

    /**
     * Find books by piece of name. Using regexp, case-insensitive search
     */
    static getBooksByName(text: string, limit: number, skip: number) {
        return `${Endpoints.API_URL}/books/by_name/${text}?limit=${limit}&skip=${skip}`;
    }

    /**
     * Download book content
     */
    static getBooksContent(bookId: string, bookType: string) {
        return `${Endpoints.API_URL}/books/${bookId}/content?type=${bookType}`;
    }

}

export default Endpoints;
