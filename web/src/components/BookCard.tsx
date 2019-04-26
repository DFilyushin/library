import React, { Component } from "react";
import { Card, CardContent, Typography, Link, CardActions, Button, withStyles, CardActionArea, CardMedia } from "@material-ui/core";
import Book from "../models/Book";
import Endpoints from "../Endpoints";
import FB2Info from "../models/FB2Info";
import Author from "../models/Author";
import CyrillicToTranslit from "../../node_modules/cyrillic-to-translit-js/CyrillicToTranslit";

interface Prop {
    classes: any;
    book: Book;
    preview: boolean;
    noLinkForAuthorId: string;
}

interface State {
    info: FB2Info;
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
                .then((data: FB2Info) => {
                    this.setState({
                        info: data
                    })
                })
                .catch(() => {
                    this.setState({
                        info: {}
                    });
                });
        }
    }

    componentWillUnmount() {
        this.abortController.abort();
    }

    render() {
        return this.props.preview
            ? this.renderPreview()
            : this.renderFull();
    }

    private renderPreview() {
        const { classes, book } = this.props;
        const { info } = this.state;
        return (
            <Card className={classes.card}>
                <CardActionArea href={`/#/books/${book.id}/${this.transliterate(book.name)}`}>
                <CardContent className={classes.content}>
                    {info && info.cover && <img style={styles.preview} src={`data:${info.coverType};base64, ${info.cover}`} title={book.name} />}
                    <Typography component="h5" variant="h5">{book.name}</Typography>
                    {book.series && <Typography variant="subtitle1" color="textSecondary">{book.series}{Number(book.sernum) > 0 && ': ' + book.sernum}</Typography>}
                    {this.renderAuthors(book.authors)}
                    {info && info.city && <Typography variant="subtitle1" color="textSecondary">{`${info.city}, ${info.publisher}, ${info.year}`}</Typography>}
                </CardContent>
                </CardActionArea>
            </Card>
        );
    }

    private renderFull() {
        const { classes, book } = this.props;
        const { info } = this.state;
        return (
            <Card className={classes.card}>
                <CardContent>
                    {info && info.cover && <img style={styles.preview} src={`data:${info.coverType};base64, ${info.cover}`} title={book.name} />}
                    <Typography component="h5" variant="h5">{book.name}</Typography>
                    {book.series && <Typography variant="subtitle1" color="textSecondary">{book.series}{Number(book.sernum) > 0 && ': ' + book.sernum}</Typography>}
                    {this.renderAuthors(book.authors)}
                    {info && info.city && <Typography variant="subtitle1" color="textSecondary">{`${info.city}, ${info.publisher}, ${info.year}`}</Typography>}
                    {info && info.isbn && <Typography variant="caption">{`ISBN ${info.isbn}`}</Typography>}
                </CardContent>
                <CardActions>
                    <Button href={Endpoints.getBooksContent(book.id)}>Скачать FB2</Button>
                </CardActions>
            </Card>
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