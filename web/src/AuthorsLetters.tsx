import React, { Component } from 'react';
import './AuthorsLetters.css';

interface Props {
    letters: string[],
    onLetterChange: (letter: string) => void;
}

interface State {
    selectedLetter: string;
}

export default class AuthorsLetters extends Component<Props, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            selectedLetter: ''
        };
     }

    componentDidMount() {
        this.setState({
            selectedLetter: this.props.letters[0]
        });
        this.props.onLetterChange(this.props.letters[0]);
    }

    onLetterClick(event: any, letter: string) {
        this.setState({
            selectedLetter: letter
        });
        this.props.onLetterChange(letter);
    }

    render() {
        return (
            <div>
                {
                    this.props.letters.map((letter) => {
                        return letter === this.state.selectedLetter
                            ? (<span key={letter} className="selected">{letter}</span>)
                            : (<span key={letter} onClick={this.onLetterClick.bind(this, event, letter)}>{letter}</span>);
                    })
                }
            </div>
        );
    }
}
