/* ================= CAROUSAL FUNCTION ================= */
document.addEventListener("DOMContentLoaded", function(){

let slides = document.querySelectorAll(".slide");
let dots = document.querySelectorAll(".dot");

let index = 0;

function showSlide(i){

slides.forEach(slide => slide.classList.remove("active"));
dots.forEach(dot => dot.classList.remove("active"));

slides[i].classList.add("active");
dots[i].classList.add("active");

}

dots.forEach((dot,i)=>{

dot.addEventListener("click",function(){

index = i;
showSlide(index);

});

});


function autoSlide(){

index++;

if(index >= slides.length){
index = 0;
}

showSlide(index);

}

setInterval(autoSlide,5000);

});

/* ================= WISHLIST FUNCTION ================= */

document.addEventListener("DOMContentLoaded", function(){

let hearts = document.querySelectorAll(".heart");

/* get saved wishlist */

let wishlist = JSON.parse(localStorage.getItem("wishlist")) || [];


/* restore saved wishlist */

hearts.forEach((heart, index)=>{

let recipeId = "recipe-" + index;

if(wishlist.includes(recipeId)){

heart.textContent = "❤";
heart.style.color = "#FE4A51";

}

heart.addEventListener("click", function(){

if(wishlist.includes(recipeId)){

/* remove from wishlist */

wishlist = wishlist.filter(item => item !== recipeId);

heart.textContent = "♡";
heart.style.color = "#6B7280";

}else{

/* add to wishlist */

wishlist.push(recipeId);

heart.textContent = "❤";
heart.style.color = "#FE4A51";

}

/* save wishlist */

localStorage.setItem("wishlist", JSON.stringify(wishlist));

});

});

});

/* Search Functionality*/

const input = document.getElementById("searchInput");
const resultsBox = document.getElementById("searchResults");

input.addEventListener("keyup", function(){

    let query = input.value;

    if(query.length === 0){
        resultsBox.style.display = "none";
        return;
    }

    fetch(`/search-api/?q=${query}`)
    .then(res => res.json())
    .then(data => {

        resultsBox.innerHTML = "";

        if(data.results.length > 0){
            resultsBox.style.display = "block";

            data.results.forEach(item => {
            resultsBox.innerHTML += `
        <div class="search-item" onclick="goToBlog('${item.url}')">
            <strong>${item.title}</strong>
            <span class="tag">${item.type}</span>
        </div>
                `;
            });

        } else {
            resultsBox.style.display = "block";
            resultsBox.innerHTML = `<div class="search-item">No results found</div>`;
        }

    });

});

function goToBlog(url){
    window.location.href = url;
}

/* dropdown Functionality*/

const toggleBtn = document.getElementById("dropdownToggle");
const menu = document.getElementById("dropdownMenu");

/* TOGGLE DROPDOWN */
toggleBtn.addEventListener("click", function(e){
    e.stopPropagation();
    menu.classList.toggle("show");
});

/* CLOSE ON CLICK OUTSIDE */
document.addEventListener("click", function(e){
    if (!menu.contains(e.target) && !toggleBtn.contains(e.target)){
        menu.classList.remove("show");
    }
});
