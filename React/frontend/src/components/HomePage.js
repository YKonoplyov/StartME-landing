import React, {useEffect, useState} from 'react';
import '@styles/index.scss';
import Header from "@/components/header/Header";
import Main from "@/components/main/Main";
import MobHeader from "@/components/header/mobile-header/MobHeader";

function HomePage() {
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
        <div className="App">
            {windowWidth >= 801 ? (
                <Header/>
            ) : (
                <MobHeader />
            )}
            <Main />
        </div>
    );
}

export default HomePage;
