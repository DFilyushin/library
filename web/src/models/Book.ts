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
    keywords?: Array<string>;
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
    genres?: Array<Genre>;
    /**
     * 
     * @type {Array<Author>}
     * @memberof Book
     */
    authors: Array<Author>;
    /**
     * 
     * @type {string}
     * @memberof Book
     */
    added?: string;
}
