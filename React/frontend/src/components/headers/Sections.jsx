import React from 'react';

class Sections extends React.Component {
    render() {
        return (
            <div className="subtitle__wrap">
                <span className="subtitle__clarification">
                    {this.props.clarification}
                </span>
                <h2>
                    {this.props.title}
                </h2>
                <h3>
                    {this.props.subtitle}
                </h3>
            </div>
        )
    }
}

export default Sections