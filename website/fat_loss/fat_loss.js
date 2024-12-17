$(document).ready(function() {
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#goTop').fadeIn();
        } else {
            $('#goTop').fadeOut();
        }
    });


    $('#goTop').click(function() {
        $('html, body').animate({scrollTop: 0}, 500);
        return false;
    });
});



$(document).ready(function() {
    $('ul li').click(function(event) {

        const offset = $(this).offset();
        const tooltip = $('<div class="tooltip"></div>');
        const title = $(this).data('title');
        const info = $(this).data('info');


        tooltip.html(`<h4>${title}</h4><p>${info}</p>`).appendTo('body');
        tooltip.css({
            top: offset.top + $(this).outerHeight(), 
            left: offset.left 
        }).fadeIn(); 


        $(this).one('mouseleave', function() {
            tooltip.fadeOut(function() {
                tooltip.remove();
            });
        });


        $(document).on('click.tooltip', function(e) {
            if (!$(e.target).closest('.tooltip').length && !$(e.target).closest('li').length) {
                tooltip.fadeOut(function() {
                    tooltip.remove(); 
                });
                $(document).off('click.tooltip');
            }
        });
    });
});
