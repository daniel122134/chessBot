import {createYoffeeElement, html, YoffeeElement} from "../libs/yoffee/yoffee.min.js";
import "./mark-down.js"

const bishop = "♜";
const knight = "♞";
const rook = "♝";
const queen = "♛";
const king = "♚";
const pawn = "♟";
let i = false;

window.state = {
    data: [[{"color": "black", "type": bishop}, {"color": "black", "type": knight}, {"color": "black", "type": rook}, {"color": "black", "type": queen}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}, {}, {}, {}],
        [{}, {}, {}, {}, {}, {}, {}, {}]
    ]
}



createYoffeeElement("home-page", class extends YoffeeElement {
    constructor() {
        super({});
        setInterval(this.updateBoard,500);
        this.randomMove()    
    }
    
    randomMove(){
        fetch('http://localhost/random')
            .then(response => response.json())
            .then(data => { 
                console.log(data);
                setTimeout(() => { this.randomMove(); }, 1);
            });
    }
    updateBoard(){
        fetch('http://localhost/board')
            .then(response => response.json())
            .then(data => {                state.data = data.data;
            });
    }
    render() {
        
        return html(this.state, state)`
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
        

    }
  
    
    .chess-board { border-spacing: 0; border-collapse: collapse;color: black }
    .chess-board td:last-child { border-right: 1px solid #000; }
    .chess-board tr:last-child td { border-bottom: 1px solid; }
    .chess-board th:empty { border: none; }
    .chess-board td { width: 1.5em; height: 1.5em; text-align: center; font-size: 32px; line-height: 0;}
    .chess-board .light { background: #eee; }
    .chess-board .dark { background: #aaa; }

    .table {
          display: flex;
          flex-direction: column;
          }
    .row {
          display: flex;
          flex-direction: row;
          }
          
    .header {
            font-weight: bold;
          }
          
    .cell {
        font-size: 66px;
        text-align: center;
        width: 100px;
        height: 100px;
          }
          
</style>
        
        <div class="table">
          
            ${() => state.data.map(row => html({"row": row})
            `
           
                    ${() => this.get_row(row)}
           
            `
        )}
            
        </div>
   
    
</script>


<i-am-table></i-am-table>



        `
    }

    get_cell(cell) {
        i = !i;
        let color = "#4e4e4e";
        if (i % 2 === 0) {
            color = "#b5b5b5"
        }
        return html({"cell": cell})`<div class="cell" style="color: ${cell.color}; background-color: ${color}">
                    ${() => cell.type}
                </div>   `
    }

    get_row(row) {
        i = !i;

        return html({"row": row})`<div class="row">
            ${() => row.map(cell => html({"cell": cell})
            `    
                ${() => this.get_cell(cell)}
            `
        )}
        </div> `
    }

});


