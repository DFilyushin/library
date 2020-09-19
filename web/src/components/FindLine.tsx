import React, {Component} from 'react';
import Book from '../models/Book';
import {InputBase, Paper, Theme, withStyles} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';

interface Props {
    classes: any;
}

interface State {
    searchText: string;
    onClickFind: any;
    onChangeField: any;
    placeholder: string;
}

const styles = (theme: Theme) => ({
    root: {
        width: '100%',
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
        paddingTop: theme.spacing(5),
    },
    rootPaper: {
        paddingTop: theme.spacing(2),
        paddingRight: theme.spacing(2),
        paddingBottom: theme.spacing(2),
        paddingLeft: theme.spacing(2),
        display: 'flex',
        alignItems: 'center',
        width: '100%',
    },
    inputRoot: {
        color: 'inherit',
        width: '100%',
        backgroundColor: theme.palette.common.white
    },
    inputInput: {
        paddingTop: theme.spacing(1),
        paddingRight: theme.spacing(1),
        paddingBottom: theme.spacing(1),
        paddingLeft: theme.spacing(1),
        width: '100%',
    },
});


class FindLine extends Component<any, State> {

    constructor(props: any) {
        super(props);
        this.state = {
            searchText: props.searchText,
            onClickFind: props.onClickFind,
            onChangeField: props.onChangeField,
            placeholder: props.placeholder
        };
    }

    handleSearchChange = (event: any) => {
        const searchByAuthor = event.target.value;
        this.setState({searchText: event.target.value});
        this.state.onChangeField(event)
    }

    handleClickFindButton = (event: any) => {
        if (event.key === 'Enter') {
            this.state.onClickFind(this.state.searchText);
        }
    }

    render() {
        const {classes} = this.props;
        const {searchText, placeholder, onClickFind, onChangeField} = this.state;

        return (
            <Paper className={classes.rootPaper}>
                <InputBase
                    value={searchText}
                    onChange={this.handleSearchChange}
                    onKeyDown={this.handleClickFindButton}
                    autoFocus
                    placeholder={placeholder}
                    classes={{
                        root: classes.inputRoot,
                        input: classes.inputInput,
                    }}
                />
                <SearchIcon onClick={onClickFind}/>
            </Paper>
        );
    }
}
export default withStyles(styles)(FindLine);
