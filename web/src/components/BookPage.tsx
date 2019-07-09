import React, { Component } from 'react';

import Endpoints from '../utils/Endpoints';
import Book from '../models/Book';
import BookCard from './BookCard';
import { Container } from '@material-ui/core';

interface State {
    book?: Book;
}

class BookPage extends Component<any, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            book: undefined
        };
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
            });
    }

    render() {
        const { book } = this.state;
        if (!book) {
            return null;
        }
        return (
            <Container maxWidth="sm">
                <BookCard book={book} preview={false} />
            </Container>
        );
    }
}

export default BookPage;
