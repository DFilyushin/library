import React, { Component } from 'react';
import AppBar from '@material-ui/core/AppBar';
import Genres from './components/Genres';
import { Route, Link, withRouter, Redirect } from 'react-router-dom';
import { Tabs, Tab, Theme, withStyles, Toolbar } from '@material-ui/core';
import Authors from './components/Authors';
import BooksList from './components/BooksList';
import Books from './components/Books';
import BookPage from './components/BookPage';

interface State {
}

interface Props {
    history?: any;
}

const styles = ({ spacing, palette, breakpoints, shape, transitions } : Theme) => ({
    root: {
      width: '100%',
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
      [breakpoints.up('sm')]: {
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
        const { history } = this.props;
        const {  } = this.state;
        
        let route = '/' + history.location.pathname.split('/')[1];
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
                <Route exact path="/" render={() => <Redirect to="/genres" />} />
                <Route exact path="/authors" component={Authors} />
                <Route exact path="/genres" component={Genres} />
                <Route exact path="/books" component={Books} />
                <Route path="/genres/:genre" component={BooksList} />
                <Route path="/authors/:authorId" component={BooksList} />
                <Route path="/books/:bookId" component={BookPage} />
            </React.Fragment>
        );
    }
}

const TabLink = (props: any) => (
    <Tab {...props} component={Link as any} />
)

export default withStyles(styles)(withRouter(App));
