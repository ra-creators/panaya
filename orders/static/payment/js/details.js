document.addEventListener("DOMContentLoaded", (e) => {
  let orderBtn = document.getElementById("order-btn");
  orderForm = document.getElementById("order-form");
  if (!(orderBtn && orderForm)) {
    console.error("error ", "element not found");
    return;
  }
  let orderCreated = false;
  let data = {};
  orderBtn.addEventListener("click", (e) => {
    e.preventDefault();
    // console.log(e);
    // console.log(orderForm);
    data = { addrId: e.target.dataset.addrid };
    // console.log(data);
    if (!orderCreated)
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
              "error occured !!, make sure cart no empty or try again after some time"
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
  });
});
