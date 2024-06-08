// ___

// CARD (PORTLET) AUTO-SIZE TO PAGE

var KTLayoutStretchedCard=function() {
 // Private properties
 var _element;

 // Private functions
var _init=function() {
var scroll=KTUtil.find(_element, '.card-scroll');
var cardBody=KTUtil.find(_element, '.card-body');
var cardHeader=KTUtil.find(_element, '.card-header');

var height=KTLayoutContent.getHeight();

  height=height - parseInt(KTUtil.actualHeight(cardHeader));

  height=height - parseInt(KTUtil.css(_element, 'marginTop')) - parseInt(KTUtil.css(_element, 'marginBottom'));
  height=height - parseInt(KTUtil.css(_element, 'paddingTop')) - parseInt(KTUtil.css(_element, 'paddingBottom'));

  height=height - parseInt(KTUtil.css(cardBody, 'paddingTop')) - parseInt(KTUtil.css(cardBody, 'paddingBottom'));
  height=height - parseInt(KTUtil.css(cardBody, 'marginTop')) - parseInt(KTUtil.css(cardBody, 'marginBottom'));

  height=height - 3;

  KTUtil.css(scroll, 'height', height + 'px');
}

 // Public methods
 return {
  init: function(id) {
   _element=KTUtil.getById(id);

   if ( !_element) {
    return;
   }

   // Initialize
   _init();

   // Re-calculate on window resize
   KTUtil.addResizeHandler(function() {
     _init();
    }
   );
  },

  update: function() {
   _init();
  }
 };
}();

// Webpack support
if (typeof module !=='undefined') {
 module.exports=KTLayoutStretchedCard;
}

// ___

// RESHAPE HC IN CONTAINERS (RESPONSIVE)

$('#kt_aside_toggle').on('click', function (event) {
    setTimeout(function () {
        for (var i = 0; i < Highcharts.charts.length; i++) {
            Highcharts.charts[i].reflow();
        }
    }, 250);
});

// ___

// ALERTS

var avatar3 = new KTImageInput('kt_image_3');


$("#kt_sweetalert_success").click(function(e) {
    Swal.fire({
        position: "top-right",
        icon: "success",
        showConfirmButton: false,
        timer: 1000
    });
});

$("#kt_sweetalert_danger").click(function(e) {
    Swal.fire({
        position: "top-right",
        icon: "danger",
        showConfirmButton: false,
        timer: 1000
    });
});

