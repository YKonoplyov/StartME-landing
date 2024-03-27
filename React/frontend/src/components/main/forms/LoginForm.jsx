import React, { useState, useEffect } from 'react';
import Images from "@/image/image";

const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showFigure, setShowFigure] = useState(window.innerWidth <= 650);

    useEffect(() => {
        const handleResize = () => {
            setShowFigure(window.innerWidth <= 650);
        };

        window.addEventListener('resize', handleResize);
        handleResize();

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Submitted!', email, password);
    };

    return (
        <>
            {showFigure && (
                <figure>
                    <img src={Images.homeBackgroundMobile} alt="homeBackgroundMobile" />
                </figure>
            )}
            <form onSubmit={handleSubmit} className="form">
                <div className="login__title">
                    Войти
                </div>
                <div className="input__wrap">
                    <input
                        className="input"
                        type="text"
                        required
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <label htmlFor="email">
                        Е-мейл
                    </label>
                </div>
                <div className="input__wrap">
                    <input
                        className="input"
                        type="password"
                        required
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <label htmlFor="password">
                        Пароль
                    </label>
                </div>
                <button className="form__btn btn-hover" type="submit">
                    Войти
                </button>
            </form>
        </>
    );
};

export default LoginForm;
