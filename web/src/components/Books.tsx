import React, {Component} from 'react';

import {Button, Container, Grid, InputBase, Theme, withStyles} from '@material-ui/core';
import CircularProgress from '@material-ui/core/CircularProgress';

import Book from '../models/Book';
import Endpoints from '../utils/Endpoints';
import BookCard from './BookCard';

interface State {
    searchText: string;
    books: Book[];
    find: boolean;
}

const styles = (theme: Theme) => ({
    root: {
        width: '100%',
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
    },
    inputRoot: {
        color: 'inherit',
        width: '50%',
        backgroundColor: theme.palette.common.white
    },
    inputInput: {
        paddingTop: theme.spacing(1),
        paddingRight: theme.spacing(1),
        paddingBottom: theme.spacing(1),
        paddingLeft: theme.spacing(1),
        width: '100%',
    },
});

class Books extends Component<any, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            searchText: '',
            books: [],
            find: false
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
        this.setState({find: true});
        fetch(Endpoints.getBooksByName(findString, 15, 0))
            .then(results => {
                return results.json();
            })
            .then((data: Book[]) => {
                this.setState({
                    books: data,
                    find: false
                });
            })
            .catch(() => {
                this.setState({books: []});
                this.setState({find: false});
            });
    };

    handleSearchBook = (event: any) => {
        if (this.state.searchText) {
            this.searchBook(this.state.searchText);
        }
    };

    handleKeyDown = (event: any) => {
        if (event.key === 'Enter') {
            if (this.state.searchText) {
                this.searchBook(this.state.searchText);
            }
        }
    };

    handleSearchChange = (event: any) => {
        const searchByBook = event.target.value;
        this.setState({searchText: event.target.value});
    };

    render() {
        const {classes} = this.props;
        const {searchText, books, find} = this.state;
        return (
            <React.Fragment>
                <InputBase
                    value={searchText}
                    onChange={this.handleSearchChange}
                    onKeyDown={this.handleKeyDown}
                    autoFocus
                    placeholder="Поиск по названию книги"
                    classes={{
                        root: classes.inputRoot,
                        input: classes.inputInput,
                    }}
                />
                <Button onClick={this.handleSearchBook}>Поиск</Button>
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
                {books.length === 0  && find &&
                <Container maxWidth="lg">
                    <CircularProgress/>
                </Container>
                }
            </React.Fragment>
        );
    }
}

export default withStyles(styles)(Books);
