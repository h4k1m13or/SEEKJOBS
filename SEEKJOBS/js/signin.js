(function ($) {

    "use strict";

    $(window).on('load', function () {

        /*Page Loader active
          ========================================================*/


//resume nav


        /* slicknav mobile menu active  */
        $('.mobile-menu').slicknav({
            prependTo: '.navbar-header',
            parentTag: 'liner',
            allowParentLinks: true,
            duplicate: true,
            label: '',
        });

        /* WOW Scroll Spy
      ========================================================*/
        var wow = new WOW({
            //disabled for mobile
            mobile: false
        });
        wow.init();

        /* Nivo Lightbox
        ========================================================*/
        $('.lightbox').nivoLightbox({
            effect: 'fadeScale',
            keyboardNav: true,
        });

        // one page navigation
        // $('.navbar-nav').onePageNav({
        //         currentClass: 'active'
        // });

        /* Back Top Link active
        ========================================================*/
        var offset = 200;
        var duration = 500;
        $(window).scroll(function () {
            if ($(this).scrollTop() > offset) {
                $('.back-to-top').fadeIn(400);
            } else {
                $('.back-to-top').fadeOut(400);
            }
        });

        $('.back-to-top').on('click', function (event) {
            event.preventDefault();
            $('html, body').animate({
                scrollTop: 0
            }, 600);
            return false;
        });

    });


// hada lcode ta3 lform

// Tooltips Initialization
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })

// Steppers
    $(document).ready(function () {
        var navListItems = $('div.setup-panel-2 div a'),
            allWells = $('.setup-content-2'),
            allNextBtn = $('.nextBtn-2'),
            allPrevBtn = $('.prevBtn-2');

        allWells.hide();
        $('.setup-content-2').hide();

        navListItems.click(function (e) {
            e.preventDefault();
            var $target = $($(this).attr('href')),
                $item = $(this);

            if (!$item.hasClass('disabled')) {
                navListItems.removeClass('btn-amber').addClass('btn-blue-grey');
                $item.addClass('btn-amber');
                allWells.show().hide();
                $target.show();
                $target.find('input:eq(0)').focus();
            }
        });

        allPrevBtn.click(function () {
            var curStep = $(this).closest(".setup-content-2"),
                curStepBtn = curStep.attr("id"),
                prevStepSteps = $('div.setup-panel-2 div a[href="#' + curStepBtn + '"]').parent().prev().children("a");

            prevStepSteps.removeAttr('disabled').trigger('click');
        });

        allNextBtn.click(function () {
            var curStep = $(this).closest(".setup-content-2"),
                curStepBtn = curStep.attr("id"),
                nextStepSteps = $('div.setup-panel-2 div a[href="#' + curStepBtn + '"]').parent().next().children("a"),
                curInputs = curStep.find("input[type='text'],input[type='url']"),
                isValid = true;

            $(".form-group").removeClass("has-error");
            for (var i = 0; i < curInputs.length; i++) {
                if (!curInputs[i].validity.valid) {
                    isValid = false;
                    $(curInputs[i]).closest(".form-group").addClass("has-error");
                }
            }

            if (isValid && document.getElementById('id_password1').value ==
                document.getElementById('id_password2').value)

                nextStepSteps.removeAttr('disabled').trigger('click');
            else {
                nextStepSteps.trigger(function () {


                })
            }
        });


        $('div.setup-panel-2 div a.btn-amber').trigger('click');
    });
// Material Select Initialization
    $(document).ready(function () {
        $('.mdb-select').materialSelect();
        $('.select-wrapper.md-form.md-outline input.select-dropdown').bind('focus blur', function () {
            $(this).closest('.select-outline').find('label').toggleClass('active');
            $(this).closest('.select-outline').find('.caret').toggleClass('active');
        });
    });
// Data Picker Initialization

    $(function () {
        $("#datepicker").datepicker();
    });


}(jQuery));


var check = function () {
    if (document.getElementById('id_password1').value ==
        document.getElementById('id_password2').value) {
        document.getElementById('message').style.color = 'green';
        document.getElementById('message').innerHTML = '';

    } else {
        document.getElementById('message').style.color = 'red';
        document.getElementById('message').innerHTML = "password doesn't match";

    }


}
var hideResume = function () {

    var x = document.getElementById("resume-up");
    x.style.display = "none";
}
var showResume = function () {

    var x = document.getElementById("resume-up");
    x.style.display = "bloxk";
}