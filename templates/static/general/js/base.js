let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let searchBtn = document.querySelector(".bx-search");

closeBtn.addEventListener("click", ()=>{
    sidebar.classList.toggle("open");
    menuBtnChange();
});

searchBtn.addEventListener("click", ()=>{ 
    sidebar.classList.toggle("open");
    menuBtnChange();
});

function menuBtnChange() {
if(sidebar.classList.contains("open")){
    closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
}else {
    closeBtn.classList.replace("bx-menu-alt-right","bx-menu");
}
}


// Espera 5 segundos e remove as mensagens
setTimeout(() => {
    const messageBox = document.querySelector('.messages');
    if (messageBox) {
        messageBox.style.transition = 'opacity 1s ease-out';
        messageBox.style.opacity = '0';
        setTimeout(() => messageBox.remove(), 1000); // Remove do DOM após 1 segundo
    }
}, 5000);