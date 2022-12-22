import {YoffeeElement, createYoffeeElement, html} from "../libs/yoffee/yoffee.min.js";
import state, {PAGES} from "./state.js"
import "./mark-down.js"

createYoffeeElement("closet-page", class extends YoffeeElement {
    constructor() {
        super({items: []})

        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: {}

        };
        fetch('/getPicks', requestOptions)
            .then(response => response.json())
            .then(data => {
                for (const item of data.data){
                    
                    item[0].src=item[0].image
                    item[1].src=item[1].image
                }
                this.state.items = data.data
            });

    }

    render() {
        return html(this.state)`
<style>
    .all{
    flex-direction: row;
    display: flex;
    }   
    .pick{
    flex-direction: column;
    display: flex;
    }
    :host {
        display: flex;
        flex-direction: column;
        height: inherit;
        padding: 20px 4%;
    }
    
    #title {
        padding-bottom: 15px;
    }
    
    #persuation-text {
        margin-bottom: 20px;
    }
    
    
    #contributors-title {
        padding-top: 20px;
        padding-bottom: 10px;
    }
    #projects{
        flexDirection: column;
        display : flex;
    }
    .project{
        flex: 1;
        margin: 10px;
    }
    
    img{
    width: 400px;
    height: 400px;
    margin: 50px;
    }
    #code{
    width: 600px;
    margin-left: 10px;
    }
    #cocktail{
        width: 250px;
        height: 180px;
        margin: 0px;
    }
    #barbot{
        width: 150px;
        height: 200px;
        margin: 0px;
    }
    
    
    
</style>

<h1 id="title">Your Daily Suggestions</h1>

<div class="all">
    ${() => this.state.items.map(item => html()`
    <div class="pick">
    <item-page items=${() => item[0]}>
    </item-page>
    <item-page items=${() => item[1]}>
    </item-page>
    </div>
    `)}
</div>
`

    }
});