/**
 * Author of a book
 * @export
 * @interface Author
 */
export default interface Author {
    /**
     * Internal author identifier
     * @type {string}
     * @memberof Author
     */
    id: string;
    /**
     * Internal author identifier
     * @type {string}
     * @memberof Author
     */
    _id: string;
    /**
     * Author's last name
     * @type {string}
     * @memberof Author
     */
    last_name?: string;
    /**
     * Author's first name
     * @type {string}
     * @memberof Author
     */
    first_name?: string;
    /**
     * Author's middle name
     * @type {string}
     * @memberof Author
     */
    middle_name?: string;
}
