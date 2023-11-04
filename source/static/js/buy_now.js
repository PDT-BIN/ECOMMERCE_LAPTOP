var buy_now = document.querySelectorAll(".btn_buy");
var img_product = document.getElementById('img_pro');
var name_product = document.getElementById('name_product');
var price_product = document.getElementById('price_product');
var screen_product = document.getElementById('scr_pro');
var cpu_product = document.getElementById('cpu_pro');
var card_product = document.getElementById('card_pro');
var ram_product = document.getElementById('ram_pro');
var disk_product = document.getElementById('disk_pro');
var weight_product = document.getElementById('weight_pro');


var closeButton = document.getElementById("closeModal");
var modal = document.getElementById('myModal');

var dropdownProv = document.getElementById("dropdownProv");
var dropdownWard = document.getElementById("dropdownWard");
var dropdownDis = document.getElementById("dropdownDistr");


var apart_input = document.getElementById('apart_input');
var btn_confirm = document.getElementById('confirm');
var radio = document.querySelectorAll('input[name="radio_add"]');
var name_take = document.getElementById('name_take');
var number_take = document.getElementById('number_take');

var box_select_ad = document.getElementById('box-select_ad');
var bg_deli = document.getElementById('bg_add');
let selectedPro = 92;
var disUrl = "https://vapi.vnappmob.com/api/province/district/" + selectedPro;
var selectedDis = 925;
var wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + selectedDis;
var selectedWard;
var provIndex = -1, disIndex = -1, wardIndex = -1;

//Select address modal
var select_address = document.getElementById('select_else');
var addressModal = document.getElementById('myAddressModal');
var close_modal_select = document.getElementById('btn_close_select');
var choose_address = document.querySelectorAll('.changeAddressBtn');

let deli_add;
let name_input = null, phone_input = null, apartment, name_contact, number_contact;
document.addEventListener("DOMContentLoaded", function () {
    loadDropdownDataProv(); // Gọi hàm để tải dữ liệu vào dropdownProv khi trang đã sẵn sàng
    loadDropdownDataDis();
    loadDropdownDataWard();
    var label = document.querySelector('label[for="radio_id"]');
    if (label) {
        name_contact = label.querySelector("#lb_name").textContent;
        number_contact = label.querySelector("#lb_phone").textContent;
        deli_add = label.querySelector("#lb_add").textContent;
    }
});

name_take.addEventListener("input", function () {
    name_input = name_take.value;
});

number_take.addEventListener("input", function () {
    phone_input = number_take.value;
});

apart_input.addEventListener("input", function () {
    apartment = apart_input.value;
});

radio.forEach(function (radioButton) {
    if (radioButton !== null) {
        radioButton.addEventListener('change', function () {
            if (radioButton.value == 'choose') {
                bg_deli.classList.add("hidden");
                if (box_select_ad.classList.contains('opacity-40')) {
                    box_select_ad.classList.remove('opacity-40');
                }
                select_address.disabled = false;
                dropdownProv.disabled = true;
                dropdownDis.disabled = true;
                dropdownWard.disabled = true;
                apart_input.disabled = true;
                name_take.disabled = true;
                number_take.disabled = true;
                box_select_ad.classList.remove("hidden");
                var label = document.querySelector('label[for="radio_id"]');
                if (label) {
                    name_contact = label.querySelector("#lb_name").textContent;
                    number_contact = label.querySelector("#lb_phone").textContent;
                    deli_add = label.querySelector("#lb_add").textContent;
                }
            }
            else {
                dropdownProv.disabled = false;
                dropdownDis.disabled = false;
                dropdownWard.disabled = false;
                apart_input.disabled = false;
                name_take.disabled = false;
                number_take.disabled = false;
                //select_address.disabled = true;
                name_input = null;
                phone_input = null;
                apartment = null;
                name_take.value = number_take.value = apart_input.value = '';
                bg_deli.classList.remove("hidden");
                box_select_ad.classList.add("hidden");
                //box_select_ad.classList.add('opacity-40');
            }
        });
    }
});

buy_now.forEach(function (button) {
    button.addEventListener("click", function (event) {
        event.preventDefault(); // Ngăn chặn hành vi mặc định của liên kết
        var old_parent = button.parentElement.parentElement;
        // console.log(old_parent.querySelector('h2').innerText);
        img_product.src = old_parent.querySelector("img").src;
        var list_spe = button.parentElement.querySelectorAll("span");
        screen_product.innerText = list_spe[4].textContent;
        name_product.innerText = button.parentElement.querySelector('h2').innerText;
        ram_product.innerText = list_spe[1].textContent;
        cpu_product.innerText = list_spe[0].textContent;
        disk_product.innerText = list_spe[2].textContent;
        price_product.innerText = button.parentElement.querySelector('a').innerText;
        // dropdownProv.selectedIndex = 0;
        // dropdownDis.selectedIndex = 0;
        // dropdownWard.selectedIndex = 0;
        var idModel = button.parentElement.querySelector("#idModel")
        var lapModal = document.getElementById("lapModel")
        lapModal.value = idModel.value
        modal.style.visibility = "visible";
        if (box_select_ad.classList.contains('opacity-40')) {
            box_select_ad.classList.remove('opacity-40');
        }
    });
});

choose_address.forEach(function (button) {
    button.addEventListener("click", function (event) {
        event.preventDefault(); // Ngăn chặn hành vi mặc định của liên kết
        let parent = button.parentElement;
        let name = parent.querySelector('#name_deli');
        let phone = parent.querySelector('#phone_contact');
        let address = parent.querySelector('#address_deli');
        name_contact = name.textContent;
        number_contact = phone.textContent;
        deli_add = address.textContent;
        var label = document.querySelector('label[for="radio_id"]');
        if (label) {
            var lb_1 = label.querySelector("#lb_name");
            var lb_2 = label.querySelector("#lb_phone");
            var lb_3 = label.querySelector("#lb_add");
            lb_1.textContent = name_contact;
            lb_2.textContent = number_contact;
            lb_3.textContent = deli_add;
        }
        addressModal.style.visibility = 'hidden';
        modal.style.visibility = "visible";
    });
});

document.addEventListener("DOMContentLoaded", function () {
    if (closeButton) {
        closeButton.addEventListener("click", function (event) {
            event.preventDefault(); // Ngăn chặn hành vi mặc định của liên kết
            // Thêm hành động tùy chỉnh ở đây, ví dụ: mở một hộp thoại mua hàng, thực hiện AJAX request, vv.
            modal.style.visibility = "hidden";
            // modal.innerHTML = initialState;
        });
    }
});

window.addEventListener("click", function (event) {
    if (event.target == modal || event.target == closeButton) {
        modal.style.visibility = "hidden";
        var radio_id = document.getElementById('radio_id');
        radio_id.checked = true;
        var label = document.querySelector('label[for="radio_id"]');
        bg_deli.classList.add('hidden');
        dropdownProv.disabled = true;
        dropdownDis.disabled = true;
        dropdownWard.disabled = true;
        apart_input.disabled = true;
        name_take.disabled = true;
        number_take.disabled = true;
        select_address.disabled = false;
        if (label) {
            name_contact = label.querySelector("#lb_name").textContent;
            number_contact = label.querySelector("#ln_phone").textContent;
            deli_add = label.querySelector("#lb_add").textContent;
        }
        box_select_ad.classList.toggle('opacity-40');
    }
});
window.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        modal.style.visibility = "hidden";
        var radio_id = document.getElementById('radio_id');
        radio_id.checked = true;
        var label = document.querySelector('label[for="radio_id"]');
        bg_deli.classList.add('hidden');
        dropdownProv.disabled = true;
        dropdownDis.disabled = true;
        dropdownWard.disabled = true;
        apart_input.disabled = true;
        name_take.disabled = true;
        number_take.disabled = true;
        select_address.disabled = false;
        if (label) {
            name_contact = label.querySelector("#lb_name").textContent;
            number_contact = label.querySelector("#ln_phone").textContent;
            deli_add = label.querySelector("#lb_add").textContent;
        }
        box_select_ad.classList.toggle('opacity-40');
    }
});

// dropdownProv.addEventListener("click", function (event) {
//     selectedPro = dropdownProv.value;
//     // console.log(selectedValue);
//     disUrl = "https://vapi.vnappmob.com/api/province/district/" + selectedPro;
//     loadDropdownDataDis();
//     selectedDis = dropdownDis.firstElementChild;
//     // console.log(dropdownDis.options[dropdownDis.selectedIndex]);
//     if (selectedDis == null) {
//         dropdownWard.innerHTML = '';
//     }
//     else {
//         wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + selectedDis;
//         loadDropdownDataWard();
//     }
//     // provIndex = dropdownProv.selectedIndex;
//     // disIndex = dropdownDis.selectedIndex = 0;
//     // wardIndex = dropdownWard.selectedIndex = -1;
// });

dropdownProv.addEventListener("change", function (event) {
    selectedPro = dropdownProv.value;
    // console.log(selectedPro);
    disUrl = "https://vapi.vnappmob.com/api/province/district/" + selectedPro;
    loadDropdownDataDis();
    // dropdownDis.selectedIndex = 1;
    // provIndex = dropdownProv.selectedIndex;
    // disIndex = dropdownDis.selectedIndex = 0;
    // wardIndex = dropdownWard.selectedIndex = -1;
});


// dropdownDis.addEventListener("click", function (event) {
//     selectedDis = dropdownDis.value;
//     wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + selectedDis;
//     loadDropdownDataWard();
//     // disIndex = dropdownDis.selectedIndex;
//     // wardIndex = dropdownWard.selectedIndex = 0;

// });
dropdownDis.addEventListener("change", function (event) {
    selectedDis = dropdownDis.value;
    wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + selectedDis;
    loadDropdownDataWard();
    // disIndex = dropdownDis.selectedIndex;
    // wardIndex = dropdownWard.selectedIndex = 0;
});
dropdownWard.addEventListener("change", function (event) {
    selectedWard = dropdownWard.selectedIndex;
    wardIndex = dropdownWard.selectedIndex;
    // wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + selectedDis;
    // loadDropdownDataWard();
});
// dropdownWard.addEventListener("click", function (event) {
//     selectedWard = dropdownWard.selectedIndex;
//     wardIndex = dropdownWard.selectedIndex;
//     // console.log(selectedWard);
//     // console.log(dropdownWard.value);
//     // console.log(dropdownWard.text);
//     // wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + selectedDis;
//     // loadDropdownDataWard();
// });

btn_confirm.addEventListener("click", function (event) {
    event.preventDefault(); // Ngăn chặn hành vi mặc định của liên kết
    if (!bg_deli.classList.contains('hidden')) {
        if (name_input == null || name_input == "") {
            alert("Họ tên người nhận không thể trống!");
            return
        }
        if (phone_input == null || phone_input == "") {
            alert("Số điện thoại người nhận không thể trống!");
            return
        }
        if (dropdownProv.options[dropdownProv.selectedIndex].text == null) {
            alert("Tỉnh/Thành phố không thể trống!");
            return
        }
        if (dropdownDis.options[dropdownDis.selectedIndex].text == null) {
            alert("Quận/Huyện không thể trống!");
            return
        }
        if (dropdownWard.options[dropdownWard.selectedIndex].text == null) {
            alert("Xã/Phường không thể trống!");
            return
        }
        name_contact = name_input;
        number_contact = phone_input;
        if (apartment == null) {
            deli_add = dropdownWard.options[dropdownWard.selectedIndex].textContent + ", " + dropdownDis.options[dropdownDis.selectedIndex].textContent + ", " + dropdownProv.options[dropdownProv.selectedIndex].textContent
        }
        else {
            deli_add = apartment + ", " + dropdownWard.options[dropdownWard.selectedIndex].textContent + ", " + dropdownDis.options[dropdownDis.selectedIndex].textContent + ", " + dropdownProv.options[dropdownProv.selectedIndex].textContent
        }
    }
    if (bg_deli.classList.contains('hidden')) {
        if (name_contact == "") {
            alert("Họ tên người nhận không thể trống!");
            return
        }
        if (number_contact == "") {
            alert("Số điện thoại người nhận không thể trống!");
            return
        }
    }
    // console.log(name_contact);
    // console.log(number_contact);
    // console.log(deli_add);

    name_take.value = name_contact;
    number_take.value = number_contact;
    var diaChi = document.getElementById("diaChi")
    diaChi.value = deli_add;
    var myModal = document.getElementById("myModal")
    myModal.submit()
});

//Modal select address
select_address.addEventListener('click', function (event) {
    event.preventDefault();
    modal.style.visibility = "hidden";
    addressModal.style.visibility = "visible";
    var radio_id = document.getElementById("radio_id");
    radio_id.checked = true;
    bg_deli.classList.add("hidden");
    box_select_ad.classList.remove("hidden");
})
close_modal_select.addEventListener('click', function (event) {
    event.preventDefault();
    var radio_id = document.getElementById("radio_id");
    radio_id.checked = true;
    bg_deli.classList.add("hidden");
    if (bg_deli.classList.contains('hidden')) {
        if (name_contact == "") {
            box_select_ad.classList.add("hidden");
        }
    }
    else {
        box_select_ad.classList.remove("hidden");
    }
    addressModal.style.visibility = 'hidden';
    modal.style.visibility = "visible";
});

// choose_address.forEach(function (button) {
//     button.addEventListener("click", function (event) {
//         event.preventDefault(); // Ngăn chặn hành vi mặc định của liên kết

//         // loadDropdownDataProv()
//         console.log(tenTinh);
//         console.log(tenHuyen);
//         console.log(tenPhuong);
//     });
// });

// changeAddress.forEach(function (button) {
//     button.addEventListener("click", function (event) {
//         event.preventDefault(); // Ngăn chặn hành vi mặc định của liên kết
//         // modal.innerHTML = initialState;
//         addressModal.style.visibility = "visible";
//     });
// });

// changeAddressBtn.forEach(function (button) {
//     button.addEventListener("click", function (event) {
//         event.preventDefault(); 
//         console.log(address);
//         for (let i = 0; i < address.length; i++) {
//             address[i].style.borderStyle = "solid";
//             address[i].style.borderColor = "#E5E7EB";
//           }
//           for (let i = 0; i < deleteAddressBtn.length; i++) {
//             deleteAddressBtn[i].style.visibility = "inherit";
//           }
//         this.parentElement.style.borderStyle = "dashed";
//         this.parentElement.style.borderColor = "green";
//         this.nextSibling.nextSibling.nextSibling.nextSibling.style.visibility = "hidden";
//     });
// });

function getParent(element, selector) {
    while (element.parentElement) {
        if (element.parentElement.matches(selector)) {
            return element.parentElement;
        }
        element = element.parentElement;
    }

}


function loadDropdownDataProv() {
    // Đặt URL của API endpoint của bạn ở đây
    const apiUrl = 'https://vapi.vnappmob.com/api/province/';
    dropdownProv.innerHTML = '';
    fetch(apiUrl)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Chuyển đổi phản hồi thành js object
        })
        .then((data) => {
            // Xử lý dữ liệu ở đây, ví dụ: hiển thị dữ liệu trong console
            data['results'].forEach((item) => {
                const option = document.createElement('option');
                option.value = item['province_id']; // Đặt giá trị cho option (ví dụ: item.code)
                option.text = item['province_name'];  // Đặt văn bản hiển thị cho option (ví dụ: item.name)
                dropdownProv.append(option);
            });
            provIndex = dropdownProv.selectedIndex = 0;
            selectedPro = dropdownProv.options[dropdownProv.selectedIndex].value;
        })
        .catch((error) => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function loadDropdownDataDis() {
    dropdownDis.innerHTML = '';
    fetch(disUrl)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Chuyển đổi phản hồi thành js object
        })
        .then((data) => {
            // Xử lý dữ liệu ở đây, ví dụ: hiển thị dữ liệu trong console
            data['results'].forEach((item) => {
                const option = document.createElement('option');
                option.value = item['district_id']; // Đặt giá trị cho option (ví dụ: item.code)
                option.text = item['district_name'];  // Đặt văn bản hiển thị cho option (ví dụ: item.name)
                dropdownDis.append(option);
            });

            disIndex = dropdownDis.selectedIndex = 0;
            selectedDis = dropdownDis.options[dropdownDis.selectedIndex].value;
            // selectedDis=dropdownDis.options[dropdownDis.selectedIndex].value;
            if (selectedDis == null) {
                dropdownWard.innerHTML = '';
            }
            else {
                wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + selectedDis;
                loadDropdownDataWard();
            }

        })
        .catch((error) => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function loadDropdownDataWard() {
    dropdownWard.innerHTML = '';
    fetch(wardUrl)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Chuyển đổi phản hồi thành js object
        })
        .then((data) => {
            // Xử lý dữ liệu ở đây, ví dụ: hiển thị dữ liệu trong console
            data['results'].forEach((item) => {
                const option = document.createElement('option');
                option.value = item['ward_id']; // Đặt giá trị cho option (ví dụ: item.code)
                option.text = item['ward_name'];  // Đặt văn bản hiển thị cho option (ví dụ: item.name)
                dropdownWard.append(option);
            });
            wardIndex = dropdownWard.selectedIndex = 0;
            selectedWard = dropdownWard.options[dropdownWard.selectedIndex].value;
        })
        .catch((error) => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

//Thay số địa chỉ thành tên
var addresses = document.querySelectorAll("span.address");
let tenTinh;
let tenHuyen;
let tenPhuong;

document.addEventListener("DOMContentLoaded", async function () {
    for (let i = 0; i < addresses.length; i++) {
        let address = addresses[i].innerHTML.split(", ");
        console.log(address);
        await dropdownDataProv(address[address.length - 1]); // Gọi hàm để tải dữ liệu vào dropdownProv khi trang đã sẵn sàng
        disUrl = "https://vapi.vnappmob.com/api/province/district/" + address[address.length - 1];
        await dropdownDataDis(address[address.length - 2]);
        wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + address[address.length - 2];
        await dropdownDataWard(address[address.length - 3]);
        if (address.length < 4) {
            addresses[i].innerHTML = [tenPhuong, tenHuyen, tenTinh].join(", ")
        }
        else {
            addresses[i].innerHTML = [address.slice(0, address.length - 3).join(", "), tenPhuong, tenHuyen, tenTinh].join(", ")
        }

    }
});

async function dropdownDataProv(a, b = 0) {
    try {
        const apiUrl = 'https://vapi.vnappmob.com/api/province/';
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        i = 0
        data['results'].forEach((item) => {
            const option = document.createElement('option');
            option.value = item['province_id'];
            option.text = item['province_name'];
            if (option.value == a) {
                tenTinh = option.text;
            }
            if (option.value == b) {
                dropdownProv.selectedIndex = i
            }
            i++
        });
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function dropdownDataDis(a, b = 0) {
    try {
        dropdownDis.innerHTML = '';
        // Đặt URL của API endpoint của bạn ở đây
        const response = await fetch(disUrl);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        i = 0
        data['results'].forEach((item) => {
            const option = document.createElement('option');
            option.value = item['district_id'];
            option.text = item['district_name'];
            dropdownDis.append(option);
            if (option.value == a) {
                tenHuyen = option.text;
            }
            if (option.value == b) {
                dropdownDis.selectedIndex = i
            }
            i++
        });
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function dropdownDataWard(a, b = 0) {
    try {
        dropdownWard.innerHTML = '';
        // Đặt URL của API endpoint của bạn ở đây
        const response = await fetch(wardUrl);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        // Xử lý dữ liệu ở đây
        i = 0
        data['results'].forEach((item) => {
            const option = document.createElement('option');
            option.value = item['ward_id'];
            option.text = item['ward_name'];
            dropdownWard.append(option);
            if (option.value == a) {
                tenPhuong = option.text;
            }
            if (option.value == b) {
                dropdownWard.selectedIndex = i
            }
            i++
        });
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}
