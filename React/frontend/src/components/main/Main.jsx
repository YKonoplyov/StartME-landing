import React from 'react';
import Footer from "@/components/footer/Footer";
import Home from "@/components/main/sections/Home/Home";
import About from "@/components/main/sections/About/About";
import Contacts from "@/components/main/sections/Contacts/Contacts";

class Main extends React.Component {
    render() {
        /*const items = [
            { id: 1, title: "Item 1", image: Images.popup__background, param1: "MTT" },
            { id: 2, title: "Item 2", image: "image2.jpg", param1: "Двухуровневые игры" },
            { id: 5, title: "Item 2", image: "image2.jpg", param1: "Двухуровневые игры" },
            { id: 3, title: "Item 3", image: "image3.jpg", param1: "СНГ" },
            { id: 4, title: "Item 4", image: "image4.jpg", param1: "Кэш-игры" },
        ];

        const filterParams = [
            { name: "param1", options: ["Кэш-игры"] },
            { name: "param1", options: ["Двухуровневые игры"] },
            { name: "param1", options: ["MTT"] },
            { name: "param1", options: ["СНГ"] },
        ];

         */

        return (
            <main id="main" className="main">
                <Home />
                <About />
                <Contacts />
                <Footer />
            </main>
        )
    }
}

export default Main