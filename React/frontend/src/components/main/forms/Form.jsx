import React, {useEffect, useState} from 'react';
import Images from "@/image/image";

const Form = () => {
    const [recommendation, setRecommendation] = useState('');
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [subject, setSubject] = useState('');
    const [message, setMessage] = useState('');
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
        console.log('Submitted!', recommendation, name, email, subject, message);
    };

    return (
        <>
            {showFigure && (
                <figure>
                    <img src={Images.popup__background} alt="popup__background"/>
                </figure>
            )}
            <form onSubmit={handleSubmit} className="form">
                <div className="radio__wrap">
                    <label className="radio">
                        <input
                            type="radio"
                            name="recommendation"
                            value="trainer"
                            checked={recommendation === 'trainer'}
                            onChange={(e) => setRecommendation(e.target.value)}
                        />
                        <span>
                        </span>
                        <p>
                            Порекомендовать тренера
                        </p>
                    </label>
                    <label className="radio">
                        <input
                            type="radio"
                            name="recommendation"
                            value="fund"
                            checked={recommendation === 'fund'}
                            onChange={(e) => setRecommendation(e.target.value)}
                        />
                        <span>
                        </span>
                        <p>
                            Порекомендовать Фонд
                        </p>
                    </label>
                </div>
                <div className="form__contact">
                    <div className="input__wrap">
                        <input
                            className="input"
                            type="text"
                            required
                            id="name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                        <label htmlFor="name">
                            Имя
                        </label>
                    </div>
                    <div className="input__wrap">
                        <input
                            className="input"
                            required
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <label htmlFor="email">
                            Е-мейл
                        </label>
                    </div>
                </div>
                <div className="input__wrap">
                    <input
                        className="input"
                        type="text"
                        required
                        id="subject"
                        value={subject}
                        onChange={(e) => setSubject(e.target.value)}
                    />
                    <label htmlFor="subject">
                        Тема
                    </label>
                </div>
                <div className="input__wrap">
                    <textarea
                        className="input"
                        required
                        id="message"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                    />
                    <label htmlFor="message">
                        Ваше сообщение
                    </label>
                </div>
                <button className="form__btn btn-hover" type="submit">
                    Отправить
                </button>
            </form>
        </>
    );
};

export default Form;
