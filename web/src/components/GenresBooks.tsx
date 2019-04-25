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
        const by = this.props.history.location.pathname.split('/')[1];
        const id = this.props.history.location.pathname.split('/')[2];

        const url = this.booksUrl(by, id);
        if (!url) {
            return;
        }

        fetch(url)
            .then(results => {
                return results.json();
            })
            .then((data: Array<Book>) => {
                const sorted = data.sort((a, b) => {
                    if (a.series && !b.series) {
                        return -1;
                    }
                    if (!a.series && b.series) {
                        return 1;
                    }
                    if (a.series && b.series) {
                        if (a.series < b.series) {
                            return -1;
                        }
                        if (a.series > b.series) {
                            return 1;
                        }
                        if (a.sernum && b.sernum) {
                            return Number(a.sernum) - Number(b.sernum);
                        }
                    }
                    if (a.name < b.name) {
                        return -1;
                    }
                    if (a.name > b.name) {
                        return 1;
                    }
                    return 0;
                });
                this.setState({
                    books: sorted
                });
            })
            .catch(e => {
                console.log(e);
            })
    }

    booksUrl(by: string, id: string) {
        switch(by.toLowerCase())
        {
            case 'genres':
                return 'http://books.toadstool.online/api/v1/books/by_genre/' + id;
            case 'authors':
                return 'http://books.toadstool.online/api/v1/books/by_author/' + id;
            default:
                return null;
        }
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
                books.map(book => {
                    return (
                        <Card className={classes.card} key={book.id}>
                                <CardContent>
                                    <Typography component="h5" variant="h5">
                                        {book.name}
                                    </Typography>
                                    {book.series && <Typography variant="subtitle1" color="textSecondary">{book.series}{Number(book.sernum) > 0 && ': ' + book.sernum}</Typography>}
                                    {
                                        book.authors.map((author, index) => {
                                            let name = '';
                                            if (author.last_name) {
                                                name += author.last_name;
                                            }
                                            if (author.first_name) {
                                                name += ' ' + author.first_name;
                                            }
                                            if (author.middle_name) {
                                                name += ' ' + author.middle_name;
                                            }

                                            const link = <Link variant="subtitle2" href={'/#/authors/' + author._id} key={author._id}>{name}</Link>;
                                            return index === 0 ? link :
                                                <React.Fragment key={author.id}>
                                                    {', '}
                                                    {link}
                                                </React.Fragment>;
                                        })
                                    }
                                    <Typography variant="caption">{book.lang}</Typography>
                                </CardContent>
                            <CardActions>
                                <Button href={'http://books.toadstool.online/api/v1/books/' + book.id + '/content'}>Скачать</Button>
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