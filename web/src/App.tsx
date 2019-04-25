import React, { Component } from 'react';
import AppBar from '@material-ui/core/AppBar';
import Genres from './components/Genres';
import { Route, Link, withRouter, Redirect } from 'react-router-dom';
import { Tabs, Tab, Theme, withStyles, Toolbar } from '@material-ui/core';
import Authors from './components/Authors';
import GenresBooks from './components/GenresBooks';

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
                            <TabLink label="Авторы" value="/authors" component={Link as any} to="/authors" />
                            <TabLink label="Жанры" value="/genres" component={Link as any} to="/genres" />
                        </Tabs>
                    </Toolbar>
                </AppBar>
                <Route exact path="/" render={() => <Redirect to="/authors" />} />
                <Route exact path="/authors" component={Authors} />
                <Route exact path="/genres" component={Genres} />
                <Route path="/genres/:genre" component={GenresBooks} />
                <Route path="/authors/:author" component={GenresBooks} />
            </React.Fragment>
        );
    }
}

const TabLink = (props: any) => (
    <Tab {...props} component={Link as any} />
)

export default withStyles(styles)(withRouter(App));
