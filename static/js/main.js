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


   

    // ─── Mobile Navbar Control ────────────────────────────────────────────────
    
    // Sync toggler icon (fa-bars <-> fa-times) on Bootstrap collapse events
    $('#navbarCollapse').on('show.bs.collapse', function () {
        $('.navbar-toggler i, .navbar-toggler span')
            .removeClass('fa-bars')
            .addClass('fa-times');
        $('[data-bs-target="#navbarCollapse"]').attr('aria-expanded', 'true');
    }).on('hide.bs.collapse', function () {
        $('.navbar-toggler i, .navbar-toggler span')
            .removeClass('fa-times')
            .addClass('fa-bars');
        $('[data-bs-target="#navbarCollapse"]').attr('aria-expanded', 'false');
    });

    /**
     * Safely close the mobile navbar collapse across Bootstrap 5 & jQuery
     */
    function closeMobileNav() {
        var $collapse = $('#navbarCollapse');
        if ($collapse.hasClass('show') || $collapse.hasClass('collapsing')) {
            if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
                var bsCollapse = bootstrap.Collapse.getInstance($collapse[0]);
                if (!bsCollapse) {
                    bsCollapse = new bootstrap.Collapse($collapse[0], { toggle: false });
                }
                bsCollapse.hide();
            } else {
                $collapse.removeClass('show');
            }
            $('.navbar-toggler i, .navbar-toggler span')
                .removeClass('fa-times')
                .addClass('fa-bars');
            $('[data-bs-target="#navbarCollapse"]').attr('aria-expanded', 'false');
        }
    }

    // 1. Close when tapping explicit mobile close button (#closeMobileMenuBtn)
    $(document).on('click', '#closeMobileMenuBtn', function (e) {
        e.preventDefault();
        closeMobileNav();
    });

    // 2. Close when a nav link or dropdown-item inside the mobile menu is tapped
    $(document).on('click', '#navbarCollapse .nav-link:not(.dropdown-toggle), #navbarCollapse .dropdown-item', function () {
        closeMobileNav();
    });

    // 3. Close when tapping outside the navbar container
    $(document).on('click', function (e) {
        var $nav = $('.nav-bar');
        if ($('#navbarCollapse').hasClass('show') && !$nav.is(e.target) && $nav.has(e.target).length === 0) {
            closeMobileNav();
        }
    });


    // ─── All Categories Dropdown Auto-Close ─────────────────────────────────

    /**
     * Close the "All Categories" dropdown menu and sync aria state.
     */
    function closeAllCat() {
        var $allCat = $('#allCat');
        if ($allCat.hasClass('show')) {
            if (typeof bootstrap !== 'undefined' && bootstrap.Collapse) {
                var bsCollapse = bootstrap.Collapse.getInstance($allCat[0]) || new bootstrap.Collapse($allCat[0], { toggle: false });
                bsCollapse.hide();
            } else {
                $allCat.removeClass('show');
            }
            $('[data-bs-target="#allCat"], [data-target="#allCat"]').attr('aria-expanded', 'false');
        }
    }

    // 1. Close when a category link inside #allCat is clicked
    $(document).on('click', '#allCat a', function () {
        closeAllCat();
    });

    // 2. Close when user clicks anywhere outside #allCat and its toggle button
    $(document).on('click', function (e) {
        var $allCat = $('#allCat');
        if ($allCat.hasClass('show')) {
            var $btn = $('[data-bs-target="#allCat"], [data-target="#allCat"]');
            if (!$allCat.is(e.target) && $allCat.has(e.target).length === 0 &&
                !$btn.is(e.target) && $btn.has(e.target).length === 0) {
                closeAllCat();
            }
        }
    });

})(jQuery);

