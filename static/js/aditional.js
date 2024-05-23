<script type="text/javascript">
$(document).ready(function () {
    $(document).keyup(function (event) {
        var key = event.keyCode || event.charCode || 0;
        if (event.ctrlKey && key == 77) { // Page One Press 1
            window.open("../Pages/LeaveMaster.aspx");
        } else if (key == 50) { // Page Two Press 2
            eval($("[id$='lbPage2']").attr("href"));
        } else if (key == 51) { // Page Three Press 3                 
            eval($("[id$='lbPage3']").attr("href"));
        } else if (key == 52) { // Alert Press 4
            $("[id$='btnAlert']").trigger('click');
        }
    })
});
</script>