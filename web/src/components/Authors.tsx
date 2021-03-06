import React, {Component} from 'react';

import {List, ListItem, ListItemText, Theme, withStyles, Container} from '@material-ui/core';
import CircularProgress from '@material-ui/core/CircularProgress';

import FindLine from './FindLine';
import Endpoints from '../utils/Endpoints';
import Author from '../models/Author';

interface Props {
    classes: any;
}

interface State {
    searchText: string;
    authors: Author[];
    loaded: boolean;
}

const styles = (theme: Theme) => ({
    root: {
        paddingTop: theme.spacing(5),
        width: '100%',
        backgroundColor: theme.palette.background.paper,
    },
});

class Authors extends Component<Props, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            searchText: '',
            authors: [],
            loaded: false
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

    handleSearchChange = (event: any) => {
        const searchByAuthor = event.target.value;
        this.setState({searchText: event.target.value});
    }

    findAuthors = async (textString: string) => {
        this.setState({loaded: true});
        fetch(Endpoints.getAuthorsStartWith(textString, 15, 0))
            .then(results => {
                return results.json();
            })
            .then((data: Author[]) => {
                this.setState({
                    authors: data,
                    loaded: false
                });
            })
            .catch(() => {
                this.setState({authors: [], loaded: false});
            });
    }

    handleSearchAuthor = (event: any) => {
        if (this.state.searchText) {
            this.findAuthors(this.state.searchText);
        }
    }

    render() {
        const {classes} = this.props;
        const {searchText, authors, loaded} = this.state;
        return (
            <React.Fragment>
                <FindLine
                    searchText={searchText}
                    onClickFind={this.handleSearchAuthor}
                    placeholder="Поиск по фамилии имени автора"
                    onChangeField={this.handleSearchChange}
                />
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
                {authors.length === 0 && loaded &&
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
