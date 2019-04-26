/**
 * FB2 book description
 * @export
 * @interface FB2Info
 */
export interface FB2Info {
    /**
     * Book annotation
     * @type {string}
     * @memberof FB2Info
     */
    annotation?: string;
    /**
     * Book name from <publish-info>
     * @type {string}
     * @memberof FB2Info
     */
    name?: string;
    /**
     * Publisher name from <publish-info>
     * @type {string}
     * @memberof FB2Info
     */
    publisher?: string;
    /**
     * City of publishing from <publish-info>
     * @type {string}
     * @memberof FB2Info
     */
    city?: string;
    /**
     * Year of publishing from <publish-info>
     * @type {number}
     * @memberof FB2Info
     */
    year?: string;
    /**
     * ISBN from <publish-info>
     * @type {string}
     * @memberof FB2Info
     */
    isbn?: string;
    /**
     * Book's cover image in base64 format
     * @type {string}
     * @memberof FB2Info
     */
    cover?: string;
    /**
     * Mime-type of cover image
     * @type {string}
     * @memberof FB2Info
     */
    coverType?: string;
}

export default FB2Info;