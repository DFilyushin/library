import React, { Component } from 'react';
import Book from '../models/Book';
import { InputBase, Theme, withStyles } from '@material-ui/core';
import BookCard from './BookCard';
import Endpoints from '../Endpoints';

interface State {
    searchText: string;
    books: Book[];
}

const styles = ({ palette, spacing } : Theme) => ({
    root: {
      width: '100%',
      maxWidth: 360,
      backgroundColor: palette.background.paper,
    },
    inputRoot: {
      color: 'inherit',
      width: '100%',
      backgroundColor: palette.common.white
    },
    inputInput: {
      paddingTop: spacing.unit,
      paddingRight: spacing.unit,
      paddingBottom: spacing.unit,
      paddingLeft: spacing.unit,
      width: '100%',
    },
  });

class Books extends Component<any, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            searchText: '',
            books: []
        }
    }

    componentDidMount(){
        document.addEventListener("keydown", this.escFunction, false);
    }
    
    componentWillUnmount(){
        document.removeEventListener("keydown", this.escFunction, false);
    }

    escFunction = (event: any) => {
        if (event.keyCode === 27) {
            this.setState({
                searchText: '',
                books: []
            });
        }
    }

    handleSearchChange = (event: any)  => {
        const searchByBook = event.target.value;

        if (searchByBook) {
            fetch(Endpoints.getBooksByName(searchByBook, 15, 0))
                .then(results => {
                    return results.json();
                })
                .then((data: Array<Book>) => {
                    this.setState({
                        books: data
                    });
                })
                .catch(() => {
                    this.setState({ books: [] })
                });
        }

        this.setState({ searchText: event.target.value });
    }

    render() {
        const { classes } = this.props;
        const { searchText, books } = this.state;
        return (
            <React.Fragment>
                <InputBase
                    value={searchText}
                    onChange={this.handleSearchChange}
                    autoFocus
                    placeholder="Поиск по названию книги"
                    classes={{
                        root: classes.inputRoot,
                        input: classes.inputInput,
                    }}
                />
                {books.length > 0 &&
                    <React.Fragment>
                        {
                            books.map(book => <BookCard book={book}/>)
                        }
                    </React.Fragment>
                }
            </React.Fragment>
        );
    }
}

export default withStyles(styles)(Books);