import {html, YoffeeElement} from "../libs/yoffee/yoffee.min.js";
import state, {PAGES} from "./state.js"
import "./tree-node.js"
import "./components/x-button.js"
import "./components/text-input.js"
import "./components/x-switch.js"
import "./components/x-icon.js"
import "./home-page.js"
import "./about-page.js"
import "./vote-page.js"
import "./contact-page.js"


customElements.define("daniel-hw-app", class extends YoffeeElement {
    constructor() {
        let urlParams = new URLSearchParams(window.location.search);
        let page = urlParams.get("page");

        super({
            currentPage: page || PAGES.home
        })
    }

    render() {
        return html(this.props, this.state, state.tree, state)`
<style>
    :host {
        display: flex;
        flex-direction: column;
        height: inherit;
    }
    
    #header {
        width: -webkit-fill-available;
        display: flex;
        padding: 10px 21px;
        align-items: center;
        max-height: 44px;
        box-shadow: 0px 0px 3px 0px var(--shadow-color);
        user-select: none; 
    }
    
    #logo {
        display: flex;
        width: 36px;
        height: 36px;
        cursor: pointer;
    }
    
    #title {
        font-size: 22px;
        padding-left: 10px;
        cursor: pointer;
    }
    
    #header > .header-button {
        transition: 300ms;
        color: var(--text-color);
        cursor: pointer;
        padding: 19px 10px;
        margin: 0px 10px;
        font-size: 18px;
        border-bottom: 3px solid #00000000;
    }
    
    #header > .header-button[highlight] {
        border-bottom-color: var(--secondary-color);
        color: var(--secondary-color);
    }
    
    #header > .header-button:hover {
        transition: 300ms;
        color: var(--secondary-color);
    }
    
    #vote-button {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }
    
    #about-button {
        margin-left: auto !important;
    }
    
    #github-button {
        display: flex;
    }
    
    #github-button > x-icon {
        margin-left: 7px;
    }
    
    #dark-theme-toggle {
        --circle-size: 20px;
    }
    
    #slide-menu-button {
        display: none;
    }
    
    @media (max-width: 800px) {
        #header {
            max-height: 26px;
        }
        
        #header > .header-button {
            font-size: 14px;
            padding: 13px 10px;
        }
        
        #github-button, #title {
            display: none;
        }
    }
</style>

<style>
    @media (max-width: 800px) {
        #logo {
            margin-left: ${() => this.state.currentPage === PAGES.about ? "20px" : "0"};
            margin-right: 10px;
            width: 28px;
            height: 28px;
        }
        
        #slide-menu-button {
            display: ${() => this.state.currentPage === PAGES.about ? "flex" : "none"};
        }
    }
</style>

<div id="header">
    <x-icon id="slide-menu-button" icon="fas fa-bars"
            onclick=${() => () => state.sideMenuOpen = !state.sideMenuOpen}></x-icon>
    <img id="logo" src="res/profile.png" onclick=${() => () => this.switchPage(PAGES.home)} />
    <div id="title" onclick=${() => () => this.switchPage(PAGES.home)}>Daniel Haddad</div>
    
    <div id="about-button" class="header-button" 
         highlight=${() => this.state.currentPage === PAGES.about}
         onclick=${() => () => this.switchPage(PAGES.about)}>
        About Daniel
    </div>
    <div id="vote-button" class="header-button" 
         highlight=${() => this.state.currentPage === PAGES.vote}
         onclick=${() => () => this.switchPage(PAGES.vote)}>
        Vote for projects ♥
    </div>
    <div id="contact-button" class="header-button" 
         highlight=${() => this.state.currentPage === PAGES.contact}
         onclick=${() => () => this.switchPage(PAGES.contact)}>
        Contact Me
    </div>
    <div id="github-button" class="header-button" 
         onclick=${() => () => this.openLinkedin()}>
        LinkedIn
        <x-icon icon="fab fa-linkedin"></x-icon>
    </div>
    <x-switch id="dark-theme-toggle" 
              value=${() => state.darkTheme}
              switched=${() => () => {
            state.darkTheme = !state.darkTheme;
            document.body.setAttribute("theme", state.darkTheme ? "dark" : "light")
        }}></x-switch>
</div>

${() => {
            if (this.state.currentPage === PAGES.home) {
                return html()`<home-page getstarted=${() => () => this.switchPage(PAGES.about)}
                                      github=${() => () => this.openLinkedin()}></home-page>`
            } else if (this.state.currentPage === PAGES.about) {
                return html()`<about-page></about-page>`
            } else if (this.state.currentPage === PAGES.vote) {
                return html()`<vote-page></vote-page>`
            } else if (this.state.currentPage === PAGES.contact) {
                return html()`<contact-page></contact-page>`
            }
        }}

`
    }

    switchPage(page) {
        window.history.replaceState(null, null, `?page=${page}`);
        this.state.currentPage = page;
    }

    openLinkedin() {
        window.open("https://www.linkedin.com/in/daniel-haddad-927a9699", "_blank")
    }
});