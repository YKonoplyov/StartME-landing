import React from 'react';

class Dignity extends React.Component {
    render() {
        return (
            <div className={this.props.class}>
                <div className="about__dignity-title-wrap">
                    <img src={this.props.src} alt={this.props.alt} />
                    <span className="about__dignity-title">
                        {this.props.title}
                    </span>
                </div>
                <p className="">
                    {this.props.text}
                </p>
            </div>
        )
    }
}

export default Dignity