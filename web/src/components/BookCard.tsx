import React, { Component } from "react";
import { Card, CardContent, Typography, Link, CardActions, Button, withStyles, CardActionArea, CardMedia } from "@material-ui/core";
import Book from "../models/Book";
import Endpoints from "../Endpoints";
import Author from "../models/Author";
import CyrillicToTranslit from "../../node_modules/cyrillic-to-translit-js/CyrillicToTranslit";

interface Prop {
    classes: any;
    book: Book;
    preview: boolean;
    noLinkForAuthorId: string;
}

interface State {
}

const styles = {
    card: {
        maxWidth: 500
    },
    preview: {
    },
    cover: {
        width: 151,
    },
    media: {
        height: 140,
    },
};

class BookCard extends Component<Prop, State> {

    private abortController = new AbortController();

    constructor(props: any) {
        super(props);
        this.state = {
        }
    }

    render() {
        return this.props.preview
            ? this.renderPreview()
            : this.renderFull();
    }

    private renderPreview() {
        const { classes, book } = this.props;
        return (
            <Card className={classes.card}>
                <CardActionArea href={`/#/books/${book.id}/${this.transliterate(book.name)}`}>
                <CardContent className={classes.content}>
                    {this.renderCover(book)}
                    <Typography component="h5" variant="h5">{book.name}</Typography>
                    {book.series && <Typography variant="subtitle1" color="textSecondary">{book.series}{Number(book.sernum) > 0 && ': ' + book.sernum}</Typography>}
                    {this.renderAuthors(book.authors)}
                    {book.city && <Typography variant="subtitle1" color="textSecondary">{`${book.city}, ${book.publisher}, ${book.year}`}</Typography>}
                </CardContent>
                </CardActionArea>
            </Card>
        );
    }

    private renderFull() {
        const { classes, book } = this.props;
        return (
            <Card className={classes.card}>
                <CardContent>
                    {this.renderCover(book)}
                    <Typography component="h5" variant="h5">{book.name}</Typography>
                    {book.series && <Typography variant="subtitle1" color="textSecondary">{book.series}{Number(book.sernum) > 0 && ': ' + book.sernum}</Typography>}
                    {this.renderAuthors(book.authors)}
                    {book.city && <Typography variant="subtitle1" color="textSecondary">{`${book.city}, ${book.publisher}, ${book.year}`}</Typography>}
                    {book.isbn && <Typography variant="caption">{`ISBN ${book.isbn}`}</Typography>}
                </CardContent>
                <CardActions>
                    <Button href={Endpoints.getBooksContent(book.id)}>Скачать FB2</Button>
                </CardActions>
            </Card>
        );
    }

    private renderCover(book: Book): JSX.Element | null {
        return (
            <div className="books">
                <div className="book">
                    <img style={styles.preview} src={'cover/' + book.id + '.jpg'} title={book.name} />
                </div>
            </div>
        );
    }

    private renderAuthors(authors: Author[]) {
        return authors.map((author, index) => {
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

            const link = author._id === this.props.noLinkForAuthorId
                ? <Typography variant="subtitle2" key={author._id}>{name}</Typography>
                : <Link variant="subtitle2" href={'/#/authors/' + author._id} key={author._id}>{name}</Link>;
            
            return index === 0 ? link :
                <React.Fragment key={author._id}>
                    {', '}
                    {link}
                </React.Fragment>;
        });
    }

    private transliterate(name: string): string {
        return new CyrillicToTranslit().transform(name, '_').toLowerCase();
    }
}

export default withStyles(styles)(BookCard);