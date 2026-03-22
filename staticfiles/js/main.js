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