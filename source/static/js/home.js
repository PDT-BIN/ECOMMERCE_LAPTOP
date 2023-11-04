// CAROUSEL.
const slideContainer = document.querySelector('.slider-container');
var images = [];
for (let i = 1; i < 4; i++) {
    images[i] = `BANNER_${i}.png`;
}

for (let i = 1; i < images.length; i++) {
    slideContainer.innerHTML += `<div class="slide">
                                    <img src="../static/img/${images[i]}" alt=""> 
                                </div>`;
}

// SLIDESHOW TOUCH.
const slides = Array.from(document.querySelectorAll('.slide'));
let isDragging = false,
    startPos = 0,
    currentTranslate = 0,
    prevTranslate = 0,
    animationID,
    currentIndex = 0

slides.forEach((slide, index) => {
    const slideImage = slide.querySelector('img');
    slideImage.addEventListener('dragstart', (e) => e.preventDefault());
    // TOUCH EVENT.
    slide.addEventListener('touchstart', touchStart(index));
    slide.addEventListener('touchend', touchEnd);
    slide.addEventListener('touchmove', touchMove);
    // MOUSE EVENT.
    slide.addEventListener('mousedown', touchStart(index));
    slide.addEventListener('mouseup', touchEnd);
    slide.addEventListener('mousemove', touchMove);
    slide.addEventListener('mouseleave', touchEnd);
})
window.addEventListener('resize', setlaivitri);

function layvitri(event) {
    return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
}

function touchStart(index) {
    return function (event) {
        currentIndex = index; startPos = layvitri(event);
        isDragging = true;
        animationID = requestAnimationFrame(animation);
    }
}

function touchMove(event) {
    if (isDragging) {
        const currentPosition = layvitri(event);
        currentTranslate = prevTranslate + currentPosition - startPos;
    }
}

function touchEnd() {
    cancelAnimationFrame(animationID);
    isDragging = false;
    const movedBy = currentTranslate - prevTranslate;
    if (movedBy < -100 && currentIndex <= slides.length - 1) {
        currentIndex += 1;
        // CHECK VỊ TRÍ NẾU Ở CUỐI CHO VỀ LẠI ĐẦU.
        if (currentIndex > slides.length - 1) {
            currentIndex = 0;
        }
    }
    if (movedBy > 100 && currentIndex >= 0) {
        if (currentIndex == 0) {
            currentIndex = slides.length - 1;
        }
        else {
            currentIndex -= 1;
        }
    }
    setlaivitri();
}

const movedBy = currentTranslate - prevTranslate;

function animation() {
    setSliderPosition()
    if (isDragging) requestAnimationFrame(animation);
}
function setlaivitri() {
    currentTranslate = currentIndex * -window.innerWidth;
    prevTranslate = currentTranslate;
    setSliderPosition();
}

currentTranslate = currentIndex * -window.innerWidth;

// HÀM SỬA LẠI THÔNG SỐ TRANSLATEX CỦA CSS CÓ CLASS = "SLIDER-CONTAINER".
function setSliderPosition() {
    slideContainer.style.transform = `translateX(${currentTranslate}px)`;
}

// HÀM AUTO-PLAY.
setInterval(function () {
    currentIndex++;
    if (currentIndex > slides.length - 1) {
        currentIndex = 0;
    }
    setlaivitri();
}, 5000);

// HÀM NEXT VÀ PREV.
function nextandprev(n) {
    if (n == 1) {
        currentIndex++;
        if (currentIndex > slides.length - 1) {
            currentIndex = 0;
        }
        setlaivitri();
    }
    else {
        if (currentIndex == 0) {
            currentIndex = slides.length;
        }
        currentIndex--;
        setlaivitri();
    }
}