/**
* Gumby Framework
*************************************************************/
Gumby.ready(function() {
	Gumby.log('Gumby is ready to go...', Gumby.dump());

	// placeholder polyfil
	if(Gumby.isOldie || Gumby.$dom.find('html').hasClass('ie9')) {
		$('input, textarea').placeholder();
	}

// Oldie document loaded
}).oldie(function() {
	Gumby.warn("This is an oldie browser...");

// Touch devices loaded
}).touch(function() {
	Gumby.log("This is a touch enabled device...");
});
/**
* / END Gumby Framework / *
*************************************************************/




/**
* Scroll Animation Module
*************************************************************/

var ScrollAnimations = (function () {

	//dont do anything if touch is supported (as scroll event wont fire properly)
	if( Modernizr.touch ) return;

    var s; // private alias to settings
    return {

        settings: {
        	$scrollElements:     $(".animate-on-scroll"),
        	initClass:           "scroll-animation-init",
        	dataAnimation:       "scrollanimation"
        },

        init: function() {
          s = this.settings; 
          s.$scrollElements.addClass(s.initClass);    
          this.bindUIActions();
        },

        bindUIActions: function() {

        	s.$scrollElements.waypoint(function(direction) {
				switch(direction) {
					case 'down':
						ScrollAnimations.doDownAnim($(this), $(this).data(s.dataAnimation));
					break;
				}        		
        	}, { offset: '75%' });

        },

        doDownAnim: function(element, animClass) {
			element.addClass(animClass);
        } 

    };
})();

/**
* / END Scroll Animation Module / *
*************************************************************/




/**
* Initialise plugins and scroll animations on document ready
*************************************************************/
$(function() {
	
	// skip link and toggle on one element
	// when the skip link completes, trigger the switch
	$('#skip-switch').on('gumby.onComplete', function() {
		$(this).trigger('gumby.trigger');
	});


	//initialise gallery slider
	$('.gallery-slider').bxSlider({
		pager:false,
		nextText: '<i class="icon-right-open-big"></i><span class="screen-reader-text">Next</span>',
		prevText: '<i class="icon-left-open-big"></i><span class="screen-reader-text">Prev</span>'
	});


	//initialise testimonials slider
	$('.testimonials-slider').bxSlider({
		auto: true,
		pause: 6000,
		controls:false,
		mode: 'fade'
	});

	//initialise scroll animations
	ScrollAnimations.init();

});