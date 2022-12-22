import {html, YoffeeElement} from "../libs/yoffee/yoffee.min.js";
import "../src/components/x-icon.js"

customElements.define("splash-page", class extends YoffeeElement {
    constructor() {
        super({
            pressedStart: false
        });
    }

    render() {
        return html(this.state)`
        <style>
            :host {
                background-color: #ca3071;
                color: white;
                display: flex;
                font-size: 36px;
                align-items: center;
                justify-content: center;
                height: inherit;
                width: 100%;
                margin-left: 0%;
                position: fixed;
                z-index: 2;
            }
            
            #logo {
                font-size: 80px;
                padding-bottom: 20px;
            }
            
            #loading {
                font-size: 50px;
                -webkit-animation: rotating 2s linear infinite;
                margin-top: 50px;
                min-height: 55px;
            }
            
            @-webkit-keyframes rotating {
               from{
                   -webkit-transform: rotate(0deg);
               }
               to{
                   -webkit-transform: rotate(360deg);
               }
            }
            
            #start-button {
                margin-top: 50px;
                background-color: #ffffff40;
                font-size: 30px;
            }
        </style>
        
        ${() => this.state.sliding && html()`
        <style>
            :host {
                margin-left: 100%;
                transition: 500ms;
            }
        </style>
        `}
        
        <div id="container">
            <x-icon id="logo" icon="fas fa-tshirt"></x-icon>
            <div style="display: flex;justify-content: center;">WARDROBE.IO</div>
            ${() => this.state.pressedStart ? 
            html()`<x-icon id="loading" icon="fas fa-spinner"></x-icon>` 
            : 
            html()`<x-button id="start-button"
                             onclick=${() => () => this.startCamera()}
                             >
                             Take a Selfie
                   </x-button>`
        }
        </div>
        `
    }

    startCamera() {
        this.state.pressedStart = true;
        this.props.onstartcamera()
        setTimeout(() => {
            this.state.sliding = true;
            this.props.onstartfinish()
            setTimeout(() => {
                this.props.onfinish()
            }, 500)
        }, 1500)
    }
})