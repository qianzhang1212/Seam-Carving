(function ($) {
    "use strict"; // Start of use strict

    // jQuery for page scrolling feature - requires jQuery Easing plugin
    $(document).on('click', 'a.page-scroll', function (event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 1250, 'easeInOutExpo');
        event.preventDefault();
    });

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 51
    });

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function () {
        $('.navbar-toggle:visible').click();
    });

    // Offset for Main Navigation
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    })

    // Initialize and Configure Scroll Reveal Animation
    window.sr = ScrollReveal();
    sr.reveal('.sr-icons', {
        duration: 600,
        scale: 0.3,
        distance: '0px'
    }, 200);
    sr.reveal('.sr-button', {
        duration: 1000,
        delay: 200
    });
    sr.reveal('.sr-contact', {
        duration: 600,
        scale: 0.3,
        distance: '0px'
    }, 300);

})(jQuery); // End of use strict

jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;


$('form#input-form').on('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    var inputImage = $('#input-upload').prop('files')[0];
    var maskImage = $('#mask-upload').prop('files')[0];
    formData.append('input-image', inputImage)
    formData.append('mask-image', maskImage)
    // for (var [key, value] of formData.entries()) {
    //     console.log(key, value);
    // }
    $('#declare').show()
    $.ajax({
        url: '/seamcarving/process',
        type: 'POST',
        data: formData,
        processData: false, // tell jQuery not to process the data
        contentType: false, // tell jQuery not to set contentType
        cache: false,
        success: function (response) {
            $('#declare').hide();
            window.open(response, 'Download');
        },
        error: function () {
            console.log(arguments);
        }
    });
});