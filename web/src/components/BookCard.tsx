import React, { Component } from 'react';

import {
    Button, Card, CardActionArea, CardActions, CardContent, CardMedia, createStyles, Link, Theme,
    Typography, withStyles, WithStyles
} from '@material-ui/core';

import CyrillicToTranslit from '../../node_modules/cyrillic-to-translit-js/CyrillicToTranslit';
import Endpoints from '../utils/Endpoints';
import Author from '../models/Author';
import Book from '../models/Book';
import Consts from '../utils/Consts';
import AtomicImage from './AtomicImage/AtomicImage';
import Books from './Books';

const styles = (theme: Theme) => createStyles({
    book3d: {
        margin: theme.spacing(2),
    },
    card: {
        display: 'flex',
    },
    details: {
        display: 'flex',
        flexDirection: 'column',
    },
    content: {
        flex: '1 0 auto',
    },
    cardMedia: {
    },
    cover: {
    },
    controls: {
        display: 'flex',
        alignItems: 'center',
        paddingLeft: theme.spacing(1),
        paddingBottom: theme.spacing(1),
    },
    playIcon: {
        height: 38,
        width: 38,
    },
});

interface Prop extends WithStyles<typeof styles> {
    book: Book;
    preview: boolean;
    noLinkForAuthorId?: string;
}

interface State {
    cardHeight: number;
}

class BookCard extends Component<Prop, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            cardHeight: 0
        };
    }

    handleResize = (width: number, height: number) => {
        this.setState({
            cardHeight: height
        });
    }

    render() {
        return this.props.preview
            ? this.renderPreview()
            : this.renderFull();
    }

    private getFirstNameLastName(book: Book): string {
        return book.authors[0].first_name + ' ' + book.authors[0].last_name;
    }

    private renderPreview() {
        const { classes, book } = this.props;
        const { cardHeight } = this.state;

        return (
            <Card className={classes.card} style={{ height: cardHeight }}>
                <div>
                    <a href={Endpoints.getBooksContent(book.id)}>
                    <AtomicImage
                        src={Consts.getCoverImage(book.id)}
                        title={book.name}
                        header={this.getFirstNameLastName(book)}
                        footer={''+book.year}
                        onResize={this.handleResize}
                    />
                    </a>
                </div>
                <CardActionArea href={`/#/books/${book.id}/${this.transliterate(book.name)}`}>
                    <div className={classes.details}>
                        <CardContent className={classes.content}>
                            <Typography component="h5" variant="h5">{book.name}</Typography>
                            {book.series && <Typography variant="subtitle1" color="textSecondary">{book.series}{Number(book.sernum) > 0 && ': ' + book.sernum}</Typography>}
                            {this.renderAuthors(book.authors)}
                            {book.city && <Typography variant="subtitle1" color="textSecondary">{`${book.city}, ${book.publisher}, ${book.year}`}</Typography>}
                        </CardContent>
                    </div>
                </CardActionArea>
            </Card>
        );
    }

    private renderFull() {
        const { classes, book } = this.props;
        const { cardHeight } = this.state;
        return (
            <Card className={classes.card}>
                <div className={classes.book3d}>
                    <AtomicImage
                        src={Consts.getCoverImage(book.id)}
                        title={book.name}
                        header={this.getFirstNameLastName(book)}
                        footer={''+book.year}
                    />
                </div>
                <div className={classes.details}>
                    <CardContent className={classes.content}>
                        <Typography component="h5" variant="h5">{book.name}</Typography>
                        {book.series && <Typography variant="subtitle1" color="textSecondary">{book.series}{Number(book.sernum) > 0 && ': ' + book.sernum}</Typography>}
                        {this.renderAuthors(book.authors)}
                        {book.city && <Typography variant="subtitle1" color="textSecondary">{`${book.city}, ${book.publisher}, ${book.year}`}</Typography>}
                        {book.isbn && <Typography variant="caption">{`ISBN ${book.isbn}`}</Typography>}
                    </CardContent>
                    <CardActions>
                        <Button variant="outlined" color="primary" href={Endpoints.getBooksContent(book.id)}>Скачать FB2</Button>
                    </CardActions>
                </div>
            </Card>
        );
    }

    private renderCover(book: Book): JSX.Element | null {
        return (
            <div className="books">
                <div className="book">
                    <img src={Consts.getCoverImage(book.id)} title={book.name} />
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
                : <Link key={author._id} variant="subtitle2" href={'/#/authors/' + author._id}>{name}</Link>;

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
