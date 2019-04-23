import React, { Component } from 'react';
import Author from './models/Author';
import Book from './models/Book';
import AppBar from '@material-ui/core/AppBar';
import Genres from './components/Genres';
import { Route, Link, withRouter, Redirect } from 'react-router-dom';
import { Tabs, Tab } from '@material-ui/core';
import Authors from './components/Authors';
import Books from './components/Books';
import GenresBooks from './components/GenresBooks';

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
        let route = '/' + this.props.history.location.pathname.split('/')[1];
        return (
            <React.Fragment>
                <AppBar position="sticky">
                <Tabs value={route}>
                    <TabLink label="Авторы" value="/authors" component={Link as any} to="/authors" />
                    <TabLink label="Жанры" value="/genres" component={Link as any} to="/genres" />
                </Tabs>
                </AppBar>
                <Route exact path="/" render={() => <Redirect to="/authors" />} />
                <Route exact path="/authors" component={Authors} />
                <Route exact path="/genres" component={Genres} />
                <Route path="/genres/:genre" component={GenresBooks} />
            </React.Fragment>
        );
    }
}

const TabLink = (props: any) => (
    <Tab {...props} component={Link as any} />
)

export default withRouter(App);
