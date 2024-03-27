import React, {useState, useEffect} from 'react';
import Sections from "@/components/headers/Sections";
import Images from "@/image/image";
import Dignity from "@/components/main/sections/About/Dignity";

const About = () => {
    const [windowWidth, setWindowWidth] = useState(window.innerWidth);

    useEffect(() => {
        const handleResize = () => {
            setWindowWidth(window.innerWidth);
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    return (
        <section id="about" className="about__wrap">
            <Sections clarification="ТОП Бекинг Фондов" title="Player’s Reputation"
                      subtitle="Список всех бекинговых фондов СНГ."/>
            <div className="about">
                <p className="about__text">
                    Мы - команда, которая не боится вызовов. Мы помогаем тем, кто нуждается, поднимаем тех, кто
                    упал. Наш фонд - это наш способ сказать миру: "Мы можем быть лучше, вместе мы сила, вместе мы
                    непобедимы".<br/>
                    <br/>
                    Давай вместе растить этот фонд, как настоящую семью. Поддержи нас, и мы сделаем больше, чем ты
                    можешь себе представить. Вместе мы - легион, готовый преодолеть любые препятствия.
                </p>
                <figure>
                    {windowWidth >= 921 ? (
                        <img src={Images.table} alt="table"/>
                    ) : (
                        <img src={Images.table__mobile} alt="table"/>
                    )}
                </figure>
            </div>

            <div className="about__dignity-wrap">
                <Dignity class="about__dignity-box" src={Images.education} alt="education" title="Обучение"
                         text="Все бекинговые фонды заинтересованы в обучении своих игроков"/>
                <div className="bb">
                </div>
                <Dignity class="about__dignity-box" src={Images.becking} alt="becking"
                         title="Бекинг"
                         text="Минимум 50% бекинг, а максимум 80% - все зависит от самого бекингового фонда."/>
                <div className="bb">
                </div>
                <Dignity class="about__dignity-box" src={Images.advantages} alt="advantages" title="Преимущества"
                         text="Вступление в бекинговый фонд дает ряд преимуществ над игроками конкурентами."/>
            </div>
        </section>
    );
};

export default About;