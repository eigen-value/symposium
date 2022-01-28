function sidebarCollapsible() {

    $("#sidebar").mCustomScrollbar({
         theme: "minimal"
    });

    $(document).ready(function () {
        $('#sidebarCollapse').on('click', function () {
            $('#sidebar').toggleClass('active');
            // close dropdowns
            $('.collapse.in').toggleClass('in');
            // and also adjust aria-expanded attributes we use for the open/closed arrows
            // in our CSS
            $('a[aria-expanded=true]').attr('aria-expanded', 'false');
            $( "#sidebarCollapse > i" ).toggleClass('fa-align-left').toggleClass('fa-chevron-left');
        });
    });
}

function sidebarComponents() {
    $(document).ready(function () {
        $('ul.sidebar-nav > li > a').on("click",function () {
            $('ul.sidebar-nav > li').removeClass('active');
            $(this).parent().toggleClass('active');
        })
    });
}

sidebarCollapsible();
sidebarComponents();