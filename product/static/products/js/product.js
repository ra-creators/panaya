// select image to view
let setActiveProductImg = (e)=>{
    selectedLink = e.target.getAttribute('src')
    // console.log( selectedLink)
    targetElement = document.getElementById('active-product-img')
    // console.log(targetElement)
    targetElement.setAttribute('src', selectedLink)
    selectImg = e.target.parentElement
    // console.log(selectImg)
    activeImg = targetElement.parentElement
    // console.log(activeImg)
    selectImg.style.height = targetElement.parentElement.offsetHeight+"px"
  }
  window.addEventListener('DOMContentLoaded', (event) => {
    selectImg = document.getElementById('select-img-container')
    targetElement = document.getElementById('active-product-img')
    selectImg.style.height = targetElement.offsetHeight+"px"
  });

// #info change tab
function changeTab(event) {
    // console.log(event);
    // var i;
    var x = document.getElementsByClassName("tab");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
      // console.log(x[i].classList);
    }
    x = document.getElementsByClassName("tab-parent");
    for (i = 0; i < x.length; i++) {
      x[i].classList.remove("active");
    }
    let target = event.target;
    let tabName = event.target.dataset.target;
    document.getElementById(tabName).style.display = "flex";
    target.classList.add("active");
  }
