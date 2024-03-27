import React, {useEffect, useState} from 'react';
import Title from "@/components/headers/Title";
import Images from "@/image/image";


const Home = () => {
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
        <section id="home" className="home__wrap">
            <figure>
                {windowWidth >= 801 ? (
                    <img src={Images.homeBackground} className="firstImage" alt="background"/>
                ) : (

                    <img src={Images.homeBackgroundMobile} className="secondIMage" alt="background"/>
                )}
            </figure>
            <Title/>
        </section>
    );
};

export default Home