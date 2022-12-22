import {YoffeeElement, createYoffeeElement, html} from "../libs/yoffee/yoffee.min.js";
import "./components/x-button.js"
import "./components/x-icon.js"
import state, {PAGES} from "./state.js";

createYoffeeElement("tree-node", class extends YoffeeElement {
    render() {
        return html(this.props.node, this.state)`
<style>
    :host {
        display: flex;
        flex-direction: column;
        align-items: baseline;
        justify-content: center;
        width: 100%;
    }
    
    #node-title {
        user-select: none;
        display: flex;
        align-items: center;
        border-radius: 0;
        box-shadow: none;
        width: -webkit-fill-available;
        justify-content: flex-start;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: ${() => this.props.depth * 15 + 10}px;
        /*font-weight: ${() => this.props.node.isSelected ? "bold" : "normal"};*/
        color: ${() => this.props.node.isSelected ? "var(--secondary-color)" : "inherit"};
        cursor: pointer;
    }
    
    #node-title:hover {
        background-color: var(--hover-color);
    }
    
    #name {
        --background-color: #00000000;
        --padding: 0;
        font-size: inherit;
        width: -webkit-fill-available;
        min-width: 0;
        margin-right: 6px;
        margin-left: 6px;
    }
    
    #open-icon {
        color: var(--text-color-weak-2);
        width: 20px;
        min-width: 20px;
        height: 20px;
        font-size: 10px;
    }
    
    #open-icon[rotated] {
        transform: rotate(90deg);
    }
    
    #children {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
</style>

<!--We use different style tag because the whole tag is overwritten when changing childs length-->
<style>
    #open-icon {
        visibility: ${() => this.props.node.children.length === 0 ? "hidden" : "inherit"};
    }
</style>

<style>    
    #node-title {
        border-left: 3px solid ${() => this.props.node.isSelected ? "var(--secondary-color)" : "#00000000"};
    }
</style>

<div id="node-title" onclick=${() => {
            if (this.props.node.children.length > 0) {
                this.props.node.opened = !this.props.node.opened
            }
            
            if (this.props.node.children.length === 0) {
                state.selectedNode.isSelected = false;
                this.props.node.isSelected = true;
                state.selectedNode = this.props.node;
                window.history.replaceState(null, null, `?page=${PAGES.about}&doc=${state.selectedNode.name}`);
                
                if (window.innerWidth < 800) {
                    state.sideMenuOpen = false;
                }
            }
        }}>
    <x-icon id="open-icon" 
            icon="fas fa-chevron-right"
            rotated=${() => this.props.node.opened}></x-icon>    
    <div id="name">${() => this.props.node.name}</div>
</div>

${() => this.props.node.opened && html()`
<div id="children">
    ${() => this.props.node.children.map((child, index) => html()`
        <tree-node node=${() => child}
                   depth=${() => parseInt(this.props.depth) + 1}></tree-node>
    `)}
</div>
`}
`
    }
});