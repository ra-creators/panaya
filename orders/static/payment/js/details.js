let orderBtn,
  addrInput,
  data = {},
  items;

document.addEventListener("DOMContentLoaded", (e) => {
  orderBtn = document.getElementById("order-btn");
  addrInput = document.getElementById("inputAddress");
  items = document.getElementsByClassName("item");
  if (!orderBtn || !addrInput) {
    console.error("error ", "element not found");
    return;
  }
  orderBtn.addEventListener("click", createOrder);
});

const getItemsData = (items) => {
  let itemsData = [];
  for (let i = 0; i < items.length; i++) {
    datas = items[i].dataset;
    itemsData.push({
      id: datas.id,
      quantity: datas.quantity,
    });
  }
  return itemsData;
};

let createOrder = (e) => {
  e.preventDefault();
  // console.log(e);
  itemsData = getItemsData(items);
  if (itemsData.length < 1) {
    alert("cart empty");
    return;
  }
  data = {
    addrId: addrInput.value,
    items: itemsData,
    requestingUrl: window.location.pathname,
  };
  // console.log(data);
  // return;
  fetch(createOrderUrl, {
    method: "POST",
    cache: "no-cache",
    credentials: "same-origin",
    mode: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    redirect: "follow",
    referrerPolicy: "origin",
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((res) => {
      // console.log(res);
      if (res["status"] != 200) {
        alert(
          "error occured !!\nmake sure cart is not empty or try again after some time"
        );
        console.error("error : ", res.payload);
        return;
      }
      if (res["status"] == 400) {
        console.error("malformed data");
        return;
      }
      localStorage.removeItem("cart_items");
      // orderCreated = true;
      //   console.log(res);
      window.location.href = res.redirect;
      // console.log(data);
    })
    .catch((err) => console.error("cart add error", err));
};
