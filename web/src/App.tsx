import React, { Component } from 'react';
import { Link, Redirect, Route, Switch, withRouter } from 'react-router-dom';

import { Tab, Tabs, Theme, Toolbar, withStyles } from '@material-ui/core';
import AppBar from '@material-ui/core/AppBar';

import Authors from './components/Authors';
import BookPage from './components/BookPage';
import Books from './components/Books';
import BooksList from './components/BooksList';
import Genres from './components/Genres';
import Author from './models/Author';

interface State {
    searchText: string;
    authors: Author[];
}

interface Props {
    history?: any;
}

const styles = (theme: Theme) => ({
    root: {
        marginTop: theme.spacing(4),
    },
    grow: {
        flexGrow: 1,
    },
    menuButton: {
        marginLeft: -12,
        marginRight: 20,
    },
    title: {
        display: 'none',
        [theme.breakpoints.up('sm')]: {
            display: 'block',
        },
    },
});

class App extends Component<any, State> {

    constructor(props: any) {
        super(props);
        this.state = {
            searchText: '',
            authors: []
        };
    }

    render() {
        const { history, classes } = this.props;
        const {  } = this.state;

        const route = '/' + history.location.pathname.split('/')[1];
        return (
            <React.Fragment>
                <AppBar position="sticky">
                    <Toolbar>
                        <Tabs value={route}>
                            <TabLink label="Жанры" value="/genres" component={Link as any} to="/genres" />
                            <TabLink label="Авторы" value="/authors" component={Link as any} to="/authors" />
                            <TabLink label="Книги" value="/books" component={Link as any} to="/books" />
                        </Tabs>
                    </Toolbar>
                </AppBar>
                <div className={classes.root}>
                    <Switch>
                        <Route exact path="/" render={() => <Redirect to="/genres" />} />
                        <Route exact path="/authors" component={Authors} />
                        <Route exact path="/genres" component={Genres} />
                        <Route exact path="/books" component={Books} />
                        <Route path="/genres/:genre" component={BooksList} />
                        <Route path="/authors/:authorId" component={BooksList} />
                        <Route path="/books/:bookId" component={BookPage} />
                    </Switch>
                </div>
            </React.Fragment>
        );
    }
}

const TabLink = (props: any) => (
    <Tab {...props} component={Link as any} />
);

export default withStyles(styles)(withRouter(App));
