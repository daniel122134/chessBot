import {YoffeeElement, createYoffeeElement, html} from "../libs/yoffee/yoffee.min.js";
import state, {PAGES} from "./state.js"
import "./mark-down.js"

createYoffeeElement("about-page", class extends YoffeeElement {
    constructor() {
        super({})

        let urlParams = new URLSearchParams(window.location.search);
        let doc = urlParams.get("doc");
        if (doc != null) {
            loop:
            for (let category of state.tree.children) {
                if (category.name === doc) {
                    this.setPage(category)
                    break;
                }
                for (let child of category.children) {
                    if (child.name === doc) {
                        this.setPage(child)
                        break loop;
                    }
                }
            }
        }
    }

    render() {
        return html(this.state, state)`
<style>
    :host {
        position: relative;
        display: flex;
        flex-direction: row;
        height: inherit;
        overflow: hidden;
    }
        
    #side-menu {
        height: -webkit-fill-available;
        display: flex;
        flex-direction: column;
        width: 240px;
        min-width: 240px;
        box-shadow: 0px 3px 3px 0px var(--shadow-color);
        overflow-y: auto;
        overflow-x: hidden;
        padding-top: 30px;
        align-items: baseline;
        font-size: 14px;
    }
    
    #side-menu {
        transition: 400ms;
        margin-left: -240px;
    }
    
    #side-menu[open] {
        transition: 400ms;
        margin-left: 0;
        z-index: 100;
    }
    
    #doc-content {
        width: 100%;
        transition: 400ms;
        opacity: 1;
        padding: 3% 7% 7% 7%;
        overflow-y: auto;
    }
    
    #doc-content[overlayed] {
        transition: 400ms;
        opacity: 0;
    }
    
    @media (max-width: 800px) {
        #side-menu {
            position: absolute;
        }
    }
    
    #next-previous-buttons {
        display: flex;
        font-size: 13px;
        padding-top: 30px;
        justify-content: space-between;
        align-items: center;
    }
    
    #next-previous-buttons > x-button {
        box-shadow: none;
        border: none;
        color: var(--secondary-color);
    }
    
    #next-previous-buttons > #next {
        margin-left: auto;
    }
</style>

<div id="side-menu" open=${() => state.sideMenuOpen}>
    ${() => state.tree.children.map((node, index) => html()`
    <tree-node node=${() => node}
               depth=${0}>           
    </tree-node>
    `)}
</div>


<div id="doc-content" overlayed=${() => state.sideMenuOpen && window.innerWidth < 800}>
    <mark-down markdown=${() => state.selectedNode.doc}></mark-down>
    <div id="next-previous-buttons">
        ${() => state.selectedNode.previous != null &&
            html()`<x-button id="previous" 
                             onclick=${() => this.flipPage(state.selectedNode.previous)}>
                         < ${() => state.selectedNode.previous.name}
                   </x-button>`}        
        ${() => state.selectedNode.next != null && 
            html()`<x-button id="next" 
                             onclick=${() => this.flipPage(state.selectedNode.next)}>
                         ${() => state.selectedNode.next.name} >
                   </x-button>`}
        
    </div> 
</div>
        `
    }

    flipPage(nextPage) {
        this.setPage(nextPage)
        window.history.replaceState(null, null, `?page=${PAGES.about}&doc=${state.selectedNode.name}`);

        this.shadowRoot.querySelector("#doc-content").scrollTop = 0;
    }

    setPage(page) {
        state.selectedNode.isSelected = false;
        page.isSelected = true;
        state.selectedNode = page;
    }
});
