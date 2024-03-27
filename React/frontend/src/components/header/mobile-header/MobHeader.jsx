import React, {useState} from 'react';
import MobHeaderList from "@/components/header/mobile-header/MobHeaderList";
import Images from "@/image/image";

const MobHeader = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => {
        setIsOpen(!isOpen);
    };

    return (<>
        <button type="button" className={`mob-header__btn ${isOpen ? 'open' : ''}`} onClick={toggleMenu}>
                <span className="burger__stick-wrap">
                    <span className="burger__stick-top">
                    </span>
                    <span className="burger__stick">
                    </span>
                    <span className="burger__stick-center">
                    </span>
                    <span className="burger__stick-bottom">
                    </span>
                </span>
        </button>
        <div className={`mob-header__wrap ${isOpen ? 'open' : ''}`}>
            <header className={`mob-header ${isOpen ? 'open' : ''}`}>
                <figure>
                    <img src={Images.homeBackgroundMobile} alt="homeBackgroundMobile"/>
                </figure>
                <MobHeaderList
                    class="footer__contact-list-social footer__contact-list"
                    items={[
                        {link: "home", src: Images.home, alt: "home", text: "Главная"},
                        {link: "#", src: Images.funds, alt: "funds", text: "Фонды"},
                        {link: "contact", src: Images.trainer, alt: "trainer", text: "Тренера"},
                        {link: "about", src: Images.about, alt: "about", text: "О нас"},
                        {link: "#", src: Images.exit, alt: "exit", text: "Войти"},
                    ]}
                />
            </header>
        </div>
    </>);
};

export default MobHeader;