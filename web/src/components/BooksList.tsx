import React, { Component } from 'react';
import Book from '../models/Book';
import { Redirect } from 'react-router';
import BookCard from './BookCard';
import Endpoints from '../Endpoints';

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
                const sorted = data.sort((a, b) => this.compareBySequenceAndName(a, b));
                this.setState({
                    books: sorted
                });
            })
            .catch(e => {
                console.log(e);
            })
    }

    private compareBySequenceAndName(a: Book, b: Book): number {
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
    }

    private booksUrl(by: string, id: string): string | undefined {
        switch(by.toLowerCase())
        {
            case 'genres':
                return Endpoints.getGenresBooks(id);
            case 'authors':
                return Endpoints.getAuthorsBooks(id);
            default:
                return undefined;
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

        if (books.length === 1) {
            return <Redirect to={`/books/${books[0].id}`} />;
        }

        if (downloadBookId) {
            return <Redirect to={Endpoints.getBooksContent(downloadBookId)} />;
        }

        return (
            <React.Fragment>
            {
                books.map(book => <BookCard book={book} preview={true} key={book.id} />)
            }
            </React.Fragment>
        );
    }
}

export default BooksList;