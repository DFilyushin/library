import React, { Component } from 'react';
import Genre from '../models/Genre';
import { List, ListItem, ListItemText, withStyles, Theme, Collapse, Divider, ListItemSecondaryAction, IconButton } from '@material-ui/core';
import CircularProgress from '@material-ui/core/CircularProgress';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';

interface State {
    loading: boolean;
    genres: Genre[];
    expanded: string;
}

const styles = ({ spacing, palette } : Theme) => ({
    root: {
      width: '100%',
      maxWidth: 360,
      backgroundColor: palette.background.paper,
    },
    progress: {
        margin: spacing.unit * 2,
    },
  });

class Genres extends Component<any, State> {
    private static GenresData: Array<Genre> = [];

    constructor(props: any) {
        super(props);
        this.state = {
            loading: false,
            genres: [],
            expanded: ''
        };
    }

    componentDidMount() {
        if (Genres.GenresData.length) {
            this.setState({
                genres: Genres.GenresData
            });
            return;
        }

        this.setState({ loading: true })
        fetch('http://books.toadstool.online/api/v1/genres')
            .then(results => {
                return results.json();
            })
            .then((data: Array<Genre>) => {
                // sort genres
                let sorted = data.sort((a, b) => {
                    if (a.titles.ru < b.titles.ru) {
                        return -1;
                    }
                    if (a.titles.ru > b.titles.ru) {
                        return 1;
                    }
                    return 0;
                });
                
                // sort sub-genres
                sorted.forEach(g => {
                    g.sub_genres = g.sub_genres.sort((a, b) => {
                        if (a.titles.ru < b.titles.ru) {
                            return -1;
                        }
                        if (a.titles.ru > b.titles.ru) {
                            return 1;
                        }
                        return 0;
                    });
                });
    
                this.setState({
                    loading: false,
                    genres: sorted
                });

                Genres.GenresData = sorted;
            })
            .catch(e => {
                console.log(e);
            });
    }

    selectAuthor(event: any, id: string | undefined) {
        this.setState({
            ...this.state
        })
    }

    handleClick = (event: Event | undefined, genre: string) => {
        event!.preventDefault();
        this.setState(state => ({ expanded: state.expanded === genre ? '' : genre }));
    };

    render() {
        const { classes} = this.props;
        const { loading, genres, expanded } = this.state;

        if (loading) {
            return <CircularProgress className={classes.progress} />;
        }

        return (
            <List component="nav" className={classes.root}>
            {
                genres.map(genre => {
                    return (
                        <React.Fragment key={genre.id}>
                        <ListItemLink href={'#/genres/' + genre.id}>
                            <ListItemText primary={genre.titles.ru} secondary={genre.detailed.ru} />
                            <IconButton onClick={() => this.handleClick(event, genre.id)}>
                                {genre.id === expanded ? <ExpandLess /> : <ExpandMore />}
                            </IconButton>
                        </ListItemLink>
                        <Divider />
                        <Collapse in={genre.id === expanded} timeout="auto" unmountOnExit>
                            <List dense={true}>
                            {
                                genre.sub_genres.map(subgenre => {
                                    return (
                                        <ListItemLink href={'#/genres/' + subgenre.id} key={subgenre.id}>
                                            <ListItemText inset primary={subgenre.titles.ru} />
                                        </ListItemLink>
                                    );
                                })
                            }
                            </List>
                        </Collapse>
                        </React.Fragment>
                    );
                })
            }
            </List>
        );
    }
}

function ListItemLink(props: any): JSX.Element {
    return <ListItem button component="a" {...props} />;
}

export default withStyles(styles)(Genres);