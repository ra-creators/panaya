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
          if (res["status"] == 400) {
            console.error("malformed data");
            return;
          }
          if (res["status"] != 200) return;
          // orderCreated = true;
          console.log(res);
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
    key: "rzp_test_zQH7ZMXqeZqmAK",
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
    callback_url: "/orders/rp_callback",
    prefill: {
      name: "Gaurav Kumar",
      email: "gaurav.kumar@example.com",
      contact: "9999999999",
    },
    notes: {
      address: "Razorpay Corporate Office",
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
