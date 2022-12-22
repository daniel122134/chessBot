import {createYoffeeElement, html, YoffeeElement} from "../libs/yoffee/yoffee.min.js";
import "./components/text-input.js"

createYoffeeElement("contact-page", class extends YoffeeElement {
    render() {
        return html(this.state)`
<style>
    :host {
        flex-direction: column;
        height: inherit;
        padding: 40px 12%;
    }
    
    #title {
        padding-bottom: 15px;
    }
  
  
    #form{
        flex-direction: column;
        display : flex;
    }
    .field{
        flex-direction: row;
        display : flex;
        margin: 10px;
    }
    text-input{
        background-color: var(--text-color-weak-1);
    }
    .desc{
        flex: 1;
    }
    .margin{
    flex:3;
    }
  
    x-button {
        width: 100px;
        height: 40px;
        box-shadow: none;
        border: none;
        color: var(--text-color);
        background-color: var(--secondary-color);
    }
    
    
</style>




<h1 id="title">Contact Me</h1>
<div id="text">
   Hi there, 
   If you wish to contact me please fill in the following form :)
</div>

<br>
<div id="form">

<div class="field">
<div class="desc">First Name:</div>
<text-input  id="first-name"></text-input>
<div class="margin"></div>
</div>


<div class="field">
<div class="desc">Last Name:</div>
<text-input id="last-name"></text-input>
<div class="margin"></div>

</div>

<div class="field">
<div class="desc">Phone Number:</div>
<text-input id="phone" name="Phone number"></text-input>
<div class="margin"></div>
</div>



</div>
<x-button type="button" onclick=${() => () => this.validateAndSend()}>Send!</x-button>





`

        
    }

    validateAndSend() {
        let re = new RegExp('^05[0-9]{8}$');
        let phone = this.shadowRoot.querySelector("#phone").getValue()
        let res = re.exec(phone);
        let first = this.shadowRoot.querySelector("#first-name").getValue()
        let last = this.shadowRoot.querySelector("#last-name").getValue()
        if (res == null || first ==null || last==null){
            alert("form is invalid!,please verify your phone is a correct israeli number and that your full name is present")
        }else{
            window.open(`mailto:dhaddad96@gmail.com?subject=${first}%20${last}%20wants%20to%20connect&body=%0D%0D%0Dsincerely yours,%0D${first}%20${last}%0D${phone}`);
        }
        
    }
});