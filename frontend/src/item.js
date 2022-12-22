import {createYoffeeElement, html, YoffeeElement} from "../libs/yoffee/yoffee.min.js";

createYoffeeElement("item-page", class extends YoffeeElement {
    constructor() {
        super({count:1});
    }

    render() {
        return html(this.state, this.props)`
<style>
    .fl{
    flex:1
    }
    button{
    border-radius: 20px;
    border-style: none;
    flex: 1;
    }
    #title {
        padding-bottom: 15px;
    }

    div.gallery {
      margin: 5px;
      border: 1px solid #ccc;
      float: left;
      width: 180px;
        box-shadow: 5px 7px 20px 0px;
    }
    .gl{
          display: flex;
      flex-direction: row;
    }
    
    div.gallery:hover {
      border: 1px solid #777;
    }
    
    div.gallery img {
      width: 100%;
      height: auto;
    }
    
    div.desc {
      padding: 15px;
      text-align: center;
    }
    
    
</style>
 <!-- Image --> 
<div class="gallery">
  <a target="_blank" href=${() => this.props.items.src}>
    <img src=${() => this.props.items.src} width="600" height="400">
  </a>
  <div class="gl">
      <div class="fl"></div>
      <button onclick="${() => this.state.count-=1}">-</button>
      ${() => this.state.count}
      <button onclick="${() => this.state.count+=1}">+</button>
      <div class="fl"></div>
    </div>
</div>


`
    }
});