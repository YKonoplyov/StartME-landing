import React from 'react';

class FooterNavigation extends React.Component {
    render() {
        const items = this.props.items.map((item, index) => (
            <li key={index}>
                <a href={item.link} className="footer__contact-link">
                    <img src={item.src} alt={item.alt}/>
                    {item.text}
                </a>
            </li>
        ));

        return (
            <nav className="footer__column">
                <ul className={this.props.class}>
                    {items}
                </ul>
            </nav>
        );
    }
}

export default FooterNavigation;