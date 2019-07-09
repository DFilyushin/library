import Genre from './Genre';
import Author from './Author';

/**
 *
 * @export
 * @interface Book
 */
export default interface Book {
    /**
     *
     * @type {string}
     * @memberof Book
     */
    id: string;
    /**
     *
     * @type {string}
     * @memberof Book
     */
    name: string;
    /**
     *
     * @type {Array<string>}
     * @memberof Book
     */
    keywords?: string[];
    /**
     *
     * @type {string}
     * @memberof Book
     */
    filename?: string;
    /**
     *
     * @type {string}
     * @memberof Book
     */
    deleted?: string;
    /**
     *
     * @type {string}
     * @memberof Book
     */
    lang?: string;
    /**
     *
     * @type {string}
     * @memberof Book
     */
    series?: string;
    /**
     *
     * @type {string}
     * @memberof Book
     */
    sernum?: string;
    /**
     *
     * @type {Array<Genre>}
     * @memberof Book
     */
    genres?: Genre[];
    /**
     *
     * @type {Array<Author>}
     * @memberof Book
     */
    authors: Author[];
    /**
     *
     * @type {string}
     * @memberof Book
     */
    added?: string;

    cover: string;

    city: string;

    publisher: string;

    year: number;

    isbn: string;

    width: number;

    height: number;
}
