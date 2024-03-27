import React from 'react';
import {Link} from "react-scroll"

class List extends React.Component {


    render() {

        const handleSetActive = (to) => {
            console.log(to);
        };

        return (
            <li className={this.props.class}>
                <Link
                    className="globalnav__link"
                    to={this.props.href}
                    spy={true}
                    smooth={true}
                    offset={0}
                    duration={0}
                    onSetActive={handleSetActive}
                >
                    <img src={this.props.name} alt={this.props.alt}/>
                    <span className={this.props.spanClass}>
                        {this.props.text}
                    </span>
                </Link>
            </li>
        )
    }
}

export default List