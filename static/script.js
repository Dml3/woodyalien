document.addEventListener("DOMContentLoaded", () => {
  const header = document.getElementById("header");
  const scrollBtn = document.getElementById("scrollToTopBtn");
  const navLinks = document.querySelectorAll(".nav-link");
  const sections = document.querySelectorAll("section");

  // --- Затемнение хедера при скролле ---
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) header.classList.add("scrolled");
    else header.classList.remove("scrolled");

    // Кнопка "наверх"
    if (window.scrollY > 200) scrollBtn.style.display = "block";
    else scrollBtn.style.display = "none";

    // Активная ссылка при прокрутке
    let current = "";
    sections.forEach(section => {
      const sectionTop = section.offsetTop - 120;
      if (scrollY >= sectionTop) current = section.getAttribute("id");
    });

    navLinks.forEach(link => {
      link.classList.remove("active");
      if (link.getAttribute("href") === `#${current}`) {
        link.classList.add("active");
      }
    });
  });

  // --- Плавный скролл при клике ---
  navLinks.forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      const target = document.querySelector(link.getAttribute("href"));
      target.scrollIntoView({ behavior: "smooth" });
    });
  });

  // --- Кнопка "наверх" ---
  scrollBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});

document.querySelectorAll('nav a[href^="#"]').forEach(link => {
    link.addEventListener("click", e => {
        e.preventDefault();
        const targetID = link.getAttribute("href").substring(1);
        const target = document.getElementById(targetID);

        window.scrollTo({
            top: target.offsetTop - 80,   // чтобы не залезало под хедер
            behavior: "smooth"
        });

        history.pushState(null, "", "#" + targetID); // обновляем URL
    });
});
