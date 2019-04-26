class Endpoints {
    private static API_URL: string = 'http://books.toadstool.online/api/v1';

    /**
     * Get all genres
     */
    public static getGenres() {
        return `${Endpoints.API_URL}/genres`;
    }

    /**
     * Find books by genres
     */
    public static getGenresBooks(genre: string) {
        return `${Endpoints.API_URL}/books/by_genre/${genre}`;
    }

    /**
     * Get list of books by author id
     */
    public static getAuthorsBooks(author: string) {
        return `${Endpoints.API_URL}/books/by_author/${author}`;
    }

    /**
     * Get authors list from first letters of last name
     */
    public static getAuthorsStartWith(text: string, limit: number, skip: number) {
        return `${Endpoints.API_URL}/authors/start_with/${text}?limit=${limit}&skip=${skip}`;
    }

    /**
     * Get book by ID
     */
    public static getBooksById(bookId: string) {
        return `${Endpoints.API_URL}/books/${bookId}`;
    }

    /**
     * Find books by piece of name. Using regexp, case-insensitive search
     */
    public static getBooksByName(text: string, limit: number, skip: number) {
        return `${Endpoints.API_URL}/books/by_name/${text}?limit=${limit}&skip=${skip}`;
    }

    /**
     * Download book content
     */
    public static getBooksContent(bookId: string) {
        return `${Endpoints.API_URL}/books/${bookId}/content`;
    }

    /**
     * Get book FB2 description and cover image
     */
    public static getBooksFB2Info(bookId: string) {
        return `${Endpoints.API_URL}/books/${bookId}/fb2info`;
    }
}

export default Endpoints;