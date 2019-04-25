import React, { Component } from "react";
import { Card, CardContent, Typography, Link, CardActions, Button, withStyles } from "@material-ui/core";
import Book from "../models/Book";

interface Prop {
    classes: any;
    book: Book;
}

interface State {

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
    }

    render() {
        const { classes, book } = this.props;
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
        );
    }
}

export default withStyles(styles)(BookCard);