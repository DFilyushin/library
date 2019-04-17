import React, { Component } from 'react';
import Genres from './Genres';
import Authors from './Authors';
import AuthorsLetters from './AuthorsLetters';
import Author from './models/Author';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import './App.css';

interface State {
    letters: string[];
    authors: Author[];
    authorsLoading: boolean;
    typed: string;
}

class App extends Component<{}, State> {
    constructor(props: any) {
        super(props);
        this.state = {
            letters: [],
            authors: [],
            authorsLoading: false,
            typed: ''
        };
    }

    componentWillMount() {
        // mock
        const letters: string[] = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
            'А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ю','Я'];

        this.setState({ 
            letters: letters,
            authors: [],
            typed: ''
        });
    }

    onLetterChange(letter: string) {
        this.setState({
            ...this.state,
            authorsLoading: true
        });
        fetch('http://books.toadstool.online/api/v1/authors/start_with/' + letter + '?limit=10000')
            .then(results => {
                return results.json();
            })
            .then((data: Array<Author>) => {
                this.setState({
                    ...this.state,
                    authors: data,
                    authorsLoading: false,
                    typed: letter
                });
            });
    }

    render() {
        return (
            <div className="App">
                <AppBar position="sticky" color="default">
                    <Toolbar>
                        <Typography variant="h6" color="inherit">
                            <AuthorsLetters letters={this.state.letters} onLetterChange={this.onLetterChange.bind(this)}/>
                        </Typography>
                    </Toolbar>
                </AppBar>
                <table>
                    <thead>
                    <tr>
                        <th>Авторы</th>
                        <th>Жанры</th>
                    </tr>
                    </thead>

                    <tbody>
                    <tr>
                    <td><Authors authors={this.state.authors} typed={this.state.typed}/></td>
                    <td><Genres /></td>
                    </tr>
                    </tbody>
                </table>
            </div>
        );
    }
}

export default App;
