/**
 * Genre of a book
 * @export
 * @interface Genre
 */
interface Genre {
    /**
     * Internal genre identifier
     * @type {string}
     * @memberof Genre
     */
    id?: string;
    /**
     * fb2 genre code
     * @type {string}
     * @memberof Genre
     */
    slug?: string;
    /**
     * Genre name in Russian
     * @type {string}
     * @memberof Genre
     */
    name?: string;
    /**
     * Genre name in English
     * @type {string}
     * @memberof Genre
     */
    nameEn?: string;
}

export default Genre;