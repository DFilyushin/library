import React, { Component } from 'react';
import Author from '../models/Author';

interface Props {
    authors: Author[];
    typed: string;
    onAuthorChange: (authorId: string | undefined) => void;
}

interface State {
    selectedAuthorId: string | undefined;
}

export default class Authors extends Component<Props, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            selectedAuthorId: ''
        };
    }

    onAuthorClick(event: any, id: string | undefined) {
        this.setState({
            selectedAuthorId: id
        });
        this.props.onAuthorChange(id);
    }

    render() {
        return (<div>Авторы</div>);
        // return (
        //     <div>
        //         {
        //             this.props.authors.map((author) => {
        //                 return author._id === this.state.selectedAuthorId
        //                     ? <div key={author._id}><b>{author.last_name} {author.first_name}</b></div>
        //                     :<div key={author._id} onClick={this.onAuthorClick.bind(this, event, author.id)}>{author.last_name} {author.first_name}</div>;
        //             })
        //         }
        //     </div>
        // );
    }
}