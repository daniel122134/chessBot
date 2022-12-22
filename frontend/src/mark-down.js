import {YoffeeElement, createYoffeeElement, html} from "../libs/yoffee/yoffee.min.js";
import state from "./state.js"

customElements.define("mark-down", class extends YoffeeElement {
    render() {
        //language=HTML
        return html(this.props)`
            <link rel="stylesheet" href="./libs/highlight/${() => state.darkTheme ? "highlight-darcula.css" : "highlight-light.css"}">
            <style>
                :host {
                    overflow: hidden
                }
                
                h1 {
                    border-bottom: 1px solid #8080808c;
                    padding-bottom: 5px;
                    padding-top: 20px;
                }
                
                a {
                    color: var(--secondary-color) !important;
                }
                
                code {
                    font-size: 18px;
                }
                
                li + li {
                    margin-top: 10px;
                }

                p > code {
                    font-size: 16px;
                    background: #00000028;
                    border-radius: 5px;
                    padding: 0px 4px;
                    opacity: 0.8;
                }

                @media (max-width: 800px) {
                    code {
                        font-size: 13px;
                    }
                }
            </style>
            ${() => {
                let converter = new showdown.Converter({
                    extensions: [showdownHighlight({
                        // Whether to add the classes to the <pre> tag
                        pre: true
                    })]
                });
                let md = this.props.markdown;
                // Change theme of JSFiddle iframe
                if (!state.darkTheme) {
                    md = md.replaceAll("embedded/html,result/dark/", "embedded/html,result/light/")
                }
                let html = converter.makeHtml(md);
                let element = document.createElement("mark-down-content");
                element.innerHTML = html
                return element
            }}
        `
    }
});