import {createYoffeeElement, html, YoffeeElement} from "../libs/yoffee/yoffee.min.js";

createYoffeeElement("dress-page", class extends YoffeeElement {
    constructor() {
        super({items: []})

        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: {}
            
        };
        fetch('/getWardrobe', requestOptions)
            .then(response => response.json())
            .then(data => {
                for (const item of data.data){
                    item.src=item.image
                }
                this.state.items = data.data
            });
        
    }

    render() {
        return html(this.state)`
<style>
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

<h1 id="title">Viewing cloths</h1>

<div>
    ${() => this.state.items.map(item => html()`
    <item-page items=${() => item}>
    </item-page>
    `)}
</div>
`

    }
});