import React, { Component } from 'react';
import Author from '../models/Author';
import { Typography, ListItemText, List, ListItem, Paper, Theme, withStyles, TextField, InputBase } from '@material-ui/core';
import { red } from '@material-ui/core/colors';

interface Props {
    classes: any;
}

interface State {
    searchText: string;
    authors: Author[];
}

const styles = ({ palette, shape, breakpoints, spacing, transitions } : Theme) => ({
    root: {
      width: '100%',
      maxWidth: 360,
      backgroundColor: palette.background.paper,
    },
    inputRoot: {
      color: 'inherit',
      width: '100%',
      backgroundColor: palette.common.white
    },
    inputInput: {
      paddingTop: spacing.unit,
      paddingRight: spacing.unit,
      paddingBottom: spacing.unit,
      paddingLeft: spacing.unit,
      transition: transitions.create('width'),
      width: '100%',
      [breakpoints.up('sm')]: {
        width: 120,
        '&:focus': {
          width: 200,
        },
      },
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

    componentDidMount(){
        document.addEventListener("keydown", this.escFunction, false);
    }
    
    componentWillUnmount(){
        document.removeEventListener("keydown", this.escFunction, false);
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

        if (searchByAuthor) {
            fetch('http://books.toadstool.online/api/v1/authors/start_with/' + searchByAuthor + '?limit=15')
                .then(results => {
                    return results.json();
                })
                .then((data: Array<Author>) => {
                    this.setState({
                        authors: data
                    });
                })
                .catch(() => {
                    this.setState({ authors: [] })
                });
        }

        this.setState({ searchText: event.target.value });
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
                    placeholder="Поиск по ФИО автора"
                    classes={{
                        root: classes.inputRoot,
                        input: classes.inputInput,
                    }}
                />
                {authors.length > 0 &&
                    <List className={classes.root}>
                        {
                            authors.map((author) => {
                                return (
                                    <ListItemLink href={'/#/authors/' + author.id}>
                                        <ListItemText>{author.last_name} {author.first_name} {author.middle_name}</ListItemText>
                                    </ListItemLink>
                                )
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