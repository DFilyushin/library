import React, { Component } from 'react';
import Author from './models/Author';
import Book from './models/Book';
import Info from './models/Info';
import AppBar from '@material-ui/core/AppBar';
import Genres from './components/Genres';
import { Route, Link, BrowserRouter as Router, HashRouter, withRouter } from 'react-router-dom';
import { Tabs, Tab, Theme, withStyles, } from '@material-ui/core';
import Authors from './components/Authors';
import Books from './components/Books';

interface State {
    letters: string[];
    authors: Author[];
    books: Book[];
    typed: string;
}

interface Props {
    history?: any;
}

class App extends Component<any, State> {

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

        fetch('http://books.toadstool.online/api/v1/info')
            .then(results => {
                return results.json();
            })
            .then((data: Info) => {
                this.setState({
                    ...this.state,
                    letters: data.authorsLetters
                });
            });
    }

    onLetterChange(letter: string) {
        fetch('http://books.toadstool.online/api/v1/authors/start_with/' + letter + '?limit=10')
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
        debugger;
        let route = '/' + this.props.history.location.pathname.split('/')[1];
        return (
            <React.Fragment>
                <AppBar position="sticky">
                <Tabs value={route}>
                    <TabLink label="Авторы" value="/" component={Link as any} exact to="/" />
                    <TabLink label="Жанры" value="/genres" component={Link as any} to="/genres" />
                    <TabLink label="Книги" value="/books" component={Link as any} to="/books" />
                </Tabs>
                </AppBar>
                <Route exact path="/" component={Authors} />
                <Route path="/genres" component={Genres} />
                <Route path="/books" component={Books} />
            </React.Fragment>
        );
    }
}

const TabLink = (props: any) => (
    <Tab {...props} component={Link as any} />
)

export default withRouter(App);
