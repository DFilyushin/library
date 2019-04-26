import React, { Component } from "react";
import { Card, CardContent, Typography, Link, CardActions, Button, withStyles } from "@material-ui/core";
import Book from "../models/Book";
import Endpoints from "../Endpoints";
import FB2Info from "../models/FB2Info";

interface Prop {
    classes: any;
    book: Book;
}

interface State {
    info: FB2Info;
}

const styles = {
    card: {
        maxWidth: 500,
    },
    media: {
        height: 140,
    },
};

class BookCard extends Component<Prop, State> {

    constructor(props: any) {
        super(props);
        this.state = {
            info: {
                city: '',
                publisher: '',
                year: '',
                isbn: ''
            }
        }
    }

    componentDidMount() {
        if (this.props.book) {
            const url = Endpoints.getBooksFB2Info(this.props.book.id);
            fetch(url)
                .then(results => {
                    return results.json()
                })
                .then((data: Array<FB2Info>) => {
                    this.setState({
                        info: data[0]
                    })
                })
                .catch(() => {
                    this.setState({
                        info: {}
                    });
                });
        }
    }

    render() {
        const { classes, book } = this.props;
        const { info } = this.state;
        return (
            <Card className={classes.card} key={book.id}>
                <CardContent>
                    <Typography component="h5" variant="h5">
                        {book.name}
                    </Typography>
                    {book.series && <Typography variant="subtitle1" color="textSecondary">{book.series}{Number(book.sernum) > 0 && ': ' + book.sernum}</Typography>}
                    {info && <Typography variant="subtitle1" color="textSecondary">{`${info.city}, ${info.publisher}, ${info.year}`}</Typography>}
                    {info && info.isbn && <Typography variant="caption">{`ISBN ${info.isbn}`}</Typography>}
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
                                <React.Fragment key={author._id}>
                                    {', '}
                                    {link}
                                </React.Fragment>;
                        })
                    }
                    <Typography variant="caption">{book.lang}</Typography>
                </CardContent>
                <CardActions>
                    <Button href={Endpoints.getBooksContent(book.id)}>Скачать</Button>
                </CardActions>
            </Card>
        );
    }
}

export default withStyles(styles)(BookCard);