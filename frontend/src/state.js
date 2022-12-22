import Childhood from "./docs/life/00_Childhood.js";
import Mechina from "./docs/life/01_Mechina.js";
import IDF from "./docs/life/02_IDF.js";
import Work from "./docs/life/03_employment.js";
import Snow from "./docs/hobbies/Snow.js";

import Acro from "./docs/hobbies/Acro.js";


const PAGES = {
    home: "home",
    about: "about",
    vote: "vote",
    contact: "contact",
}

let state = {
    darkTheme: true,
    sideMenuOpen: window.innerWidth > 800,
    selectedNode: null,
    tree: {
        name: "ROOT",
        children: [{
            name: "Life",
            opened: true,
            children: [{
                name: "about Daniel",
                children: [],
                isSelected: true,
                doc: Childhood,
            }, {
                name: "Education",
                children: [],
                doc: Mechina
            }, {
                name: "IDF service - 8200",
                children: [],
                doc: IDF
            },
            {
                name: "Employment",
                children: [],
                doc: Work
            },

            ]
        },
        {
            name: "Hobbies",
            children: [
                {
                name: "Acrobatics",
                children: [],
                doc: Acro
            },
            {
                name: "Snowboarding",
                children: [],
                doc: Snow
            }, 
            ]
        },
        ]
    }
};
state.tree.children.forEach(
    (category, catIndex) => category.children.forEach(
        (n, index) => {
            n.previous = state.tree.children[catIndex].children[index - 1]
            n.next = state.tree.children[catIndex].children[index + 1]
        }
    )
)



state.selectedNode = state.tree.children[0].children[0]

export default state;
export {PAGES}