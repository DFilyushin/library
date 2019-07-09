export default class Consts {
    static PUBLIC_URL: string = '';

    static getCoverImage(id: string): string {
        return `${Consts.PUBLIC_URL}/cover/${id}.jpg`;
    }
}