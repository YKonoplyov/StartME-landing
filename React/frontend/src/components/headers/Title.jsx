import React, {useState} from 'react';
import Modal from "@/components/main/modal/Modal";
import LoginForm from "@/components/main/forms/LoginForm";

const Title = () => {
    const [modalActive, setModalActive] = useState(false);

    return (
        <div className="title__wrap">
            <h1>
                Бекинговый фонд
            </h1>
            <p className="title__text">
                Организация, которая предоставляет обучение и финансирование игрокам в покер
            </p>
            <button onClick={() => setModalActive(true)} type="button" className="btn-hover title__btn">
                Войти
            </button>
            <Modal active={modalActive} setActive={setModalActive}>
                <button className="modal__btn-close" onClick={() => setModalActive(false)}>
                </button>
                <LoginForm/>
            </Modal>
        </div>
    );
};

export default Title;