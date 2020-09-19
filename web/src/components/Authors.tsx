import React, { Component } from 'react';

import {InputBase, List, ListItem, ListItemText, Theme, withStyles, Button, Container} from '@material-ui/core';
import CircularProgress from '@material-ui/core/CircularProgress';

import Endpoints from '../utils/Endpoints';
import Author from '../models/Author';

interface Props {
    classes: any;
}

interface State {
    searchText: string;
    authors: Author[];
    find: boolean;
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
            authors: [],
            find: false
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

    handleKeyDown = (event: any) => {
        if (event.key === 'Enter') {
            this.findAuthors(this.state.searchText)
        }
    }

    handleSearchChange = (event: any)  => {
        const searchByAuthor = event.target.value;
        this.setState({ searchText: event.target.value });
    }

    findAuthors = async (textString: string) => {
        this.setState({find: true})
        fetch(Endpoints.getAuthorsStartWith(textString, 15, 0))
            .then(results => {
                return results.json();
            })
            .then((data: Author[]) => {
                this.setState({
                    authors: data,
                    find: false
                });
            })
            .catch(() => {
                this.setState({ authors: [], find: false });
            });
    }

    handleSearchAuthor = (event: any) => {
        if (this.state.searchText) {
            this.findAuthors(this.state.searchText)
        }
    }

    render() {
        const { classes } = this.props;
        const { searchText, authors, find } = this.state;
        return (
            <React.Fragment>
                <InputBase
                    value={searchText}
                    onChange={this.handleSearchChange}
                    onKeyDown={this.handleKeyDown}
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
                {authors.length === 0  && find &&
                <Container maxWidth="lg">
                    <CircularProgress/>
                </Container>
                }
            </React.Fragment>
        );
    }
}

function ListItemLink(props: any): JSX.Element {
    return <ListItem button component="a" {...props} />;
}

export default withStyles(styles)(Authors);
