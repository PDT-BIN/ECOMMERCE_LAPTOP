var buyButtons = document.querySelectorAll("a[data-action='buy-now'], button.buyButtons");
var closeButton = document.getElementById("closeModal");
var dropdownProv = document.getElementById("dropdownProv");
var dropdownWard = document.getElementById("dropdownWard");
var dropdownDis = document.getElementById("dropdownDistr");
var modal = document.getElementById('myModal');
var selectedPro = 92;
var disUrl = "https://vapi.vnappmob.com/api/province/district/" + selectedPro;
var selectedDis = 925;
var wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + selectedDis;

var indexPro = document.querySelector('input[name="province"]')
var indexDis = document.querySelector('input[name="district"]')
var indexWar = document.querySelector('input[name="commune"]')

document.addEventListener("DOMContentLoaded", function () {
    loadDropdownDataProv(); // Gọi hàm để tải dữ liệu vào dropdownProv khi trang đã sẵn sàng
    loadDropdownDataDis();
    loadDropdownDataWard();
});
// var initialState = modal.innerHTML;

buyButtons.forEach(function (button) {
    button.addEventListener("click", function (event) {
        event.preventDefault(); // Ngăn chặn hành vi mặc định của liên kết
        // modal.innerHTML = initialState;
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
    }
});
window.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        modal.style.visibility = "hidden";
    }
});

dropdownProv.addEventListener("change", function (event) {
    selectedPro = dropdownProv.value;
    // console.log(selectedValue);
    disUrl = "https://vapi.vnappmob.com/api/province/district/" + selectedPro;
    loadDropdownDataDis();
    indexPro.value = dropdownProv.selectedIndex
});

dropdownDis.addEventListener("click", function (event) {
    selectedDis = dropdownDis.value;
    wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + selectedDis;
    loadDropdownDataWard();
    indexDis.value = dropdownDis.selectedIndex
});
dropdownDis.addEventListener("change", function (event) {
    selectedDis = dropdownDis.value;
    wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + selectedDis;
    loadDropdownDataWard();
    indexDis.value = dropdownDis.selectedIndex
});

dropdownWard.addEventListener("click", function (event) {
    selectedWard = dropdownWard.value;
    indexWar.value = dropdownWard.selectedIndex
});

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
            selectedDis = dropdownDis.options[0].value;
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

//Cập nhật
let updateBtn = document.querySelectorAll("button.updateBtn")
let nameInput = document.getElementById("nameInput")
let tel = document.getElementById("tel")
let houseNum = document.getElementById("houseNum")
let updatePk = document.getElementById("submitBtnModal")

updateBtn.forEach(function (button) {
    button.addEventListener("click", async function (event) {
        event.preventDefault();
        modal.style.visibility = "visible";
        updateAddress = this.parentNode.previousElementSibling.children[2].innerHTML.split(", ");
        updateName = this.parentNode.previousElementSibling.children[0].children[0].innerText;
        updatePhone = this.parentNode.previousElementSibling.children[0].children[1].innerText;
        updatePk.value = this.nextElementSibling.children[1].value;
        nameInput.value = updateName;
        tel.value = updatePhone;
        houseNum.value = updateAddress.slice(0, updateAddress.length - 3).join(", ");
        await dropdownDataProv(0, updateAddress[updateAddress.length - 1]);
        disUrl = "https://vapi.vnappmob.com/api/province/district/" + updateAddress[updateAddress.length - 1];
        await dropdownDataDis(0, updateAddress[updateAddress.length - 2]);
        wardUrl = "https://vapi.vnappmob.com/api/province/ward/" + updateAddress[updateAddress.length - 2];
        await dropdownDataWard(0, updateAddress[updateAddress.length - 3]);
    });
});

//reset field sau khi đóng form 
closeButton.addEventListener("click", async function (event) {
    nameInput.value = '';
    tel.value = '';
    houseNum.value = '';
    await dropdownDataProv(0, 92);
    disUrl = "https://vapi.vnappmob.com/api/province/district/92";
    await dropdownDataDis(0, 925);
    wardUrl = "https://vapi.vnappmob.com/api/province/ward/925";
    await dropdownDataWard(0, updateAddress[updateAddress.length - 3]);
})

// //Xác nhận xóa
// let deleteFrm = document.getElementById("deleteFrm")
// dele