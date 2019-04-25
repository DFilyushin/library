import React, { Component } from 'react';
import Book from '../models/Book';
import { Redirect } from 'react-router';
import BookCard from './BookCard';

interface State
{
    loading: boolean;
    books: Book[];
    downloadBookId: string;
}

class BooksList extends Component<any, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            loading: false,
            books: [],
            downloadBookId: ''
        };
    }

    componentDidMount() {
        const by = this.props.history.location.pathname.split('/')[1];
        const id = this.props.history.location.pathname.split('/')[2];

        const url = this.booksUrl(by, id);
        if (!url) {
            return;
        }

        fetch(url)
            .then(results => {
                return results.json();
            })
            .then((data: Array<Book>) => {
                const sorted = data.sort((a, b) => {
                    if (a.series && !b.series) {
                        return -1;
                    }
                    if (!a.series && b.series) {
                        return 1;
                    }
                    if (a.series && b.series) {
                        if (a.series < b.series) {
                            return -1;
                        }
                        if (a.series > b.series) {
                            return 1;
                        }
                        if (a.sernum && b.sernum) {
                            return Number(a.sernum) - Number(b.sernum);
                        }
                    }
                    if (a.name < b.name) {
                        return -1;
                    }
                    if (a.name > b.name) {
                        return 1;
                    }
                    return 0;
                });
                this.setState({
                    books: sorted
                });
            })
            .catch(e => {
                console.log(e);
            })
    }

    booksUrl(by: string, id: string) {
        switch(by.toLowerCase())
        {
            case 'genres':
                return 'http://books.toadstool.online/api/v1/books/by_genre/' + id;
            case 'authors':
                return 'http://books.toadstool.online/api/v1/books/by_author/' + id;
            default:
                return null;
        }
    }

    handleDownloadClick(event: any, book: Book) {
        this.setState({ downloadBookId: book.id });
    }

    render() {
        const { classes } = this.props;
        const { books, downloadBookId } = this.state;

        if (books.length === 0) {
            return null;
        }

        if (downloadBookId) {
            return <Redirect to={'http://books.toadstool.online/api/v1/books/' + downloadBookId + '/content'} />;
        }

        return (
            <React.Fragment>
            {
                books.map(book => <BookCard book={book} />)
            }
            </React.Fragment>
        );
    }
}

export default BooksList;