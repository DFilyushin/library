import React, { Component } from 'react';
import Genre from '../models/Genre';
import { List, ListItem, ListItemText, withStyles, Theme, Collapse, Divider } from '@material-ui/core';

interface State {
    genres: Genre[];
}

const styles = ({ spacing, palette } : Theme) => ({
    root: {
      width: '100%',
      maxWidth: 360,
      backgroundColor: palette.background.paper,
    },
    nested: {
      paddingLeft: spacing.unit,
    },
  });

class Genres extends Component<any, State> {
    private static GenresData: Array<Genre> = [];

    constructor(props: any) {
        super(props);
        this.state = {
            genres: []
        };
    }

    componentDidMount() {
        if (Genres.GenresData.length) {
            this.setState({
                genres: Genres.GenresData
            });
            return;
        }

        fetch('http://books.toadstool.online/api/v1/genres')
        .then(results => {
            return results.json();
        })
        .then((data: Array<Genre>) => {
            let sorted = data.sort((a, b) => {
                if (a.titles.ru < b.titles.ru) {
                    return -1;
                }
                if (a.titles.ru > b.titles.ru) {
                    return 1;
                }
                return 0;
            });
   
            this.setState({
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

    render() {
        const { classes } = this.props;
        return (
            <List component="nav" classes={classes}>
            {
                this.state.genres.map(g => {
                    return (
                        <React.Fragment>
                        <ListItemLink href={'#/genres/' + g.id}>
                            <ListItemText primary={g.titles.ru} secondary={g.detailed.ru} />
                        </ListItemLink>
                        <Divider />
                        <Collapse in={true} timeout="auto" unmountOnExit>
                            <List dense={true}>
                            {
                                g.sub_genres
                                .sort((a, b) => {
                                    if (a.titles.ru < b.titles.ru) {
                                        return -1;
                                    }
                                    if (a.titles.ru > b.titles.ru) {
                                        return 1;
                                    }
                                    return 0;
                                })
                                .map(s => {
                                    return (
                                        <React.Fragment>
                                        <ListItemLink href={'#/genres/' + g.id + '/' + s._id} className={classes.nested}>
                                            <ListItemText inset primary={s.titles.ru} />
                                        </ListItemLink>
                                        </React.Fragment>
                                    );
                                })
                            }
                            </List>
                        </Collapse>
                        <Divider />
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