import React, { Component } from 'react';
import Text from './Text';

interface Props {
    src: string;
    title: string;
    header?: string;
    footer?: string;
    onResize?: (width: number, height: number) => void;
}

interface State {
    width?: number;
    height?: number;
    error: boolean;
}

class AtomicImage extends Component<Props, State> {
    defaultWidth: number = 140;
    defaultHeight: number = 200;

    constructor(props: any) {
        super(props);
        this.state = {
            error: false,
        };
    }

    handleLoad = (event: any) => {
        const width = event.target.offsetWidth;
        const height = event.target.offsetHeight;
        this.setState({
            width,
            height,
        });
        if (this.props.onResize) {
            this.props.onResize(width, height);
        }
    }

    handleError = (event: any) => {
        this.setState({
            error: true
        });
        if (this.props.onResize) {
            this.props.onResize(this.defaultWidth, this.defaultHeight);
        }
    }

    render() {
        const { src, title, header, footer } = this.props;
        const { error, width, height } = this.state;

        if (error) {
            return (
                <svg width={this.defaultWidth} height={this.defaultHeight}>
                    <rect width={this.defaultWidth} height={this.defaultHeight} rx={4} style={{ fill: 'lightgray', strokeWidth: 1, stroke: 'rgb(0,0,0)' }} />
                    {header &&
                        <Text x={this.defaultWidth / 2} y="2em" width={this.defaultWidth} textAnchor="middle" style={{ fontSize: 'small' }}>
                            {header}
                        </Text>
                    }
                    <Text x={this.defaultWidth / 2} y="5em" width={this.defaultWidth} textAnchor="middle" style={{ fontSize: 'large' }}>
                        {title}
                    </Text>
                    {footer &&
                        <Text x={this.defaultWidth / 2} y="14em" width={this.defaultWidth} textAnchor="middle" style={{ fontSize: 'small' }}>
                            {footer}
                        </Text>
                    }
                </svg>
            );
        }

        return (
            <img onLoad={this.handleLoad} onError={this.handleError} style={{ width, height }} src={src} title={title} />
        );
    }
}

export default AtomicImage;
