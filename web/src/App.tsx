import React, { Component } from 'react';
import Genres from './Genres';
import Authors from './Authors';
import Books from './Books';
import AuthorsLetters from './AuthorsLetters';
import Author from './models/Author';
import Book from './models/Book';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import './App.css';

interface State {
    letters: string[];
    authors: Author[];
    books: Book[];
    typed: string;
}

class App extends Component<{}, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            letters: [],
            authors: [],
            books: [],
            typed: ''
        };
    }

    componentWillMount() {

        fetch('http://books.toadstool.online/api/v1/authors/letters')
            .then(results => {
                return results.json();
            })
            .then((data: string[]) => {
                this.setState({ 
                    letters: data,
                    authors: [],
                    typed: ''
                });
            });
    }

    onLetterChange(letter: string) {
        fetch('http://books.toadstool.online/api/v1/authors/start_with/' + letter + '?limit=10000')
            .then(results => {
                return results.json();
            })
            .then((data: Array<Author>) => {
                this.setState({
                    ...this.state,
                    authors: data,
                    typed: letter
                });
            });
    }

    onAuthorChange(authorId: string | undefined) {
        fetch('http://books.toadstool.online/api/v1/books/by_author/' + authorId)
            .then(results => {
                return results.json();
            })
            .then((data: Array<Book>) => {
                this.setState({
                    ...this.state,
                    books: data
                });
            });
    }

    render() {
        return (
            <div className="App">
                <AppBar position="sticky" color="default">
                    <Toolbar>
                        <Typography variant="h6" color="inherit">
                            <AuthorsLetters letters={this.state.letters} onLetterChange={this.onLetterChange.bind(this)}/>
                        </Typography>
                    </Toolbar>
                </AppBar>
                <table>
                    <thead>
                    <tr>
                        <th>Авторы</th>
                        <th>Жанры</th>
                        <th>Книги</th>
                    </tr>
                    </thead>

                    <tbody>
                    <tr>
                        <td><Authors authors={this.state.authors} typed={this.state.typed} onAuthorChange={this.onAuthorChange.bind(this)}/></td>
                        <td><Genres /></td>
                        <td><Books books={this.state.books} /></td>
                    </tr>
                    </tbody>
                </table>
            </div>
        );
    }
}

export default App;
