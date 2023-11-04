var all_models = document.querySelectorAll('.M')
var all_quantities = document.querySelectorAll('.Q')
var all_prices = document.querySelectorAll('.P')

all_models.forEach((checkbox, index) => {
    checkbox.onchange = function (_) {
        all_quantities[index].required = !all_quantities[index].required
        all_prices[index].required = !all_prices[index].required
    }
});


var search = document.getElementById('look-up')
var models = document.querySelectorAll('.model')

search.addEventListener("keyup", (e) => {
    models.forEach(model => {
        model_code = model.querySelector('.model-code')
        if (model_code.innerText.includes(search.value)) {
            model.style.display = 'flex'
        } else {
            model.style.display = 'none'
        }
    })
});


var select_reservation = document.querySelector('select[name="reservation"]')

if (select_reservation) {
    var filter_inputs = document.querySelectorAll('.filter')
    filter_inputs.forEach(input => {
        if (input.value == select_reservation.value) {
            input.parentElement.style.display = 'flex'
        } else {
            input.parentElement.style.display = 'none'
        }
    })

    select_reservation.addEventListener("change", (e) => {
        filter_inputs.forEach(input => {
            if (input.value == select_reservation.value) {
                input.parentElement.style.display = 'flex'
            } else {
                input.parentElement.style.display = 'none'
            }
        })
    })
}
