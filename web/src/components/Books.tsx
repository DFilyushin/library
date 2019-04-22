import React, { Component } from 'react';
import Book from '../models/Book';

interface Props {
    books: Book[];
}

export default class Books extends Component<Props, {}> {
    constructor(props: any) {
        super(props);
    }

    render() {
        return (<div>Книги</div>);
        return (
            <div>
            {
                this.props.books.map(b => {
                    return <div key={b.filename}>{b.name}</div>
                })
            }
            </div>
        )
    }
}