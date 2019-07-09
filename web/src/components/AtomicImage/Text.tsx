import React, { Component } from 'react';

interface State {
    lines: string[];
}

interface IWord {
    word: string;
    words: string[];
    width: number;
}

class Text extends Component<any, State> {
    static defaultProps = {
      lineHeight: 1,
      capHeight: 0.71,
    };

    wordsWithComputedWidth: IWord[] = [];
    spaceWidth: number = 0;

    constructor(props: any) {
      super(props);

      this.state = {
        lines: []
      };
    }

    componentWillMount() {
        const { wordsWithComputedWidth, spaceWidth } = this.calculateWordWidths();
        this.wordsWithComputedWidth = wordsWithComputedWidth;
        this.spaceWidth = spaceWidth;

        const lines = this.calculateLines(this.wordsWithComputedWidth, this.spaceWidth, this.props.width);
        this.setState({ lines });
    }

    render() {
        // TODO: determine lineHeight and dy dynamically (using passed in props)
        const { lineHeight, capHeight, ...props } = this.props;
        const dy = capHeight;
        const { x, y } = props;

        return (
            <text {...props} dy={`${dy}em`}>
                {this.state.lines.map((word, index) => (
                    <tspan key={index} x={x} y={y} dy={`${index * lineHeight}em`}>
                        {word}
                    </tspan>
                ))}
            </text>
        );
    }

    componentDidUpdate(nextProps: any, nextState: any) {
        if (this.props.children !== nextProps.children) {
            const { wordsWithComputedWidth, spaceWidth } = this.calculateWordWidths();
            this.wordsWithComputedWidth = wordsWithComputedWidth;
            this.spaceWidth = spaceWidth;
        }

        const lines = this.calculateLines(this.wordsWithComputedWidth, this.spaceWidth, this.props.width);
        const newLineAdded = this.state.lines.length !== lines.length;
        const wordMoved = this.state.lines.some((line, index) => line.length !== lines[index].length);
        // Only update if number of lines or length of any lines change
        if (newLineAdded || wordMoved) {
            this.setState({ lines });
        }
    }

    calculateWordWidths() {
        // Calculate length of each word to be used to determine number of words per line
        const words = (this.props.children as string)!.split(/\s+/);
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        Object.assign(text.style, this.props.style);
        svg.appendChild(text);
        document.body.appendChild(svg);

        const wordsWithComputedWidth = words.map(word => {
            text.textContent = word;
            return { word, words: [], width: text.getComputedTextLength() };
        });

        text.textContent = '\u00A0'; // Unicode space
        const spaceWidth = text.getComputedTextLength();

        document.body.removeChild(svg);

        return { wordsWithComputedWidth, spaceWidth };
    }

    calculateLines(wordsWithComputedWidth: IWord[], spaceWidth: number, lineWidth: number) {
        const wordsByLines = wordsWithComputedWidth.reduce<IWord[]>((result, { word, width }) => {
            const lastLine = result[result.length - 1] || { words: [], width: 0 };

            if (lastLine.words.length === 0) {
                // First word on line
                const newLine: IWord = { word: '', words: [word], width };
                result.push(newLine);
            } else if (lastLine.width + width + (lastLine.words.length * spaceWidth) < lineWidth) {
                // Word can be added to an existing line
                lastLine.words.push(word);
                lastLine.width += width;
            } else {
                // Word too long to fit on existing line
                const newLine = { word: '', words: [word], width };
                result.push(newLine);
            }

            return result;
        }, []);

        return wordsByLines.map((line: any) => line.words.join(' '));
    }
}

export default Text;
