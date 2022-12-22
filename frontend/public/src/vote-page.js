import {createYoffeeElement, html, YoffeeElement} from "../libs/yoffee/yoffee.min.js";

createYoffeeElement("vote-page", class extends YoffeeElement {
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
<h1 id="title">Voting for projects is not yet open</h1>
<div id="persuation-text">
   Daniel loves building DIY projects and cool apps with his friend david.
   Until we open voting to the public here are some of our previous projects for you to enjoy :) 
    
</div>

<div id="projects">

    <div id="barbot" class="project">
        <h2 >Barbot</h2>
        Barbot is a one of a kind cocktail maker we built! 
        built out of wood and empowered with a raspberry-pie inside, Barbot makes any cocktail you can think of
        on its admin page you configure on which tube you installed which drink and Barbot takes care of the rest
        it will calculate which drinks are available for your choices and pour you some into your glass in no time :)
        <br>

       <img id="barbot" src="res/Barbot.jpeg" />
       <img id="cocktail" src="res/cocktail.png" />
    </div>
    
    <div id="codenames" class="project">
        <h2 >CodeNames App</h2>
        During covid querntine we got a little bored and decided to develope an <a href="https://namecoding.herokuapp.com/" target="_blank">App</a>  for our beloved codename board game. 
        this we thought would enable us to play toghether online with our friends! after a weekof intense work we realeased our game,
        codename was a sensation and above 150,000 game sessions took place over the course of the different lockdowns in israel
               <br>

        <img id="code" src="res/code.png" />
    </div>
    
    <div id="chess" class="project">
        <h2 >Wizards Chess</h2>
        this poject is still a WIP, we intend to build a wizerd's chess set, controlled by voice commands and controlled with an electromagnet.
        we still have to build a chess engine for move calculations and gameplay and our mechanical parts are still on their way to israel.
        additinaly we might build a little web GUI.
        <br>
        <img id="harry" src="res/harry.jpg" />
    </div>
</div>
`
    }
});