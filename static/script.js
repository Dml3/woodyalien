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