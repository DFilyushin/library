import React, { Component } from 'react';
import Genre from './models/Genre';
import './Genres.css';

interface IGenresState {
    genres: Genre[];
    selected: string | undefined;
}

class Genres extends Component<{}, IGenresState> {
    constructor(props: any) {
        super(props);
        this.state = {
            genres: [],
            selected: ''
        };
    }

    componentDidMount() {
        fetch('http://books.toadstool.online/api/v1/genres')
        .then(results => {
            return results.json();
        })
        .then((data: Array<Genre>) => {

            let sorted = data.sort((a, b) => {
                if (a.name! < b.name!) {
                    return -1;
                }
                if (a.name! > b.name!) {
                    return 1;
                }
                return 0;
            });

            this.setState({
                genres: sorted,
                selected: sorted[0].slug
            });
        });
    }

    selectAuthor(event: any, slug: string | undefined) {
        this.setState({
            ...this.state,
            selected: slug
        })
    }

    render() {
        return (
            <div>
                {
                    this.state.genres.map((g) => {
                        return g.slug === this.state.selected
                        ? (
                            <div key={g.id}>
                                <b>{g.name}</b>
                            </div>
                        )
                        : (
                            <div key={g.id} onClick={this.selectAuthor.bind(this, event, g.slug)}>
                                {g.name}
                            </div>
                        );
                    })
                }
            </div>
        );
    }
}

export default Genres;