import React, { Component } from 'react';
import { Typography, Card, CardContent, withStyles, CardActions, Button, CardActionArea, Link } from '@material-ui/core';
import Book from '../models/Book';
import { Redirect } from 'react-router';

interface State
{
    loading: boolean;
    books: Book[];
    downloadBookId: string;
}

const styles = {
    card: {
        maxWidth: 500,
    },
    media: {
        height: 140,
    },
};

class GenresBooks extends Component<any, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            loading: false,
            books: [],
            downloadBookId: ''
        };
    }

    componentDidMount() {
        const genre = this.props.history.location.pathname.split('/')[2];

        fetch('http://books.toadstool.online/api/v1/books/by_genre/' + genre)
            .then(results => {
                return results.json();
            })
            .then((data: Array<Book>) => {
                this.setState({
                    books: data
                });
            })
            .catch(e => {
                console.log(e);
            })
    }

    handleDownloadClick(event: any, book: Book) {
        this.setState({ downloadBookId: book.id });
    }

    render() {
        const { classes } = this.props;
        const { books, downloadBookId } = this.state;

        if (books.length === 0) {
            return null;
        }

        if (downloadBookId) {
            return <Redirect to={'http://books.toadstool.online/api/v1/books/' + downloadBookId + '/content'} />;
        }

        return (
            <React.Fragment>
            {
                books.map(b => {
                    return (
                        <Card className={classes.card}>
                            <CardActionArea>
                                <CardContent>
                                    <Typography gutterBottom variant="h5">
                                        {b.name}
                                    </Typography>
                                    <Typography component="p">
                                    {
                                        b.authors.map((a, index) => {
                                            let name = index === 0 ? '' : ', ';
                                            if (a.last_name) {
                                                name += a.last_name;
                                            }
                                            if (a.first_name) {
                                                name += ' ' + a.first_name;
                                            }
                                            if (a.middle_name) {
                                                name += ' ' + a.middle_name;
                                            }
                                            return name;
                                        })
                                    }
                                    </Typography>
                                    <Typography variant="caption">{b.lang}</Typography>
                                </CardContent>
                            </CardActionArea>
                            <CardActions>
                                <Button href={'http://books.toadstool.online/api/v1/books/' + b.id + '/content'}>Скачать</Button>
                            </CardActions>
                        </Card>
                    )
                })
            }
            </React.Fragment>
        );
    }
}

export default withStyles(styles)(GenresBooks);