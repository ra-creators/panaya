class Item {
  constructor(id, name, price, quantity, img) {
    if (typeof id === "object") {
      this.id = id.id;
      this.name = id.name;
      this.price = id.price;
      this.quantity = id.quantity;
      this.img = id.img;
    } else {
      this.id = id;
      this.name = name;
      this.price = price;
      this.quantity = quantity;
      this.img = img;
    }
  }
  get total() {
    return parseInt(this.price, 10) * parseInt(this.quantity, 10);
  }
}

class Cart {
  getFromLS() {
    let raw_data = localStorage.getItem("cart_items");
    if (raw_data) return JSON.parse(raw_data);
    return {};
  }
  constructor(cardDetails = false) {
    this.container = document.getElementById("cart-container");
    this.summaryContainer = document.getElementById("cart-summary-container");
    this.items = this.getFromLS();
    this.cardDetails = cardDetails;
    for (let item in this.items) {
      //   console.log(new Item(this.items[item]));
      this.items[item] = new Item(this.items[item]);
      this.addToDom(this.items[item]);
    }
    this.save();
  }
  save() {
    // console.log(this.items);
    let cartTotal = document.getElementById("cart-total");
    // console.log(cartTotal);
    cartTotal.innerHTML = `Rs. ${this.total}`;
    localStorage.setItem("cart_items", JSON.stringify(this.items));
  }
  addToDom(item) {
    // console.log(item);
    if (this.cardDetails) {
      this.container.innerHTML += `
        <div class="row align-items-center" id="item-${item.id}">
          <div class="col-6">
            <div class="row mt-3 desc_box">
              <div class="col-sm-4">
                  <img class="img-fluid" src="${item.img}" alt="product">
              </div>
              <div class="col-sm-8 align-self-center">
                <div class="name">${item.name}</div>
                <div class="price">Price ₹ ${item.price}</div>
                <div>Size - 2 L</div>
              </div>
            </div>
          </div>
          <div class="col-2 text-center p_m"><span class="minus">-</span><span class="num">${item.quantity}</span><span class="plus">+</span></div>
          <div class="col-2 text-center c_price">₹ ${item.total}</div>
          <div class="col-2 text-center"><i onClick="cart.removeItem(${item.id})" class="fa fa-trash" aria-hidden="true"></i></i></div>
        </div>`;
      this.summaryContainer.innerHTML += `
        <div class="row mt-5" id="item-summary-${item.id}">
          <div class="col-sm-6 i_name"> ${item.name}</div>
          <div class="col-sm-6 i_price">₹ ${item.total}</div>
        </div>
      `;
      return;
    } else {
      this.container.innerHTML += `
      <div class="row" id="item-${item.id}">
        <div class="col-4"><img class="img-fluid" src=${item.img}></img></div>
        <div class="col-6 align-self-center text-white">
          <h1>${item.name}</h1>
          <h3>Price-${item.price}</h3>
          <h3>Qty-${item.quantity}</h3>
        </div>
        <div data-targetid=${item.id} onClick="removeFromCart(event)" class="col-2 cross">X</div>
      </div>
      `;
    }
  }
  removeFromDom(item_id) {
    let elm = document.getElementById(`item-${item_id}`);
    if (elm) elm.remove();
    if (this.cardDetails) {
      let elm = document.getElementById(`item-summary-${item_id}`);
      if (elm) elm.remove();
    }
  }
  addItem(item) {
    if (item instanceof Item) {
      this.items[item.id] = item;
      this.save();
      this.removeFromDom(item.id);
      this.addToDom(item);
    }
  }
  removeItem(id) {
    delete this.items[id];
    this.removeFromDom(id);
    this.save();
  }
  get total() {
    let total = 0;
    for (let item in this.items) {
      total += parseInt(this.items[item].total, 10);
      //   console.log(total);
    }
    return total;
  }
}
let cart;

let addToCart = (e) => {
  //   console.log(e.target.dataset);
  dataset = e.target.dataset;
  stock = dataset.stock;
  quantity = document.getElementById("quantity").value;
  if (stock < quantity) {
    alert("stock limited");
    return;
  }
  newItem = new Item(
    dataset.id,
    dataset.name,
    dataset.price,
    quantity,
    dataset.img
  );
  if (quantity == 0) {
    cart.removeItem(newItem.id);
    return;
  }
  //   console.log(newItem);
  cart.addItem(newItem);
};

let removeFromCart = (event) => {
  let itemId = event.target.dataset.targetid;
  //   console.log(itemId);
  if (itemId) cart.removeItem(itemId);
};
