input_os = document.getElementById('os')
input_ram = document.getElementById('ram')
input_cpu = document.getElementById('cpu')
input_disk = document.getElementById('disk')
input_vga = document.getElementById('vga')
input_screen = document.getElementById('screen')
input_battery = document.getElementById('battery')
input_weight = document.getElementById('weight')
filter_inputs = [input_os, input_ram, input_cpu, input_disk,
    input_vga, input_screen, input_battery, input_weight]


all_specifications = document.querySelectorAll('.specification')
filter_inputs.forEach(filter_input => {
    filter_input.addEventListener("keyup", (e) => {
        all_specifications.forEach(specification => {
            os = specification.querySelector('.os').innerText.toLowerCase()
            ram = specification.querySelector('.ram').innerText.toLowerCase()
            cpu = specification.querySelector('.cpu').innerText.toLowerCase()
            disk = specification.querySelector('.disk').innerText.toLowerCase()
            vga = specification.querySelector('.vga').innerText.toLowerCase()
            screen = specification.querySelector('.screen').innerText.toLowerCase()
            battery = specification.querySelector('.battery').innerText.toLowerCase()
            weight = specification.querySelector('.weight').innerText.toLowerCase()

            if (os.includes(input_os.value) && ram.includes(input_ram.value)
                && cpu.includes(input_cpu.value) && disk.includes(input_disk.value)
                && vga.includes(input_vga.value) && screen.includes(input_screen.value)
                && battery.includes(input_battery.value) && weight.includes(input_weight.value)) {
                specification.style.display = 'flex'
            } else {
                specification.style.display = 'none'
            }
        })
    })
})