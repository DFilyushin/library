import React, {Component} from 'react';

import {Container, Grid, Theme, withStyles} from '@material-ui/core';
import CircularProgress from '@material-ui/core/CircularProgress';

import Book from '../models/Book';
import Endpoints from '../utils/Endpoints';
import BookCard from './BookCard';
import FindLine from './FindLine';

interface State {
    searchText: string;
    books: Book[];
    loaded: boolean;
}

const styles = (theme: Theme) => ({
    root: {
    },
});

class Books extends Component<any, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            searchText: '',
            books: [],
            loaded: false
        };
    }

    componentDidMount() {
        document.addEventListener('keydown', this.escFunction, false);
    }

    componentWillUnmount() {
        document.removeEventListener('keydown', this.escFunction, false);
    }

    escFunction = (event: any) => {
        if (event.keyCode === 27) {
            this.setState({
                searchText: '',
                books: []
            });
        }
    }

    searchBook = async (findString: string) => {
        this.setState({loaded: true});
        fetch(Endpoints.getBooksByName(findString, 15, 0))
            .then(results => {
                return results.json();
            })
            .then((data: Book[]) => {
                this.setState({
                    books: data,
                    loaded: false
                });
            })
            .catch(() => {
                this.setState({books: []});
                this.setState({loaded: false});
            });
    }

    handleSearchBook = (event: any) => {
        if (this.state.searchText) {
            this.searchBook(this.state.searchText);
        }
    }

    handleKeyDown = (event: any) => {
        if (event.key === 'Enter') {
            if (this.state.searchText) {
                this.searchBook(this.state.searchText);
            }
        }
    }

    handleSearchChange = (event: any) => {
        const searchByBook = event.target.value;
        this.setState({searchText: event.target.value});
    }

    render() {
        const {classes} = this.props;
        const {searchText, books, loaded} = this.state;
        return (
            <React.Fragment>
                <FindLine
                    searchText={searchText}
                    onClickFind={this.handleSearchBook}
                    placeholder="Поиск по названию книги"
                    onChangeField={this.handleSearchChange}
                />
                {books.length > 0 &&
                <Container maxWidth="lg">
                    <Grid container spacing={4}>
                        {books.map(book => (
                            <Grid key={book.id} item xs={12} sm={6} md={4}>
                                <BookCard book={book} preview={true}/>
                            </Grid>
                        ))}
                    </Grid>
                </Container>
                }
                {books.length === 0 && loaded &&
                <Container maxWidth="lg">
                    <CircularProgress/>
                </Container>
                }
            </React.Fragment>
        );
    }
}

export default withStyles(styles)(Books);
