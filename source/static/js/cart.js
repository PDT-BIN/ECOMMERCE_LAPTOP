var changeAddress = document.querySelectorAll("button.changeAddress");
var address = document.querySelectorAll("div.address");
var changeAddressBtn = document.querySelectorAll("button.changeAddressBtn");
var addressModal = document.getElementById('myAddressModal');
/* ADDRESS INFORMATION */
let fullname_input = document.querySelector('input[name="fullname"]')
let phone_input = document.querySelector('input[name="phone"]')
let address_input = document.querySelector('input[name="address"]')

changeAddress.forEach(function (button) {
    button.addEventListener("click", function (event) {
        event.preventDefault();
        addressModal.style.visibility = "visible";
    });
});

changeAddressBtn.forEach(function (button) {
    button.addEventListener("click", function (event) {
        event.preventDefault();
        /* ASSIGN CUSTOMER ADDRESS TO ORDER ADDRESS */
        fullname_input.value = button.parentElement.querySelector('.fullname').innerText
        phone_input.value = button.parentElement.querySelector('.phone').innerText
        address_input.value = button.parentElement.querySelector('.address').innerText

        addressModal.style.visibility = "hidden"
    });
});

function getParent(element, selector) {
    while (element.parentElement) {
        if (element.parentElement.matches(selector)) {
            return element.parentElement;
        }
        element = element.parentElement;
    }

}

window.addEventListener("click", function (event) {
    if (event.target == addressModal || event.target == closeButton) {
        addressModal.style.visibility = "hidden";
    }
});