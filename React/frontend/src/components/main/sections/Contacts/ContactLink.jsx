import React, {useState} from 'react';
import Modal from "@/components/main/modal/Modal";
import Sections from "@/components/headers/Sections";
import Form from "@/components/main/forms/Form";


const ContactLink = (props) => {
    const [modalActive, setModalActive] = useState(false);

    return (
        <div className="contact">
            <div className="contact__text-wrap">
                <p className="contact__title">
                    {props.title}
                </p>
                <p className="contact__text">
                    {props.text}
                </p>
            </div>
            <button onClick={() => setModalActive(true)} type="button" className="contact__btn btn-hover">
                {props.textbtn}
            </button>
            <Modal active={modalActive} setActive={setModalActive}>
                <button className="modal__btn-close" onClick={() => setModalActive(false)}>
                </button>
                <Sections clarification="Вам есть что сказать?" title="Давайте пообщяемся" subtitle="Заполните форму и мы это обсудим"/>
                <Form />
            </Modal>
        </div>
    );
};

export default ContactLink