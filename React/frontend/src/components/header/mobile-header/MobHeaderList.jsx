import React from 'react';
import {Link} from "react-scroll"

class MobHeaderList extends React.Component {
    render() {
        const handleSetActive = (to) => {
            console.log(to);
        };

        const items = this.props.items.map((item, index) => (
            <li key={index}>
                <Link
                    className="mob-header-link"
                    to={item.link}
                    spy={true}
                    smooth={true}
                    offset={0}
                    duration={0}
                    onSetActive={handleSetActive}
                >
                    <img src={item.src} alt={item.alt}/>
                    <p>
                        {item.text}
                    </p>
                </Link>
            </li>
        ));

        return (
            <nav className="mob-header__column">
                <ul className="mob-header__list">
                    {items}
                </ul>
            </nav>
        );
    }
}

export default MobHeaderList;