import React, { Component } from 'react';
import Genre from './models/Genre';

interface IGenreState {
    genres: JSX.Element[];
}

class Genres extends Component<{}, IGenreState> {
    constructor() {
        super({});
        this.state = {
            genres: []
        };
    }

    componentDidMount() {
        debugger;
        fetch('http://books.toadstool.online/api/v1/genres')
        .then(results => {
            return results.json();
        })
        .then((data: Array<Genre>) => {
            let gen = data.map((g) => {
                return (
                    <div key={g.id}>
                        {React.createElement('a', { href:'#' + g.slug }, g.name)}
                    </div>
                )
            });
            let newState: IGenreState = {
                genres: gen
            };
            this.setState(newState);
            //console.log("state", this.state.genres);
        });
    }

    render() {
        return (
            <div>
                {this.state.genres}
            </div>
        );
    }
}

export default Genres;