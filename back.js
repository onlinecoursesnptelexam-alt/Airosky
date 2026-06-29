const topBtn = document.getElementById("topBtn");

window.addEventListener("scroll",()=>{

    if(window.scrollY > 300){

        topBtn.style.display = "block";

    }else{

        topBtn.style.display = "none";
    }

});

topBtn.addEventListener("click",()=>{

    window.scrollTo({

        top:0,
        behavior:"smooth"

    });

});

const popup = document.getElementById("popup");

const openPopup = document.getElementById("openPopup");

const closePopup = document.getElementById("closePopup");

openPopup.onclick = () => {

    popup.classList.add("active");

}

closePopup.onclick = () => {

    popup.classList.remove("active");

}

popup.onclick = (e)=>{

    if(e.target===popup){

        popup.classList.remove("active");

    }

}

document.addEventListener("keydown",(e)=>{

    if(e.key==="Escape"){

        popup.classList.remove("active");

    }

});

const mobileOverlay = document.getElementById("mobileOverlay");

const menuOpen = document.getElementById("menuOpen");

const menuClose = document.getElementById("menuClose");

menuOpen.addEventListener("click", () => {

    mobileOverlay.classList.add("active");
    document.body.classList.add("no-scroll");

});

menuClose.addEventListener("click", () => {

    mobileOverlay.classList.remove("active");
    document.body.classList.remove("no-scroll");

});

mobileOverlay.addEventListener("click", (e) => {

    if (e.target === mobileOverlay) {

        mobileOverlay.classList.remove("active");
        document.body.classList.remove("no-scroll");

    }

});

// Close after clicking any menu link

document.querySelectorAll(".mobile-nav a").forEach(link => {

    link.addEventListener("click", () => {

        mobileOverlay.classList.remove("active");
        document.body.classList.remove("no-scroll");

    });

});

// Close with Escape key

document.addEventListener("keydown", (e) => {

    if (e.key === "Escape") {

        mobileOverlay.classList.remove("active");
        document.body.classList.remove("no-scroll");

    }

});