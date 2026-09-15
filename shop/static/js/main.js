document.addEventListener('DOMContentLoaded', function () {
    // Product Detail Image Gallery Switcher
    const mainProductImg = document.getElementById('mainProductImage');
    const galleryThumbs = document.querySelectorAll('.gallery-thumbs .thumb-item');

    if (mainProductImg && galleryThumbs.length > 0) {
        galleryThumbs.forEach(function (thumb) {
            thumb.addEventListener('click', function () {
                if (mainProductImg.tagName.toLowerCase() === 'img') {
                    mainProductImg.src = this.src;
                }
                galleryThumbs.forEach(function (t) {
                    t.classList.remove('active');
                });
                this.classList.add('active');
            });
        });
    }

    // Swiper Sliders
    if (typeof Swiper !== 'undefined') {
        const createSwiper = (selector, nextBtn, prevBtn, pagEl, delay) => {
            if (document.querySelector(selector)) {
                new Swiper(selector, {
                    slidesPerView: 2,
                    spaceBetween: 12,
                    loop: true,
                    autoplay: {
                        delay: delay || 3000,
                        disableOnInteraction: false,
                        pauseOnMouseEnter: true,
                    },
                    navigation: {
                        nextEl: nextBtn,
                        prevEl: prevBtn,
                    },
                    pagination: {
                        el: pagEl,
                        clickable: true,
                    },
                    breakpoints: {
                        768: { slidesPerView: 3, spaceBetween: 15 },
                        1024: { slidesPerView: 4, spaceBetween: 20 },
                    }
                });
            }
        };

        createSwiper('.bestsellers-swiper', '.bestsellers-next', '.bestsellers-prev', '.bestsellers-pagination', 3000);
        createSwiper('.discounted-swiper', '.discounted-next', '.discounted-prev', '.discounted-pagination', 3500);
        createSwiper('.related-swiper', '.related-next', '.related-prev', '.related-pagination', 3200);
    }

    // Hover Dropdowns (Desktop)
    // باز شدن منوهای کشویی نوار بالا با هاور موس در دسکتاپ
    if (typeof bootstrap !== 'undefined') {
        document.querySelectorAll('.header .dropdown').forEach(function (dropdown) {
            const toggle = dropdown.querySelector('[data-bs-toggle="dropdown"]');
            if (!toggle) return;

            dropdown.addEventListener('mouseenter', function () {
                if (window.innerWidth >= 992) {
                    bootstrap.Dropdown.getOrCreateInstance(toggle).show();
                }
            });

            dropdown.addEventListener('mouseleave', function () {
                if (window.innerWidth >= 992) {
                    const instance = bootstrap.Dropdown.getInstance(toggle);
                    if (instance && dropdown.querySelector('.dropdown-menu.show')) {
                        instance.hide();
                    }
                }
            });
        });
    }
});
