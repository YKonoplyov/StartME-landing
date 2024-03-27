import React, { useState } from 'react';
import Sticky from 'react-sticky-el';
import Navigation from "@/components/header/Navigation";

const Header = () => {
    const [isButtonClicked, setIsButtonClicked] = useState(false);

    const handleButtonClick = () => {
        setIsButtonClicked(prevState => !prevState);
    };

    return (
        <div className={`header__wrap ${isButtonClicked ? 'header__wrap-width' : ''}`}>
            <Sticky topOffset={0} boundaryElement=".header__wrap" stickyStyle={{ top: '8px' }}>
                <header className={`header ${isButtonClicked ? 'header-width' : ''}`}>
                    <Navigation onButtonClick={handleButtonClick} />
                </header>
            </Sticky>
        </div>
    );
};

export default Header;
