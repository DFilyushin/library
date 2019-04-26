import React, { Component } from 'react';
import Book from '../models/Book';
import { Redirect } from 'react-router';
import BookCard from './BookCard';
import Endpoints from '../Endpoints';

interface State
{
    book?: Book;
}

class BookPage extends Component<any, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            book: undefined
        }
    }

    componentDidMount() {
        const id = this.props.history.location.pathname.split('/')[2];

        fetch(Endpoints.getBooksById(id))
            .then(results => {
                return results.json();
            })
            .then((data: Book) => {
                this.setState({
                    book: data
                });
            })
            .catch(e => {
                console.log(e);
            })
    }

    render() {
        const { book } = this.state;
        if (!book) {
            return null;
        }
        return <BookCard book={book} preview={false}/>;
    }
}

export default BookPage;