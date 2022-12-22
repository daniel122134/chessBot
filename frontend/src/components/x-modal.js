import {html, createYoffeeElement, YoffeeElement} from "../../libs/yoffee/yoffee.min.js";


const openModal = (content, onClose, {closeOnFocus} = {closeOnFocus: true}) => {
    let modal = document.createElement("x-modal")
    modal.appendChild(content)
    document.body.appendChild(modal)

    let closeEvent = e => {
        if (!modal.contains(e.target)) {
            modal.remove()
            document.removeEventListener("click", closeEvent)
            onClose && onClose(e)

        }
    }

    if (closeOnFocus) {
        requestAnimationFrame(() => document.addEventListener(
            "click",
            closeEvent,
            {
                capture: false
            }
        ))
    }

    modal.style.left = window.innerWidth / 2 - modal.getBoundingClientRect().width / 2 + "px"
    modal.close = () => {
        modal.remove()
        document.removeEventListener("click", closeEvent)
        onClose && onClose()
    }
    return modal
}

export {openModal}

createYoffeeElement("x-modal", class extends YoffeeElement {
    render() {
        return html(this.state)`
<style>
    :host {
        position: fixed;
        top: ${() => window.innerHeight / 5}px;
        left: ${() => window.innerWidth - 150}px;
        max-height: ${() => Math.floor(window.innerHeight * 0.7)}px;
        display: flex;
        flex-direction: column;
        z-index: 1;
        background-color: #222222;
        border-radius: 4px;
        box-shadow: 1px 1px 5px 0px #000000c2;
        color: #bbbbbb;
        overflow: auto;
    }
    
</style>
<slot
    
></slot>
`
    }
});