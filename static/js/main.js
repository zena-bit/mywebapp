(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
                $('#spinner').hide();
            }
        }, 1);
    };
    spinner(0);
    
    
    // Initiate the wowjs
    if (typeof WOW !== 'undefined') {
        new WOW().init();
    }


    // Fall back to a no-op if owlCarousel failed to load, so the handlers below still bind
    if (!$.fn.owlCarousel) {
        $.fn.owlCarousel = function () { return this; };
    }


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.nav-bar').addClass('sticky-top shadow-sm');
        } else {
            $('.nav-bar').removeClass('sticky-top shadow-sm');
        }
    });


    // Hero Header carousel
    if ($(".header-carousel").length && $.fn.owlCarousel) {
        $(".header-carousel").owlCarousel({
            items: 1,
            autoplay: true,
            smartSpeed: 2000,
            center: false,
            dots: false,
            loop: true,
            margin: 0,
            nav : true,
            navText : [
                '<i class="bi bi-arrow-left"></i>',
                '<i class="bi bi-arrow-right"></i>'
            ]
        });
    }

    // ProductList carousel
    if ($(".productList-carousel").length && $.fn.owlCarousel) {
        $(".productList-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 2000,
            dots: false,
            loop: true,
            margin: 25,
            nav : true,
            navText : [
                '<i class="fas fa-chevron-left"></i>',
                '<i class="fas fa-chevron-right"></i>'
            ],
            responsiveClass: true,
            responsive: {
                0:{ items:1 },
                576:{ items:1 },
                768:{ items:2 },
                992:{ items:2 },
                1200:{ items:3 }
            }
        });
    }

    // Single Products carousel
    if ($(".single-carousel").length && $.fn.owlCarousel) {
        $(".single-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 1500,
            dots: true,
            dotsData: false,
            loop: false,
            items: 1,
            nav : true,
            navText : [
                '<i class="bi bi-arrow-left"></i>',
                '<i class="bi bi-arrow-right"></i>'
            ]
        });
    }

    // Related Products carousel
    if ($(".related-carousel").length && $.fn.owlCarousel) {
        $(".related-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 1500,
            dots: false,
            loop: true,
            margin: 25,
            nav : true,
            navText : [
                '<i class="fas fa-chevron-left"></i>',
                '<i class="fas fa-chevron-right"></i>'
            ],
            responsiveClass: true,
            responsive: {
                0:{ items:1 },
                576:{ items:1 },
                768:{ items:2 },
                992:{ items:3 },
                1200:{ items:4 }
            }
        });
    }



    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });


    
   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        var easing = $.easing && $.easing.easeInOutExpo ? 'easeInOutExpo' : 'swing';
        $('html, body').animate({scrollTop: 0}, 1500, easing);
        return false;
    });


   

    // Mobile Navbar Toggler Fallback
    $(document).on('click', '.navbar-toggler', function (e) {
        var target = $(this).attr('data-bs-target') || $(this).attr('data-target');
        if (target && $(target).length) {
            e.preventDefault();
            $(target).toggleClass('show');
        }
    });


    // ─── Mobile Menu Auto-Close ───────────────────────────────────────────────

    /**
     * Close the mobile navbar collapse and update the toggler aria state.
     */
    function closeMobileNav() {
        var $collapse = $('#navbarCollapse');
        if ($collapse.hasClass('show')) {
            $collapse.removeClass('show');
            // Keep aria-expanded in sync so screen-readers and Bootstrap are happy
            $('[data-bs-target="#navbarCollapse"], [data-target="#navbarCollapse"]')
                .attr('aria-expanded', 'false');
        }
    }

    // 1. Close when a nav link or dropdown-item inside the mobile menu is tapped.
    //    Dropdown-toggle links are excluded so sub-menus can still open normally.
    $(document).on('click', '#navbarCollapse .nav-link:not(.dropdown-toggle), #navbarCollapse .dropdown-item', function () {
        closeMobileNav();
    });

    // 2. Close when the user taps anywhere outside the navbar (overlay / content tap).
    $(document).on('click touchstart', function (e) {
        var $nav = $('.nav-bar');
        // Only act when the menu is open and the tap was outside the navbar
        if ($('#navbarCollapse').hasClass('show') && !$nav.is(e.target) && $nav.has(e.target).length === 0) {
            closeMobileNav();
        }
    });

})(jQuery);

