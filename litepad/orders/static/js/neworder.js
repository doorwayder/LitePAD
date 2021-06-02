"use strict";

$(document).ready(function () {
    let categories = document.querySelectorAll(".btn.category");
    let products = document.querySelectorAll(".btn.product");
    Array.from(categories).forEach(function (button_cat) {
        button_cat.addEventListener('click', function (e) {
            $(".product").hide();
            $("." + e.target.id).show();
        });
    });
    Array.from(products).forEach(function (button_prod) {
        button_prod.addEventListener('click', function (e) {
            e.preventDefault();
            addToCart(e.target.id, e.target.innerText, e.target.getAttribute("data-price"));
        });
    });
    document.getElementById("cat-1").click();
});

function discount(d){
    let discount = document.getElementById("discount");
    let input_discount = document.getElementById("id_discount")
    discount.innerText = d + " %";
    discount.setAttribute("data-discount", d);
    input_discount.value = d;
    $("#discount").popover("hide");
    updateCost();
}

function addToCart(id, good, price){
    let added = false;
    const cart = document.querySelectorAll(".trprod");
    const order_input = document.querySelectorAll(".order_input");
    if (cart.length===0) addCartRow(id, good, price);
    else {
        Array.from(cart).forEach(function (item) {
            if (item.querySelector(".tdid").innerText===id) {
                let counttd = item.querySelector(".prodcount");
                counttd.innerText = parseInt(counttd.innerText)+1;
                added=true;
            }
        });
        Array.from(order_input).forEach(function (item) {
            if (item.getAttribute("name") === id) item.setAttribute("value", +item.getAttribute("value")+1)
        });
        if (!added) addCartRow(id, good, price);
    }
    updateCost();
}

function addCartRow(id, good, price) {
    const tbody = document.getElementById("cart").getElementsByTagName("tbody")[0];
    const form = document.getElementById("mainform");
    const input = document.createElement("input");
    input.setAttribute("name", id);
    input.setAttribute("type", "hidden");
    input.setAttribute("value", "1");
    input.className = "order_input";
    let row = document.createElement("tr");
    row.className = "trprod";
    row.setAttribute("data-id", id);
    let td1 = document.createElement("td");
    td1.className = "tdid";
    let td2 = document.createElement("td");
    td2.className = "tdmain prodname";
    let td3 = document.createElement("td");
    td3.className = "tdprice prodprice";
    let td4 = document.createElement("td");
    td4.className = "tdmain prodcount";
    td1.appendChild(document.createTextNode(id));
    td2.appendChild(document.createTextNode(good));
    td3.appendChild(document.createTextNode(price));
    td4.appendChild(document.createTextNode("1"));
    row.appendChild(td1);
    row.appendChild(td2);
    row.appendChild(td3);
    row.appendChild(td4);
    tbody.appendChild(row);
    form.appendChild(input);
}

function clearCart() {
    const table = document.getElementById("cart");
    const order_input = document.querySelectorAll(".order_input");
    order_input.forEach(function (elem) {
        elem.parentNode.removeChild(elem);
    });
    while(table.rows.length > 0) {
        table.deleteRow(0);
    }
    updateCost();
}

function updateCost() {
    let input_cost = document.getElementById("id_cost")
    let cost = document.getElementById("cost");
    let items = document.querySelectorAll(".trprod");
    let discount = parseInt(document.getElementById("discount").innerText);
    let coef = (100-discount)/100;
    if (items.length===0) {
        cost.setAttribute("data-cost", 0);
        cost.innerText = "К оплате: 0";
        input_cost.value = 0;
    }
    else{
        let sum = 0;
        items.forEach(item => {
            let price = +item.querySelector(".prodprice").innerText;
            let count = +item.querySelector(".prodcount").innerText;
            sum += price*count;
        });
         sum *= coef;
        cost.setAttribute("data-cost", sum);
        cost.innerText = "К оплате: " + sum;
        input_cost.value = sum;
    }
}

function pay_type_change() {
    if (document.getElementById("id_pay_type").checked) $("#pay_type_label").text("Нал.");
    else $("#pay_type_label").text("Безнал.");
}