import React from 'react';
import FooterNavigation from "@/components/footer/FooterNavigation";
import Images from "@/image/image";

class Footer extends React.Component {
    render() {
        return (
            <footer className="footer">
                <FooterNavigation
                    class="footer__contact-list"
                    items={[
                        {
                            link: "mailto:exfundcorp@gmail.com",
                            src: Images.mail,
                            alt: "mail",
                            text: "exfundcorp@gmail.com"
                        },
                        {link: "tel:+380 63 157 7418", src: Images.phone, alt: "phone", text: "+380 63 157 7418"},
                    ]}
                />
                <FooterNavigation
                    class="footer__contact-list-social footer__contact-list"
                    items={[
                        {link: "#", src: Images.instagram, alt: "instagram", text: ""},
                        {link: "#", src: Images.vk, alt: "vk", text: ""},
                        {link: "#", src: Images.telegram, alt: "telegram", text: ""},
                        {link: "#", src: Images.youtube, alt: "youtube", text: ""},
                        {link: "#", src: Images.discord, alt: "discord", text: ""},
                        {link: "#", src: Images.twitch, alt: "twitch", text: ""},
                    ]}
                />
                <div className="footer__text">
                    <p>
                        ©2024 Player’s Reputation
                    </p>
                    <p>
                        Powered by FlexFrame
                    </p>
                </div>
            </footer>
        );
    }
}

export default Footer;