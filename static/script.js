document.addEventListener("DOMContentLoaded", () => {
  // --- затемнение хедера при скролле ---
  const header = document.getElementById("header");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  });

  // --- кнопка "наверх" ---
  const scrollBtn = document.getElementById("scrollToTopBtn");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 200) {
      scrollBtn.style.display = "block";
    } else {
      scrollBtn.style.display = "none";
    }
  });
  scrollBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // --- Swiper на странице продукта ---
  const productSwiper = document.querySelector(".productSwiper");
  if (productSwiper) {
    new Swiper(".productSwiper", {
      slidesPerView: 1,
      loop: true,
      pagination: {
        el: ".productSwiper .swiper-pagination",
        clickable: true,
      },
    });
  }
});
document.addEventListener("DOMContentLoaded", () => {
  // Слайдер только на странице товара
  const productSwiper = document.querySelector(".productSwiper");
  if (productSwiper) {
    new Swiper(".productSwiper", {
      slidesPerView: 1,
      loop: true,
      pagination: {
        el: ".productSwiper .swiper-pagination",
        clickable: true,
      },
    });
  }
});
