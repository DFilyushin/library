import React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

import Authors from '../Authors';
import BookPage from '../BookPage';
import Books from '../Books';
import BooksList from '../BooksList';
import Genres from '../Genres';

export const Routes = () => (
    <Switch>
        <Route exact path="/" render={() => <Redirect to="/genres" />} />
        <Route exact path="/authors" component={Authors} />
        <Route exact path="/genres" component={Genres} />
        <Route exact path="/books" component={Books} />
        <Route path="/genres/:genre" component={BooksList} />
        <Route path="/authors/:authorId" component={BooksList} />
        <Route path="/books/:bookId" component={BookPage} />
    </Switch>
);
