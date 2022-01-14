class Item {
  constructor(id, name, price, quantity, img) {
    if (typeof id === "object") {
      this.id = id.id;
      this.name = id.name;
      this.price = id.price;
      this.quantity = parseInt(id.quantity, 10);
      this.img = id.img;
    } else {
      this.id = id;
      this.name = name;
      this.price = price;
      this.quantity = parseInt(quantity, 10);
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
  get noItems() {
    return Object.keys(this.items).length;
  }
  constructor(cardDetails = false) {
    this.container = document.getElementById("cart-container");
    this.summaryContainer = document.getElementById("cart-summary-container");
    this.plusItems = document.getElementById("plus-items");
    this.items = {};
    this.savedItems = this.getFromLS();
    this.cardDetails = cardDetails;
    this.addCartUrl = "/cart/add/";
    this.removeCartUrl = "/cart/remove/";
    for (let item in this.savedItems) {
      //   console.log(new Item(this.items[item]));
      // this.items[item] = new Item(this.items[item]);
      // this.addToDom(this.items[item]);
      this.addItem(new Item(this.savedItems[item]));
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
    if (item == null) {
      this.container.innerHTML = `<h4 style="color:white">Cart Empty</h4>`;
      if (this.plusItems) this.plusItems.innerHTML = "";
      return;
    }
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
          <div class="col-2 text-center p_m">
            <span data-id="${item.id}" data-quantity="${item.quantity}" class="minus" onClick="decreaseQuantity(event)">-</span>
            <span class="num">${item.quantity}</span>
            <span data-id="${item.id}" data-quantity="${item.quantity}" class="plus" onClick="increaseQuantity(event)">+</span>
          </div>
          <div class="col-2 text-center c_price">₹ ${item.total}</div>
          <div class="col-2 text-center"><i onClick="cart.removeItem(${item.id})" class="fa fa-trash" aria-hidden="true"></i></i></div>
        </div>`;
      this.summaryContainer.innerHTML += `
        <div class="row" id="item-summary-${item.id}">
          <div class="col-sm-6 i_name"> ${item.name}</div>
          <div class="col-sm-6 i_price">₹ ${item.total}</div>
        </div>
      `;
      return;
    } else {
      this.container.innerHTML = `
      <div class="row" id="item-${item.id}">
        <div class="col-4"><img class="img-fluid" src=${item.img}></img></div>
        <div class="col-auto align-self-center text-white">
          <p class="cross"> <i onClick="removeFromCart(${item.id})" class="fas fa-times-circle"></i></p>
          <h3>${item.name}</h3>
          <h4>Price-${item.price}</h4>
          <h4>Qty-${item.quantity}</h4>
        </div>
        </div>
        `;
      // <div data-targetid=${item.id} onClick="removeFromCart(${item.id})" class="col-auto">
      //   <i onClick="removeFromCart(${item.id})" class="cross fas fa-times-circle"></i>
      // </div>
      if (this.noItems > 1) {
        this.plusItems.innerHTML = "+" + String(this.noItems - 1) + " items.";
      } else {
        this.plusItems.innerHTML = "";
      }
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
    fetch(this.addCartUrl, {
      method: "POST",
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      mode: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "origin", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify(item),
    })
      .then((res) => res.json())
      .then((res) => {
        if (res == 400) {
          console.error("malformed data");
          return;
        }
        if (res != 200) return;
      })
      .catch((err) => console.error("cart add error", err));

    if (item instanceof Item) {
      if (this.items[item.id]) {
        item.quantity += this.items[item.id].quantity;
      }
      this.items[item.id] = item;
      this.save();
      // this.removeFromDom(item.id);
      this.addToDom(item);
    }
  }
  removeItem(id) {
    fetch(this.removeCartUrl, {
      method: "POST",
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      mode: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: "follow", // manual, *follow, error
      referrerPolicy: "origin", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify({ id: id }),
    })
      .then((res) => res.json())
      .then((res) => {
        if (res == 400) {
          console.error("malformed data");
          return;
        }
        if (res != 200) return;
      })
      .catch((err) => console.error("cart add error", err));

    delete this.items[id];
    this.removeFromDom(id);
    let keys = Object.keys(this.items);
    let lastItem = keys.length != 0 ? keys[keys.length - 1] : null;
    if (lastItem) {
      lastItem = this.items[lastItem];
      this.addToDom(lastItem);
    } else this.addToDom(null);
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
  quantity = parseInt(quantity, 10);
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
  //   console.log(newItem);
  cart.addItem(newItem);
};

let removeFromCart = (itemId) => {
  //   console.log(itemId);
  if (itemId) cart.removeItem(itemId);
};

const increaseQuantity = (e) => {
  // console.log("clicked");
  id = e.target.dataset.id;
  oldItem = cart.items[id];
  oldItem.quantity++;
  cart.removeItem(oldItem.id);
  cart.addItem(oldItem);
};
const decreaseQuantity = (e) => {
  // console.log("clicked");
  id = e.target.dataset.id;
  oldItem = cart.items[id];
  oldItem.quantity--;
  cart.removeItem(oldItem.id);
  cart.addItem(oldItem);
};
