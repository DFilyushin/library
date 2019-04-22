/**
 * Genre of a book
 * @export
 * @interface Genre
 */
export interface Genre {
    /**
     * FB2 genre code
     * @type {string}
     * @memberof Genre
     */
    id: string;
    /**
     * 
     * @type {GenreTitles}
     * @memberof Genre
     */
    titles: GenreTitles;
    /**
     * 
     * @type {GenreDetailed}
     * @memberof Genre
     */
    detailed: GenreDetailed;
    /**
     * Sub-genres
     * @type {Array<SubGenre>}
     * @memberof Genre
     */
    subGenres?: Array<SubGenre>;
}

/**
 * Genre description
 * @export
 * @interface GenreDetailed
 */
export interface GenreDetailed {
    /**
     * 
     * @type {string}
     * @memberof GenreDetailed
     */
    en: string;
    /**
     * 
     * @type {string}
     * @memberof GenreDetailed
     */
    ru: string;
}

/**
 * Genre title
 * @export
 * @interface GenreTitles
 */
export interface GenreTitles {
    /**
     * 
     * @type {string}
     * @memberof GenreTitles
     */
    en: string;
    /**
     * 
     * @type {string}
     * @memberof GenreTitles
     */
    ru: string;
}

/**
 * Sub-genre of a book
 * @export
 * @interface SubGenre
 */
export interface SubGenre {
    /**
     * FB2 genre code
     * @type {string}
     * @memberof SubGenre
     */
    id: string;
    /**
     * 
     * @type {SubGenreTitles}
     * @memberof SubGenre
     */
    titles: SubGenreTitles;
}

/**
 * Sub-genre title
 * @export
 * @interface SubGenreTitles
 */
export interface SubGenreTitles {
    /**
     * 
     * @type {string}
     * @memberof SubGenreTitles
     */
    en: string;
    /**
     * 
     * @type {string}
     * @memberof SubGenreTitles
     */
    ru: string;
}

export default Genre;