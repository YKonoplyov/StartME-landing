import React from 'react';
import Images from "@/image/image";
import List from "@/components/header/List";

const Navigation = ({onButtonClick}) => {
    return (
        <>
            <nav className="globalnav__wrap">
                <ul className="globalnav__list">
                    <List href="#" class="globalnav globalnav-logo" name={Images.logo} alt="logo" spanClass="globalnav__text" text="Player’s Reputation"/>
                    <List href="home" class="globalnav" name={Images.home} alt="home" spanClass="globalnav__text" text="Главная"/>
                    <List href="about" class="globalnav" name={Images.about} alt="about" spanClass="globalnav__text" text="О нас"/>
                    <List href="about" class="globalnav" name={Images.funds} alt="funds" spanClass="globalnav__text" text="Фонды"/>
                    <List href="contact" class="globalnav" name={Images.trainer} alt="trainer" spanClass="globalnav__text" text="Тренера"/>
                    <List href="#" class="globalnav" name={Images.exit} alt="exit" spanClass="globalnav__text" text="Выйти"/>
                </ul>
            </nav>
            <button className="header__btn" onClick={onButtonClick}></button>
        </>
    );
}

export default Navigation;