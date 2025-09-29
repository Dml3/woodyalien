window.addEventListener('scroll', () => {
    const header = document.getElementById('header');
    const scrollY = window.scrollY;

    if (scrollY > 100) {
        header.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
    } else {
        header.style.backgroundColor = `rgba(0, 0, 0, ${0.3 + scrollY * 0.007})`;
    }

    const scrollToTopBtn = document.getElementById('scrollToTopBtn');
    if (scrollY > 300) {
        scrollToTopBtn.classList.add('visible');
    } else {
        scrollToTopBtn.classList.remove('visible');
    }
});

document.getElementById('scrollToTopBtn').addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Главный слайдер
const mainSwiper = new Swiper(".mainSwiper", {
    slidesPerView: 3,
    spaceBetween: 20,
    loop: true,
    centeredSlides: true,
    pagination: {
        el: ".mainSwiper .swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".mainSwiper .swiper-button-next",
        prevEl: ".mainSwiper .swiper-button-prev",
    },
    breakpoints: {
        320: { slidesPerView: 1 },
        640: { slidesPerView: 2 },
        1024: { slidesPerView: 3 },
    }
});

// Мини-слайдеры внутри карточек
document.querySelectorAll('.productSwiper').forEach((el) => {
    new Swiper(el, {
        slidesPerView: 1,
        spaceBetween: 5,
        loop: false, // без бесконечного цикла
        pagination: { el: el.querySelector('.swiper-pagination'), clickable: true },
    });
});
