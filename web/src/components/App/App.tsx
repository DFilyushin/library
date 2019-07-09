import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';

import { Tab, Tabs, Theme, Toolbar, withStyles } from '@material-ui/core';
import AppBar from '@material-ui/core/AppBar';

import Author from '../../models/Author';
import { Routes } from './Routes';

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
                    <Routes />
                </div>
            </React.Fragment>
        );
    }
}

const TabLink = (props: any) => (
    <Tab {...props} component={Link as any} />
);

export default withStyles(styles)(withRouter(App));
