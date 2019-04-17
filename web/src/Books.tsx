import React, { Component } from 'react';
import Book from './models/Book';
import './Books.css';

interface Props {
    books: Book[];
}

export default class Books extends Component<Props, {}> {
    constructor(props: any) {
        super(props);
    }

    render() {
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