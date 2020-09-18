import React, { Component } from 'react';

import { InputBase, List, ListItem, ListItemText, Theme, withStyles, Button } from '@material-ui/core';

import Endpoints from '../utils/Endpoints';
import Author from '../models/Author';

interface Props {
    classes: any;
}

interface State {
    searchText: string;
    authors: Author[];
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
      // width: '100%',
    },
  });

class Authors extends Component<Props, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            searchText: '',
            authors: []
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
                authors: []
            });
        }
    }

    handleSearchChange = (event: any)  => {
        const searchByAuthor = event.target.value;
        this.setState({ searchText: event.target.value });
    }

    handleSearchAuthor = (event: any) => {
        console.log(this.state.searchText);
        if (this.state.searchText) {
            fetch(Endpoints.getAuthorsStartWith(this.state.searchText, 15, 0))
                .then(results => {
                    return results.json();
                })
                .then((data: Author[]) => {
                    this.setState({
                        authors: data
                    });
                })
                .catch(() => {
                    this.setState({ authors: [] });
                });
        }
    }

    render() {
        const { classes } = this.props;
        const { searchText, authors } = this.state;
        return (
            <React.Fragment>
                <InputBase
                    value={searchText}
                    onChange={this.handleSearchChange}
                    autoFocus
                    placeholder="Поиск по фамилии имени автора"
                    classes={{
                        root: classes.inputRoot,
                        input: classes.inputInput,
                    }}
                />
                <Button onClick={this.handleSearchAuthor}>Поиск</Button>
                {authors.length > 0 &&
                    <List className={classes.root}>
                        {
                            authors.map((author) => {
                                return (
                                    <ListItemLink href={'/#/authors/' + author.id} key={author.id}>
                                        <ListItemText>{author.last_name} {author.first_name} {author.middle_name}</ListItemText>
                                    </ListItemLink>
                                );
                            })
                        }
                    </List>
                }
            </React.Fragment>
        );
    }
}

function ListItemLink(props: any): JSX.Element {
    return <ListItem button component="a" {...props} />;
}

export default withStyles(styles)(Authors);
