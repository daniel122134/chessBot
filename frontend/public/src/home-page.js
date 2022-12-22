import {YoffeeElement, createYoffeeElement, html} from "../libs/yoffee/yoffee.min.js";
import "./mark-down.js"


const description = `
<b>Daniel Haddad</b> is a young computer engineer and a student.

* Total of 6 years of programing experience in Full Stack software development and data piping system architecture.
* Extensive experience with framework development and distributed systems design.
* Served as an officer at Unit 8200 taking a leading position at a highly intensive environment.  

<br>


`

createYoffeeElement("home-page", class extends YoffeeElement {
    render() {
        return html(this.state)`
<style>
    :host {
        display: flex;
        flex-direction: column;
        height: inherit;
        align-items: center;
        overflow-y: auto;
    }
    
    #title-block-container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 700px;
        padding-top: 100px;
    }
    
    #logo {
        width: 240px;
        padding-right: 40px;
    }
    
    #title-text-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    
    #title-text {
        font-size: 66px;
        font-weight: bold;
        color: var(--secondary-color);
        padding-bottom: 20px;
    }
    
    #title-description {
        font-size: 24px;
        padding-bottom: 28px;
    }
    
    #buttons-container {
        display: flex;    
    }
    
    #get-started-button {
        font-size: 20px;
        padding: 16px 19px;
        background-color: var(--secondary-color);
        margin-right: 20px;
    }
    
    #linkedin-button {
        font-size: 20px;
        padding: 16px 19px;
        background-color: var(--text-color-weak-3);
    }
    
    #linkedin-button > #linkedin-icon {
        margin-left: 10px;
    }
    
    @media (max-width: 800px) {
        #title-block-container {
            flex-direction: column;
            width: 350px;
            padding-top: 50px;
        }
        
        #logo {
            width: 140px;
            padding-right: 0;
            padding-bottom: 20px;
        }
        
        #title-text-container {
            align-items: center;
        }
        
        #title-text {
            font-size: 42px;
        }
        
        #title-description {
            text-align: center;
        }
        
        #buttons-container {
            flex-direction: column;
            align-items: center;
        }
        
        #get-started-button {
            margin-right: 0;
            margin-bottom: 20px;
        }
    }
    
    #description-container {
        display: flex;
        padding: 40px 40px;
        max-width: 800px;
        width: -webkit-fill-available;
    }
    
</style>
<div id="title-block-container">
    <img id="logo" src="res/profile.png"/>
    <div id="title-text-container">
        <div id="title-text">Daniel.H</div>
        <div id="title-description">Software Engeneer at Yahoo, Student at Reichman University</div>
        <div id="buttons-container">
            <x-button id="get-started-button" onclick=${() => () => this.props.getstarted()}>About Daniel</x-button>
            <x-button id="linkedin-button" onclick=${() => () => this.props.linkedin()}>
                LinkedIn
                <x-icon id="linkedin-icon" icon="fab fa-linkedin"></x-icon>
            </x-button>
        </div>
    </div>
</div>
<div id="description-container">
    <mark-down markdown=${() => description}></mark-down>
</div>

        `
    }
});