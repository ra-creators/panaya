document.addEventListener("DOMContentLoaded", (e) => {
  let orderBtn = document.getElementById("order-btn");
  if (!orderBtn) {
    console.error("error ", "element not found");
    return;
  }
  let orderCreated = false;
  let data = {};
  orderBtn.addEventListener("click", (e) => {
    e.preventDefault();
    // console.log(e);
    data = { addrId: e.target.dataset.addrid };
    // console.log(data);
    if (!orderCreated)
      fetch(window.location.href, {
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
          // if (res["status"] == 400) {
          //   console.error("malformed data");
          //   return;
          // }
          // orderCreated = true;
          // console.log(res);
          data = res["rapay_data"];
          // console.log(data);
          razor_pay_init(data);
        })
        .catch((err) => console.error("cart add error", err));
  });
});

const razor_pay_init = (data) => {
  console.log(data);
  var options = {
    key: data["key"],
    amount: data["amount"],
    currency: data["currency"],
    name: data["name"],
    description: data["description"],
    // image: data["image"],
    order_id: data["order_id"],
    // handler: function (response) {
    //   payment = {}
    //   payment['payment_id'] = (response.razorpay_payment_id);
    //   payment['order_id'] = (response.razorpay_order_id);
    //   payment['signature'] = (response.razorpay_signature);
    // },
    callback_url: redirectUrl,
    notes: {
      address: "Panaya.in ",
    },
    theme: {
      color: "#8d0020",
    },
  };
  var rzp1 = new Razorpay(options);
  // rzp1.on("payment.failed", function (response) {
  //   alert(response.error.code);
  //   alert(response.error.description);
  //   alert(response.error.source);
  //   alert(response.error.step);
  //   alert(response.error.reason);
  //   alert(response.error.metadata.order_id);
  //   alert(response.error.metadata.payment_id);
  // });
  rzp1.open();
};
